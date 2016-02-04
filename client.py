# -*- coding: utf-8 -*-
from commands import TelegramCommands

try:
    # Custom settings in your device
    from local_settings import config
except Exception:
    # default settings
    config = {
        'from_users': [u'rafenm'],
        'groups': {
            u'Example Chat': u'chat#108633111'
        },
        'to_users': {
            u'rafenm': u'Rafael_Capdevielle'
        }
    }

if __name__ == '__main__':
    client = TelegramCommands(**config)
