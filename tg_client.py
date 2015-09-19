import logging
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine

PORT = 4458
HOST = u'localhost'

logging.basicConfig()


class TelegramClient(object):

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

    def send_reply(self, msg, message):
        to = msg['sender'].get('username')
        self.send_message(to, message)

    def send_message(self, to, message):
        if to in self.to_users:
            self.sender.send_msg(self.to_users[to], message)

    def send_reply_photo(self, msg, file_path, caption=None):
        to = msg['sender'].get('username')
        self.send_photo(to, file_path, caption)

    def send_photo(self, to, file_path, caption=None):
        if to in self.to_users:
            self.sender.send_photo(self.to_users[to], file_path, caption)

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


class TelegramClientCommands(TelegramClient):

    CMD_PREFIX = 'command__'

    def is_valid(self, msg):
        return msg.get('sender') and msg['sender'].get('username') in self.from_users

    def read_command(self, msg):
        if self.is_valid(msg) and msg.get('text'):
            args = msg.get('text').split(' ')
            cmd = self.CMD_PREFIX + args[0].lower()
            if hasattr(self, cmd):
                return getattr(self, cmd)(*([msg]+args[1:]))
        return False
