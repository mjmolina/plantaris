# Code

On this directory you can find all the different scripts used
during the talk.

Make sure to install all the requirements for the telegram bot,
flask application, and Circuit Playground Express monitor script.

## Circuit python

These codes need to be placed on the internal memory of your CPX
with the name `code.py`.

Please make sure you have configure the scripts before running them
since each component needs to be defined inside the code by the exact
port being used.

Additionally, depending on your sensors, and configuration,
you need to adapt the number limits of each situation.

### System 1

Files:
 * [system2_code.py](system2_code.py)

This is a simple code that only reads the moisture sensor,
checks the level and activate the relay to run the water pump.

### System 2

Files:
 * [system2_code.py](system2_code.py)
 * [outfinal.wav](outfinal.wav)

This systems uses the Crickit and CPX boards.
Since it is a bit more complicated compared the first version,
a general class is provided to encapsulate all the functionality
of the system.

There is also a WAV file that needs to be copy to the board memory
to get the voice notification when the water level is low.


## Monitor System

Files:
 * [monitor_system.py](monitor_system.py)

This is the main script that reads the output from the CPX system
and store it locally on your Raspberry Pi device.

The specific file will be used by the Telegram Bot and Flask application
so make sure to configure it right after your CPX system is working.

To execute just run:

```
python monitor_system.py
```

Please notice that the connection configuration is written inside
on the line:

```
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0.5)
```

if your device has a different entry or port, make sure to change it
before starting it.

This script will generate `output.txt` and `errors.txt`
for you to check what the system is reading.

## Flask application

Files:
 * [flask_monitor.py](flask_monitor.py)
 * [templates/](templates/)
 * [static/](static/)

To start the application and make it visible inside your network,
you need to run:

```
FLASK_APP=flask_monitor.py flask run --host=0.0.0.0
```

This simple application relies on only one template called `templates/data.html`
and in some elements from **bootstrap** that can be found onf the `static`
directory.

## Telegram bot

Files:
 * [telegram_bot.py](telegram_bot.py)
 * [config.ini](#) Not included!
 * [start_bot](start_bot)


Due to some issues I had for my current system configuration,
I created a small script to initialize the bot, called `start_bot`.
This just adds `libatomic.so.1` for the execution of the main script.

Normally, this will just require to run:

```
python telegram_bot.py
```

For the bot configuration, you would need to create a `config.ini`
file containing the token you got when registering your bot.
More information on how to register your bot can be found
[here](https://core.telegram.org/bots).

Also, for the bot to send you messages, you will require to start
a conversation with your bot, and then send a message to the
`@userinfobot` to get the chat ID that you need to store on the `config.ini`
too.

```
# config.ini
[DEFAULT]
Token = xxxxxxxxxx
ChatID = yyyyy
```
