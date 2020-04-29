import re
import logging
import configparser

import cv2
import numpy as np

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

from emoji import emojize


def clean_message(s):
    for i in ["-"]:
        s = s.replace(i, f"\{i}")
    return s

def get_image():
    filename = "opencv_snap.png"
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite(filename, image)
    return filename

def get_video():
    filename = "output.avi"
    cap = cv2.VideoCapture(0)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640,480))

    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
            # 100 -> 5s
            # 50 -> 2.5s
            if i == 50:
                break
        else:
            break
        i += 1

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return filename


# Main command functions
def test(update, context):
    logging.info("test command")
    context.bot.send_message(chat_id=update.effective_chat.id, text="It's working")

def data(update, context):
    logging.info("data command")
    line = None
    with open("output.txt", "r") as f:
        line = f.readlines()[-1]

    s_date, _, s_relay, s_moisture, s_water_level = line.split(";")

    msg = clean_message(f"{emojize(':herb:')} {s_date}\n\nRelay: {s_relay}\nMoisture: {s_moisture}\nWater level: {s_water_level}")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )

def smile(update, context):
    logging.info("smile command")
    filename = get_image()

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(filename, 'rb')
    )

def dance(update, context):
    logging.info("dance command")
    filename = get_video()
    context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=open(filename, 'rb'),
            supports_streaming=True
    )


def callback_minute(context: telegram.ext.CallbackContext):
    logging.info("Checking output")
    line = None
    with open("output.txt", "r") as f:
        line = f.readlines()[-1]
    s_date, _, _, s_moisture, s_water_level = line.split(";")

    if int(s_moisture) < 415:
        context.bot.send_message(chat_id=CHAT_ID,
                text=f"Moisture level < 415")
    if int(s_water_level) < 6:
        context.bot.send_message(chat_id=CHAT_ID,
                text=f"Water level < 6")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)

    config = configparser.ConfigParser()
    config.read("config.ini")

    TOKEN = config["DEFAULT"]["Token"]
    CHAT_ID = config["DEFAULT"]["ChatID"]

    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    test_handler = CommandHandler("test", test)
    dispatcher.add_handler(test_handler)

    # Get last line from the data
    data_handler = CommandHandler("data", data)
    dispatcher.add_handler(data_handler)

    # Get image
    smile_handler = CommandHandler("smile", smile)
    dispatcher.add_handler(smile_handler)

    # Get short video
    dance_handler = CommandHandler("dance", dance)
    dispatcher.add_handler(dance_handler)

    # Monitoring handler every 10 minutes
    j = updater.job_queue
    job_minute = j.run_repeating(callback_minute, interval=600, first=0)

    updater.start_polling()
