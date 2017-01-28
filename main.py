# Copyright (c) 2016 Adafruit Industries
# Author: Brian Norman
#
# Heavily based on https://github.com/adafruit/micropython-adafruit-pca9685/blob/master/pca9685.py
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from microbit import sleep, i2c
import PCA9685
import servo

# Initialise the PCA9685 using the default address (0x40).
pwm = PCA9685.PCA9685(i2c)

# Configure min and max servo pulse lengths (will need to adjust for different servos)
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096:

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')

# Move servo on channel O between extremes.
pwm.set_pwm(0, 0, servo_min)
sleep(1000)
pwm.set_pwm(0, 0, servo_max)
sleep(1000)

# Use servo helper class to move channel 0 by degrees
s0 = servo.Servos(i2c)
s0.position(0, 90)
sleep(1000)
s0.release(0)
