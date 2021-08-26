import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional
import os
import emails
import requests
from emails.template import JinjaTemplate
from jose import jwt
from app.core.config import settings
from typing import TypeVar
from fastapi import Query
from fastapi_pagination.default import Params as BaseParams
from pydantic import BaseModel
from fastapi_pagination.bases import RawParams, AbstractParams
import json


class Params(BaseModel, AbstractParams):
    total_items: int
    return_per_page: int

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.total_items,
            offset=self.total_items * self.return_per_page,
        )
T = TypeVar("T")

class Params(BaseParams):
    size: int = Query(500, ge=1, le=4, description="Page size")



def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None

def transpose(l1, l2) -> str:
    for i in range(len(l1[0])):
        row = []
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2


def handle_uploaded_file(f, name, type_f, file_type):
    address = os.getcwd()+'/statics/'+type_f+'/'+name+'.'+str(file_type)
    with open(address, 'wb+') as destination:
        destination.write(f.read())
        destination.close()
        return '/../static/'+type_f+'/'+name+'.'+str(file_type)

def handle_uploaded_file_project(f, dir, name, id_dir):
    address = dir+'/'+name
    with open(address, 'wb+') as destination:
        destination.write(f.read())
        destination.close()
        return address


def row2dict(row, p):
    for column in vars(row).keys():
        for item in vars(p).keys():
            if column == item:
                p.__setattr__(item, row.__getattribute__(column))
    return p

class DaemonRPC:
    def __init__(self, ip='127.0.0.1', port='19744'):
        self.IP = ip
        self.PORT = port
        self.URL = 'http://' + self.IP + ':' + self.PORT + '/json_rpc'
        self.header = {'Content-Type': 'application/json'}

    def send_request(self, method=None, param=None):
        data = {'jsonprc': '2.0', 'id': '0', 'method': method}
        if param is not None:
            data['params'] = param

        try:
            res = requests.post(self.URL, data=json.dumps(data), headers=self.header)
            return res
        except Exception as ex:
            print('ERROR : ', type(ex))
            print("Check Server Connection")

    def print_version(self):
        res = self.send_request('get_version')
        if res is None: return
        print('Version : ')
        print(res.text[1:-1].split('{')[-1][3:-3])

    def get_block_cound(self):
        res = self.send_request('get_block_count')
        if res is None: return
        # print(res.text[1:-1].split('{')[-1][3:-3].split(',')[0][3:])
        return res.text[1:-1].split('{')[-1][3:-3].split(',')[0][3:]

    def on_get_block_hash(self, height):
        res = self.send_request('on_get_block_hash', [height])
        if res is None: return
        print(res.text[1:-1].split(',')[-1][4:-2])
        return res.text[1:-1].split(',')[-1][4:-2]

    def get_block_template(self, wallet_address, reserve_size):
        params = {'wallet_address': wallet_address, 'reserve_size': int(reserve_size)}
        res = self.send_request('get_block_template', params)
        if res is None: return
        return res.text

    def submit_block(self, block_blob_data):
        param = [block_blob_data]
        res = self.send_request('submit_block', param)
        if res is None: return
        return res.text

    def get_last_block_header(self):
        res = self.send_request('get_last_block_header')
        if res is None: return
        return res.text

    def get_block_header_by_hash(self, hash):
        param = {'hash': hash}
        res = self.send_request('get_block_by_hash', param)
        if res is None: return
        return res.text

    def get_block_header_by_height(self, height):
        param = {'height': int(height)}
        res = self.send_request('get_block_header_by_height', param)
        if res is None: return
        return res.text

    def get_block_headers_range(self, start_height, end_height):
        params = {'start_height': int(start_height), 'end_height': int(end_height)}
        res = self.send_request('get_block_headers_range', params)
        if res is None: return
        return res.text

    def get_block_by_hash(self, hash):
        param = {'hash': hash}
        res = self.send_request('get_block', param)
        if res is None: return
        return res.text

    def get_block_by_height(self, height):
        param = {'height': int(height)}
        res = self.send_request('get_block', param)
        if res is None: return
        return res.text

    def get_connection(self):
        res = self.send_request('get_connection')
        if res is None: return
        return res.text

    def get_info(self):
        res = self.send_request('get_info')
        if res is None: return
        return res.text

    def get_fork_info(self):
        res = self.send_request('hard_fork_info')
        if res is None: return
        return res.text

    def set_ban_by_host(self, host, ban, seconds):
        param = {'bans': [{'host': host, 'ban': ban, 'second': seconds}]}
        res = self.send_request('set_bans', param)
        if res is None: return
        return res.text

    def set_ban_by_ip(self, ip, ban, seconds):
        param = {'bans': [{'ip': ip, 'ban': ban, 'second': seconds}]}
        res = self.send_request('set_bans', param)
        if res is None: return
        return res.text

    def get_bans(self):
        res = self.send_request('get_bans')
        if res is None: return
        return res.text

    def flush_txpool(self, list_of_transactions_ids):
        param = {'txids': list_of_transactions_ids}
        res = self.send_request('flush_txpool', param)
        if res is None: return
        return res.text

    def get_output_histogeram(self, amounts):
        params = {'amountts': amounts}
        res = self.send_request('get_output_histogram', params)
        if res is None: return
        return res.text


