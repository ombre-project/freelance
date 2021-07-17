import json
import requests


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
        print(res.text)

    def transfer(self, wallet_address, amount):
        data = {'destinations': [{'amount': amount, 'address': wallet_address}]}
        res = self.send_request('transfer', data)
        if res is None: return
        print(res.text)


def main():
    wallet = WalletRPC()
    wallet.open_wallet('wallet_4', 'Pouyan')
    # wallet.get_transfers('in')
    wallet.get_accounts()
    # wallet.transfer('Shad379LPu3ASYBM14wsGuXNQP32N9HMXF4mhV234sZmA3FeGh79kgw', 1000000000)


#
if __name__ == '__main__':
    main()
