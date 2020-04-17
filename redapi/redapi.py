import requests
import time
import logging
from collections import deque

headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept-Charset': 'utf-8',
    'User-Agent': 'redapi-agnitrate'
    }
supported_api_versions = ['redacted-v2.0']
default_ratelimit = (5, 10) # ratelimited to 5 calls every 10 seconds. 

class LoginException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Unknown Error'
        super(LoginException, self).__init__(msg)

class RequestException(Exception):
    pass

class RatelimitException(Exception):
    pass

logging.basicConfig(format='%(levelname)s:%(message)s')

class RedAPI:
    def __init__(self, apikey=None, server="https://redacted.ch", ratelimit=(None, None)):
        self.apikey = apikey
        self.server = server
        self.username = None
        
        self.session = requests.Session()
        headers['Authorization'] = apikey
        self.session.headers = headers

        self.ratelimit = ratelimit if ratelimit != (None, None) else default_ratelimit
        self._historyqueue = []

        self._login()



    def _ratelimited_api_call(self, method, url, params=None, allow_redirects=False):
        nowtime = time.time()
        self._historyqueue = [x for x in self._historyqueue if nowtime - x < self.ratelimit[1]]
        if len(self._historyqueue) >= self.ratelimit[0]:
            logging.warning('You are being ratelimited to {} requests per {} seconds. '
                            'Use the ratelimit argument to change this setting at your own risk.'
                            .format(*self.ratelimit))
            raise RatelimitException
        
        r = self.session.request(method, url, params=params, allow_redirects=allow_redirects)
        self._historyqueue.append(time.time())
        return r

    def _login(self):
        '''Logs in user'''
        index = self.server + '/ajax.php?action=index'
        r = self._ratelimited_api_call('POST', index, allow_redirects=False)
        r_json = r.json()
        if r_json['status'] == 'success':
            if 'api_version' not in r_json or r_json['api_version'] not in supported_api_versions:
                logging.warning('api_version {} is not supported.'.format(
                    'None' if 'api_version' not in r_json else r_json['api_version']
                ))
            self.username = r_json['response']['username']
        else:
            if 'error' in r_json:
                err = r_json['error']
            raise LoginException(err)

    def get_torrent(self, torrent_id, usetoken=0):
        '''Downloads the torrent at torrent_id'''
        torrentpage = self.server + '/ajax.php'
        params = {'action': 'download', 'id': torrent_id, 'usetoken': usetoken}
        r = self._ratelimited_api_call('GET', torrentpage, params=params, allow_redirects=False)
        if r.status_code == 200 and 'application/x-bittorrent' in r.headers['content-type']:
            return r.content
        return None

    def logout(self):
        logging.warning('logout is deprecated')

    def request(self, action, method='POST', **kwargs):
        '''Makes an AJAX request at a given action page'''
        ajaxpage = self.server + '/ajax.php'
        params = {'action': action}
        params.update(kwargs)

        r = self._ratelimited_api_call(method, ajaxpage, params=params, allow_redirects=False)
        try:
            r_json = r.json()
            if r_json["status"] != "success":
                raise RequestException
            return r_json
        except ValueError:
            raise RequestException

    def manual_request(self, req_str, method='POST'):
        ajaxpage = self.server + '/ajax.php'
        url = ajaxpage + '?' + req_str
        r = self._ratelimited_api_call(method, url, allow_redirects=False)
        try:
            r_json = r.json()
            if r_json["status"] != "success":
                raise RequestException
            return r_json
        except ValueError:
            raise RequestException
