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
import json


def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
) -> None:
    """
    complete later
    :param email_to:
    :param subject_template:
    :param html_template:
    :param environment:
    :return:
    """
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
    """
    complete later
    :param email_to:
    :return:
    """
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
    """
    complete later
    :param email_to:
    :param email:
    :param token:
    :return:
    """
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
    """
    complete later
    :param email_to:
    :param username:
    :param password:
    :return:
    """
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
    """
    complete later
    :param email:
    :return:
    """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    complete later
    :param token:
    :return:
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def transpose(l1, l2) -> str:
    """
    to transpose 2d array
    :param l1:
    :type l1:list
    :param l2:
    :type l2: list
    :return:
    :rtype: list
    """
    for i in range(len(l1[0])):
        row = []
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2


def handle_uploaded_file(f, name, type_f, file_type):
    """
    to write file in a path and get the address of that
    :param f: file
    :type f: FILE
    :param name: name of the file
    :type name: str
    :param type_f: directory name
    :type type_f: str
    :param file_type: type of the file
    :type file_type:
    :return: the address of file
    :rtype: str
    """
    address = os.getcwd() + '/statics/' + type_f + '/' + name + '.' + str(file_type)
    with open(address, 'wb+') as destination:
        destination.write(f.read())
        destination.close()
        return '/../static/' + type_f + '/' + name + '.' + str(file_type)


def handle_uploaded_file_project(f, dir, name, id_dir):
    """
    to write file in a path and get the address of that
    :param f: file
    :type f: FILE
    :param name: name of the file
    :type name: str
    :param dir: directory to save
    :type dir: str
    :param id_dir: directory to save
    :type id_dir: str
    :return: address of saving file
    :rtype: str
    """
    address = dir + '/' + name
    with open(address, 'wb+') as destination:
        destination.write(f.read())
        destination.close()
        return address


def row2dict(row, p):
    """
    to convert p to a schemas model
    :param row: object
    :type row: object
    :param p: object
    :type p: object
    :return: schemas model
    :rtype: object
    """
    for column in vars(row).keys():
        for item in vars(p).keys():
            if column == item:
                p.__setattr__(item, row.__getattribute__(column))
    return p


class WalletRPC:
    """
    connect to ombre-wallet-rpc
    """

    def __init__(self, ip='127.0.0.1', port='19746'):
        """
        initial function for connect to ombre-wallet-rpc
        :param ip:string,wallet-rpc daemon ip
        :param port:string,wallet-rpc daemon port
        """
        self.IP = ip
        self.PORT = port
        self.URL = 'http://' + self.IP + ':' + self.PORT + '/json_rpc'
        self.header = {'Content-Type': 'application/json'}

    def send_request(self, method=None, param=None):
        """
        send json data to rpc daemon
        :param method:string,method of api
        :param param:dict,dictionary of parameters
        :return:response of daemon
        :rtype:string
        """
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
        """
        create wallet in file directory
        :param wallet_name:string,name of wallet
        :param password:string, password for wallet
        :return: None
        """
        param = {'filename': wallet_name, 'password': password, 'language': 'English'}
        res = self.send_request('create_wallet', param)
        if res is None: return

    def open_wallet(self, wallet_file, password):
        """
        open wallet with filename and password
        :param wallet_file:string, open wallet with this file name
        :param password:string, password of wallet
        :return: None
        """
        param = {'filename': wallet_file, 'password': password}
        res = self.send_request('open_wallet', param)
        if res is None: return

    def get_transfers(self, mode):
        """
        show all transfers that the wallet done
        :param mode:
        :return:
        """
        param = {mode: True}
        res = self.send_request('get_transfers', param)
        if res is None: return
        print(res.text)

    def get_accounts(self):
        """
        get the open wallet information
        :return: json file
        """
        res = self.send_request('get_accounts')
        if res is None: return
        # print(res.text)
        return res

    def transfer(self, wallet_address, amount):
        """
        transfer amount ombre to wallet_address from open wallet
        :param wallet_address:string,destination wallet address
        :param amount:int,amount of ombre in atomic unit
        :return:response node
        :rtype:string
        """
        data = {'destinations': [{'amount': amount, 'address': wallet_address}]}
        res = self.send_request('transfer', data)
        if res is None: return
        return res.text

    def close_wallet(self, ):
        """
        close open wallet
        :return:string,response node
        """
        res = self.send_request('close_wallet')
        return res.text


class WalletOlancer:
    """
    the function that olancer web site use for conncting ombre-wallet-rpc and use it
    """

    def __init__(self, ip='127.0.0.1', port='19746'):
        """
        connect to ombre-wallet-rpc
        :param ip:string,ombre-wallet-rpc ip
        :param port:string,ombre-wallet-rpc port
        """
        self.wallet_rpc = WalletRPC(ip, port)

    def create_wallet(self, username, password):
        """
        create wallet with the username as file name and password
        :param username:string,wallet file name
        :param password:string,wallet password
        :return:
        """
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.create_wallet(username, password)

    def check_wallet(self, username, password):
        """
        read address and balance form wallet
        :param username:string,wallet file name
        :param password:string,wallet password
        :return:wallet info
        :rtype:dict
        """
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.open_wallet(username, password)
        res = self.wallet_rpc.get_accounts()
        data = json.loads(res.text)['result']['subaddress_accounts'][0]
        wallet_info = {'address': data['base_address'], 'balance': data['balance']}
        return wallet_info

    def transfer(self, from_user, from_pass, to_user, to_pass, amount):
        """
        transfer ombre from to users
        :param from_user:string,file name user one
        :param from_pass:string,password user one
        :param to_user:string,file name user two
        :param to_pass:string,password user two
        :param amount:int,number of ombre that transfer from user one to user two
        :return:node response
        :rtype:str
        """
        wallet_info_des = self.check_wallet(to_user, to_pass)
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.open_wallet(from_user, from_pass)
        res = self.wallet_rpc.transfer(wallet_info_des['address'], (amount * (10 ** 9)))
        return res

    def transfer_to_address(self, username, password, address, amount):
        """
        transfer ombre from wallet to address
        :param username:string, wallet file name
        :param password:string, wallet password
        :param address:string, address of destination wallet
        :param amount:string, amount of ombre to transfer
        :return:node response
        "rtype:dict
        """
        self.wallet_rpc.close_wallet()
        self.wallet_rpc.open_wallet(username, password)
        res = self.wallet_rpc.transfer(address, (amount * (10 ** 9)))
        res = json.loads(res)
        return res
