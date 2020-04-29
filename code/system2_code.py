import os
import time
import math
import digitalio
import board
import audioio

from adafruit_crickit import crickit


class PlantarisSystem():
    def __init__(self, relay_pump_signal=None,
          moisture_sensor_signal=None,
          water_level_signal=None,
          audio_filename=None,
          water_value=0,
          moisture_value=0,
          water_time=0):

        if not all(relay_pump_signal, moisture_sensor_signal, water_level_signal,
                   audio_filename, water_value, moisture_value, water_time):
            print("Setup error")

        self.ss = crickit.seesaw
        self.relay_pump = relay_pump_signal
        self.moisture_sensor = moisture_sensor_signal
        self.water_level = water_level_signal

        # Relay needs to be OUTPUT
        # but the other components are INPUT by default
        self.ss.pin_mode(relay_pump, ss.OUTPUT)
        # Enabling at the beginning to close the circuit
        self.ss.digital_write(relay_pump, True)

        self.audio_file = audio_filename
        self.watering_time = water_time

        self.water_critical_value = water_value
        self.moisture_critical_value = moisture_value

    
    def play_message(self):
    
        with open(self.audio_file, "rb") as f:
            wav_file = audioio.WaveFile(f)
            audio = audioio.AudioOut(board.A0)
            audio.play(wav_file)
            while audio.playing:
                pass

    def water_level_ok(self):
        value = self.ss.analog_read(self.water_level)

        if value <= self.water_critical_value:
            return False
        else:
            return True

    def moisture_level_ok(self):
        value = self.ss.analog_read(self.moisture_sensor)

        if value <= self.moisture_critical_value:
            return False
        else:
            return True
    
    def water_plant(self):
    
        self.ss.digital_write(self.relay_pump, False)
        time.sleep(watering_time)
        self.ss.digital_write(self.relay_pump, True)
    

## Main
# the configuration of the system is being done while creating
# the PlantarisSystem instance.
# In this case you can see the connectionf to the Crickit
# and where each device is connected.
# If the ports of your configuration are different, please adapt it.
plantaris = PlantarisSystem(relay_pump_signal=crickit.SIGNAL1,
                            moisture_sensor_signal=crickit.SIGNAL2,
                            water_level_signal=crickit.SIGNAL3,
                            audio_filename="outfinal.wav",
                            water_value=900,
                            moisture_value=200,
                            water_time=1)

wait_time = 3600 # 1 hour!

while True:
    if not plantaris.water_level_ok():
        plantaris.play_message()
    
    if not plantaris.moisture_level_ok():
        plantaris.water_plant()

    time.sleep(wait_time)
