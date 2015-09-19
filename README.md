# raspTelegram
A simple Telegram Client for Raspberry Pi

<img src="https://dl.dropboxusercontent.com/u/14133267/telegram.raspberry.png" alt="raspTelegram screenshot" width="400">

## Installation

Install the Telegram CLI (from @vysheng), follow the [official Instructions](https://github.com/vysheng/tg)

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

This client can be also installed as a daemon using ths init.d/raspTelegram.

In ubuntu, copy both files to /etc/init.d/ folder. and then install them as defaults scripts:

    sudo update-rc.d telegram-daemon defaults
    sudo update-rc.d raspTelegram defaults
