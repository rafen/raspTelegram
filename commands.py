import Adafruit_DHT
import subprocess
from datetime import datetime
from time import time

from tg_client import TelegramClientCommands


class TelegramCommands(TelegramClientCommands):

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

    def command__photo(self, msg, *args):
        # take picture:
        timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d_%H_%M_%S')
        file_name = u'/home/pi/photos/{}.jpg'.format(timestamp)
        self.send_reply(msg, u'taking picture...')
        subprocess.call([
            'fswebcam',
            '-r', '640x480', '-S', '3',  '--jpeg', '85', '--save',  file_name
        ])
        # send picture
        self.send_reply_photo(msg, file_name, u'Photo: {}'.format(timestamp))

    def command__quit(self, msg, *args):
        self.send_reply(msg, u'Closing client. Good bye!')
        return 'quit'