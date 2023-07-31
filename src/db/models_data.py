from enum import Enum


class Channel(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'
