headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBSOversea/1.5.0'}

class Base(object):
    def __int__(self, cookie: str):
        self.cookie = cookie
        self.headers = headers
        self.uid = None
        self.api = 'https://bbs-api-os.hoyolab.com'

        self.roles_info_url = f'{self.api}/game_record/card/wapi/getGameRecordCard?uid={self.uid}'
        self.sign_info_url = None
        self.rewards_info_url = None
        self.sign_url = None
        self.spiral_abyss_url = None