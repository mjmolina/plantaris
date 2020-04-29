import time
import digitalio
import touchio
import board

# We connect the relay to the A0 port on the CPX
relay = digitalio.DigitalInOut(board.A0)

# Since the INPUT mode is by default, we change to OUTPUT,
# to be able to send instructions to it.
relay.switch_to_output()

# The moisture sensors is on the A1 port
touch = touchio.TouchIn(board.A1)
# The relay was configure to use the Always Close gate,
# so we need to set it as true for the relay to be inactive.
relay.value = True

# Period of time to check the system
wait_time = 1

# Perior of time to keep watering the plant
# This heavily depends on the voltage feeding the pump,
# and its power.
watering_time = 1

# This needs to be adapted according the moisture sensor
dry_value = 4000

while True:
    
    # Read value
    sensor_value = touch.raw_value
    print("Sensor value:", sensor_value)

    if sensor_value < dry_value:
        print("Starting watering...")
        # We connect the relay on the "always closed"
        # and that is why adding a Falso to "always closed"
        # means Open.
        relay.value = False
        time.sleep(watering_time)
        print("Finishing watering.")
    else:
        # if the level is OK, we just make sure the relay is closed,
        # and we sleep until the next period.
        relay.value = True
        time.sleep(wait_time)
