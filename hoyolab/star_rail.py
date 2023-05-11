from .base import Base

class StarRail(Base):
    def __init__(self, cookie: str = None):
        super().__init__(cookie, 2)
        self.api = 'https://sg-public-api.hoyolab.com'
        self.act_id = 'e202303301540311'

        self.sign_info_url = f'{self.api}/event/luna/info?lang={self.lang}&act_id={self.act_id}'
        self.rewards_info_url = f'{self.api}/event/luna/home?lang={self.lang}&act_id={self.act_id}'
        self.sign_url = f'{self.api}/event/luna/sign?lang={self.lang}'

