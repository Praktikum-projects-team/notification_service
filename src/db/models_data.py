from sqlalchemy import Enum


class Channel(Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'
