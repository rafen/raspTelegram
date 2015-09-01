# -*- coding: utf-8 -*-
import Adafruit_DHT
import logging
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine

PORT = 4458
HOST = u'localhost'

logging.basicConfig()


class TelegramClient(object):

    CMD_PREFIX = 'command__'

    def __init__(self, from_users=[], to_users=None):
        """
        List of allowed user to send messages: from_users
        List of users that will receive the message: to_users
        """
        self.from_users = from_users
        self.to_users = to_users
        self.receiver = Receiver(port=PORT)
        self.sender = Sender(host=HOST, port=PORT)
        self.receiver.start()
        # start loop
        self.receiver.message(self.main_loop())

    def command__hello(self, msg, *args):
        self.send_reply(msg, u'Hi!')

    def command__thanks(self, msg, *args):
        self.send_reply(msg, u'You are welcome!')

    def command__temp(self, msg, *args):
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        if humidity is not None and temperature is not None:
            res = u'Temp={0:0.1f} C  Humidity={1:0.1f}%'.format(
                temperature, humidity
            )
        else:
            res = u'Failed to get reading. Try again!'
        self.send_reply(msg, res)

    def command__quit(self, msg, *args):
        self.send_reply(msg, u'Closing client. Good bye!')
        return 'quit'

    def send_reply(self, msg, message):
        to = msg['sender'].get('username')
        self.send_message(to, message)

    def send_message(self, to, message):
        if to in self.to_users:
            self.sender.send_msg(self.to_users[to], message)

    def is_valid(self, msg):
        return msg.get('sender') and msg['sender'].get('username') in self.from_users

    def read_command(self, msg):
        if self.is_valid(msg) and msg.get('text'):
            args = msg.get('text').split(' ')
            cmd = self.CMD_PREFIX + args[0].lower()
            if hasattr(self, cmd):
                return getattr(self, cmd)(*([msg]+args[1:]))
        return False

    def stop(self):
        self.receiver.stop()

    @coroutine
    def main_loop(self):
        try:
            while True:
                msg = (yield)
                if self.read_command(msg) == 'quit':
                    break
        except Exception as e:
            print(u"ERROR: {}".format(e))
        finally:
            self.stop()


if __name__ == '__main__':
    client = TelegramClient(
        from_users=[u'rafenm'],
        to_users={
            u'rafenm': u'Rafael_Capdevielle'
        }
    )
