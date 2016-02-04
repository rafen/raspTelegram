# raspTelegram
A simple Telegram Client for Raspberry Pi

<img src="https://dl.dropboxusercontent.com/u/14133267/telgram.raspberry.photo.png" alt="raspTelegram screenshot photo" width="400">

## Installation

Install the Telegram CLI (from @vysheng), follow the [official Instructions](https://github.com/vysheng/tg)

Optionally install camera: [webcams and raspberry pi](https://www.raspberrypi.org/documentation/usage/webcams/)

then install raspTelegram:

    git clone https://github.com/rafen/raspTelegram.git
    cd raspTelegram

create a virtualenv for the project:

    mkvirtualenv raspTelegram

install dependencies:

    pip install -r requirements.txt

Install pytg following the official doc (avoid using sudo): https://github.com/luckydonald/pytg#install


## Configuration:

In this example we are using the telegram client as a daemon:
https://github.com/vysheng/tg/wiki/Running-Telegram-CLI-as-Daemon if you have problems with the installation you can use the script in  init.d/telegram-daemon of this repo.

This client can be also installed as a daemon using upstart.
First install upstart and reboot (see for more info: http://infovore.org/archives/2013/08/09/running-scripts-on-startup-with-your-raspberry-pi/):

    sudo apt-get install upstart

In your pi, copy both files to /etc/init/

    sudo cp init/telegram-daemon.conf /etc/init/
    sudo cp init/rasp-telegram.conf /etc/init/
