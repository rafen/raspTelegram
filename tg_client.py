import logging
import sys
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine

PORT = 4458
HOST = u'localhost'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class TelegramClient(object):

    def __init__(self, users=None, groups=None, config=None):
        """
        List of allowed user to send messages: users
        List of groups to reply and receive messages: groups
        """
        self.users = users
        self.groups = groups
        self.receiver = Receiver(port=PORT)
        self.sender = Sender(host=HOST, port=PORT)
        self.receiver.start()
        # extra config
        self.config = config or {}
        # start loop
        self.receiver.message(self.main_loop())

    def _get_receiver(self, msg):
        # try to return message to group
        group_name = msg['receiver'].get('name')
        if group_name and group_name in self.groups:
            return self.groups[group_name]
        # try to return message to user
        user_name = msg['sender'].get('username')
        if user_name and user_name in self.users:
            return self.users[user_name]

    def send_reply(self, msg, message):
        self.send_message(self._get_receiver(msg), message)

    def send_message(self, to, message):
        self.sender.send_msg(to, message)

    def send_reply_photo(self, msg, file_path, caption=None):
        self.send_photo(self._get_receiver(msg), file_path, caption)

    def send_photo(self, to, file_path, caption=None):
        self.sender.send_photo(to, file_path, caption)

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
        if msg[u'event'] != u'message':
            return False
        is_valid_user = msg.get('sender') and msg['sender'].get('username') in self.users
        return is_valid_user

    def read_command(self, msg):
        if self.is_valid(msg) and msg.get('text'):
            logging.debug(u'VALID MSG: "{}"'.format(msg))
            args = msg.get('text').split(' ')
            cmd = self.CMD_PREFIX + args[0].lower()
            if hasattr(self, cmd):
                return getattr(self, cmd)(*([msg]+args[1:]))
        return False