class WalletRPC:
    def __init__(self, ip='127.0.0.1', port='19746'):
        self.IP = ip
        self.PORT = port
        self.URL = 'http://' + self.IP + ':' + self.PORT + '/json_rpc'
        self.header = {'Content-Type': 'application/json'}

    def send_request(self, method=None, param=None):
        data = {'jsonprc': '2.0', 'id': '0', 'method': method}
        if param is not None:
            data['params'] = param

        try:
            res = requests.post(self.URL, data=json.dumps(data), headers=self.header)
            return res
        except Exception as ex:
            print('ERROR : ', type(ex))
            print("Check Server Connection")

    def create_wallet(self, wallet_name, password):
        param = {'filename': wallet_name, 'password': password, 'language': 'English'}
        res = self.send_request('create_wallet', param)
        if res is None: return

    def open_wallet(self, wallet_file, password):
        param = {'filename': wallet_file, 'password': password}
        res = self.send_request('open_wallet', param)
        if res is None: return

    def get_transfers(self, mode):
        param = {mode: True}
        res = self.send_request('get_transfers', param)
        if res is None: return
        print(res.text)

    def get_accounts(self):
        res = self.send_request('get_accounts')
        if res is None: return
        # print(res.text)
        return res

    def transfer(self, wallet_address, amount):
        data = {'destinations': [{'amount': amount, 'address': wallet_address}]}
        res = self.send_request('transfer', data)
        if res is None: return
        return res.text

    def close_wallet(self, ):
        res = self.send_request('close_wallet')
        return res.text


class WalletOlancer:
    def __init__(self, ip='127.0.0.1', port='19746'):
        self.wallet_rpc = WalletRPC(ip, port)

    def create_wallet(self, username, password):
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.create_wallet(username, password)

    def check_wallet(self, username, password):
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.open_wallet(username, password)
        res = self.wallet_rpc.get_accounts()
        data = json.loads(res.text)['result']['subaddress_accounts'][0]
        wallet_info = {'address': data['base_address'], 'balance': data['balance']}
        return wallet_info

    def transfer(self, from_user, from_pass, to_user, to_pass, amount):
        wallet_info_des = self.check_wallet(to_user, to_pass)
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.open_wallet(from_user, from_pass)
        res = self.wallet_rpc.transfer(wallet_info_des['address'], (amount * (10 ** 9)))
        return res

    def transfer_to_address(self, username, password, address, amount):
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.open_wallet(username, password)
        res = self.wallet_rpc.transfer(address, (amount * (10 ** 9)))
        res = json.loads(res)
        return res
