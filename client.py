# -*- coding: utf-8 -*-
from commands import TelegramCommands


if __name__ == '__main__':
    client = TelegramCommands(
        from_users=[u'rafenm'],
        to_users={
            u'rafenm': u'Rafael_Capdevielle'
        }
    )
