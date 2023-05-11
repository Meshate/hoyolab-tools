import struct

from .utils import cookie_to_dict, request, extract_subset_of_dict
from .exception import RequestException

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBSOversea/1.5.0'}



class Base(object):
    def __int__(self, cookie: str = None):
        self.cookie = extract_subset_of_dict(cookie_to_dict(cookie), ['cookie_token', 'account_id'])
        self.headers = headers
        self.account_info = {}
        self.account_id = self.cookie['account_id']
        self.server = None
        self.game_role_id = None
        self.game_id = None
        self.role_api = 'https://bbs-api-os.hoyolab.com'
        self.api = 'https://sg-hk4e-api.hoyolab.com'

        self.account_info_url = f'{self.role_api}/game_record/card/wapi/getGameRecordCard?uid={self.account_id}'
        self.sign_info_url = None
        self.rewards_info_url = None
        self.sign_url = None
        self.character_url = f'{self.api}/game_record/genshin/api/index?server={self.server}&role_id={self.game_role_id}'
        self.spiral_abyss_url = f'{self.api}/game_record/genshin/api/spiralAbyss?server={self.server}&role_id={self.game_role_id}&schedule_type=1'

    def require_info(func):
        def update(self, *args, **kwargs):
            if len(self.account_info) < 1:
                response = request('get', self.account_info_url, headers=self.headers, cookies=self.cookie).json()
                if response['retcode'] != 0:
                    raise RequestException(response['message'])
                try:
                    self.account_info = [i for i in response['data']['list'] if i['game_id'] == self.game_id][0]
                except Exception as e:
                    raise RequestException(e)
            return func(self, *args, **kwargs)
        return update

    @property
    def sign_info(self):
        return self.sign_info

