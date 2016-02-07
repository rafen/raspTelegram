import logging
import sys
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine

PORT = 4458
HOST = u'localhost'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class TelegramClient(object):

    def __init__(self, from_users=[], groups=None, to_users=None):
        """
        List of allowed user to send messages: from_users
        List of groups to reply and receive messages: groups
        List of users to receive the message if no group is specified: to_users
        """
        self.from_users = from_users
        self.groups = groups
        # if group is defined default receivers is the group
        if groups:
            self.receivers = self.groups
        else:
            self.receivers = to_users
        self.receiver = Receiver(port=PORT)
        self.sender = Sender(host=HOST, port=PORT)
        self.receiver.start()
        # start loop
        self.receiver.message(self.main_loop())

    def _get_receiver(self, msg):
        if self.groups:
            key = msg['receiver'].get('name')
        else:
            key = msg['sender'].get('username')
        return self.receivers[key]

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
        is_valid_user = msg.get('sender') and msg['sender'].get('username') in self.from_users
        is_valid_group = not self.groups or (msg.get('receiver') and msg['receiver'].get('name') in self.groups)
        return is_valid_user and is_valid_group

    def read_command(self, msg):
        logging.debug(u'MSG: "{}"'.format(msg))
        if self.is_valid(msg) and msg.get('text'):
            args = msg.get('text').split(' ')
            cmd = self.CMD_PREFIX + args[0].lower()
            if hasattr(self, cmd):
                return getattr(self, cmd)(*([msg]+args[1:]))
        return False
