import Adafruit_DHT
import logging
import subprocess
import sys
from datetime import datetime
from RPi import GPIO
from time import time

from tg_client import TelegramClientCommands

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class TelegramCommands(TelegramClientCommands):
    BUTTON = 17

    def __init__(self, *args, **kwargs):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON, GPIO.IN)
        GPIO.add_event_detect(self.BUTTON, GPIO.FALLING,
                              callback=self.button_alert, bouncetime=200)
        super(TelegramCommands, self).__init__(*args, **kwargs)

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

    def button_alert(self, *args, **kwargs):
        self.send_alert_message()
        self.send_alert_photo()

    def send_alert_photo(self, *args, **kwargs):
        """
        Send photo to receivers
        """
        for name, value in self.groups.items():
            # call the photo command using a mockes msg with the name of the receivers
            self.command__photo({
                'sender': {'username': name},
                'receiver': {'name': name}
            })

    def send_alert_message(self, *args, **kwargs):
        for name, group_id in self.groups.items():
            self.send_message(group_id, u'ALERT!')

    def command__quit(self, msg, *args):
        self.send_reply(msg, u'Closing client. Good bye!')
        return 'quit'

    def stop(self):
        super(TelegramCommands, self).stop()
        GPIO.remove_event_detect(self.BUTTON)
