import http
from datetime import datetime
from .utils import cookie_to_dict, request, extract_subset_of_dict
from utils import log

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBSOversea/1.5.0'}



class Base(object):
    def __init__(self, cookie: str = None, game_id: int = None):
        self.cookie = extract_subset_of_dict(cookie_to_dict(cookie), ['cookie_token', 'account_id'])
        self.headers = headers
        self.account_info = {}
        self._account_info_last_update = None
        self._sign_info = {}
        self._sign_info_last_update = None
        self.account_id = self.cookie['account_id']
        self.server = None
        self.game_uid = None
        self.game_id = game_id
        self.act_id = None
        self.lang = 'zh-cn'
        self.role_api = 'https://bbs-api-os.hoyolab.com'
        self.api = None

        self.account_info_url = f'{self.role_api}/game_record/card/wapi/getGameRecordCard?uid={self.account_id}'
        self.sign_info_url = None
        self.rewards_info_url = None
        self.sign_url = None
        self.character_url = f'{self.api}/game_record/genshin/api/index?server={self.server}&role_id={self.game_uid}'
        self.spiral_abyss_url = f'{self.api}/game_record/genshin/api/spiralAbyss?server={self.server}&role_id={self.game_uid}&schedule_type=1'

    def require_account_info(func):
        def update(self):
            if (len(self.account_info) < 1) or (not self._account_info_last_update) or ((datetime.now() - self._account_info_last_update).total_seconds() > 3600):
                response = request('get', self.account_info_url, headers=self.headers, cookies=self.cookie).json()
                if response['retcode'] != 0:
                    log.error(f'url={self.account_info_url}, resp={response["message"]}')
                    return None
                account_info = [i for i in response['data']['list'] if i['game_id'] == self.game_id]
                if len(account_info) != 1:
                    return None
                self.account_info = account_info[0]
                self._account_info_last_update = datetime.now()
            return func(self)
        return update

    def require_sign_info(func):
        def update(self):
            if (len(self._sign_info) < 1) or (not self._sign_info_last_update) or ((datetime.now() - self._sign_info_last_update).total_seconds() > 3600):
                r = request('get', self.sign_info_url, headers=self.headers, cookies=self.cookie)
                log.debug(f'code = {r.status_code}, method = get, url = {self.sign_info_url}, headers = {self.headers}, cookies = {self.cookie}')
                if r.status_code != http.HTTPStatus.OK:
                    return None
                response = r.json()
                if response['retcode'] != 0:
                    log.error(f'url={self.sign_info_url}, resp={response["message"]}')
                    return None
                self._sign_info = response['data']
                self._sign_info_last_update = datetime.now()
            return func(self)
        return update


    @property
    def sign_info(self):
        return self._sign_info

    @require_account_info
    @require_sign_info
    def sign(self) -> str:
        if self.sign_info['is_sign'] == True:
            return "today already check-in"
        payload = {
            'act_id': self.act_id,
            'region': self.account_info['region'],
            'uid': self.account_info.get('game_role_id')
        }
        response = request('post', self.sign_url, headers=self.headers, json=payload, cookies=self.cookie).json()
        log.info(response)
        # 0:      success
        # -5003:  already checked in
        if response['retcode'] == 0:
            self._sign_info['total_sign_day'] += 1
            self._sign_info['is_sign'] = True
            return 'check-in success'
        elif response['retcode'] == -5003:
            return response['message']
        else:
            return f'error in check-in, data = {response["data"]}'