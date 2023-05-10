from .utils import cookie_to_dict

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBSOversea/1.5.0'}

class Base(object):
    def __int__(self, cookie: str = None):
        self.cookie = cookie_to_dict(cookie)
        self.headers = headers
        self.account_info = {}
        self.uid = None
        self.server = None
        self.role_id = None
        self.api = 'https://bbs-api-os.hoyolab.com'

        self.roles_info_url = f'{self.api}/game_record/card/wapi/getGameRecordCard?uid={self.uid}'
        self.sign_info_url = None
        self.rewards_info_url = None
        self.sign_url = None
        self.character_url = f'{self.api}/game_record/genshin/api/index?server={self.server}&role_id={self.role_id}'
        self.spiral_abyss_url = f'{self.api}/game_record/genshin/api/spiralAbyss?server={self.server}&role_id={self.role_id}&schedule_type=1'