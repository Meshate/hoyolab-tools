from .base import Base

class Genshin(Base):
    def __init__(self, cookie: str = None):
        super().__init__(cookie, 2)
        self.api = 'https://sg-hk4e-api.hoyolab.com'
        self.act_id = 'e202102251931481'

        self.sign_info_url = f'{self.api}/event/sol/info?lang={self.lang}&act_id={self.act_id}'
        self.rewards_info_url = f'{self.api}/event/sol/home?lang={self.lang}&act_id={self.act_id}'
        self.sign_url = f'{self.api}/event/sol/sign?lang={self.lang}'