# Copyright (c) 2016 Adafruit Industries
# Author: Brian Norman
#
# Heavily based on Tony DiCola's driver at https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/Adafruit_PCA9685/PCA9685.py
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
import math, ustruct

# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04
RESET              = 0x00


class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, i2c, address=PCA9685_ADDRESS):
        """Initialize the PCA9685."""
        self.address = address
        i2c.write(self.address, bytearray([MODE1, RESET])) # reset not sure if needed but other libraries do it
        self.set_all_pwm(0, 0)
        i2c.write(self.address, bytearray([MODE2, OUTDRV]))
        i2c.write(self.address, bytearray([MODE1, ALLCALL]))
        sleep(5)  # wait for oscillator
        i2c.write(self.address, bytearray([MODE1])) # write register we want to read from first
        mode1 = i2c.read(self.address, 1)
        mode1 = ustruct.unpack('<H', mode1)[0]
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        i2c.write(self.address, bytearray([MODE1, mode1]))
        sleep(5)  # wait for oscillator

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        # print('Setting PWM frequency to {0} Hz'.format(freq_hz))
        # print('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        # print('Final pre-scale: {0}'.format(prescale))
        i2c.write(self.address, bytearray([MODE1])) # write register we want to read from first
        oldmode = i2c.read(self.address, 1)
        oldmode = ustruct.unpack('<H', oldmode)[0]
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        i2c.write(self.address, bytearray([MODE1, newmode]))  # go to sleep
        i2c.write(self.address, bytearray([PRESCALE, prescale]))
        i2c.write(self.address, bytearray([MODE1, oldmode]))
        sleep(5)
        i2c.write(self.address, bytearray([MODE1, oldmode | 0x80]))

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        if on is None or off is None:
            i2c.write(self.address, bytearray([LED0_ON_L+4*channel])) # write register we want to read from first
            data = i2c.read(self.address, 4)
            return ustruct.unpack('<HH', data)
        i2c.write(self.address, bytearray([LED0_ON_L+4*channel, on & 0xFF]))
        i2c.write(self.address, bytearray([LED0_ON_H+4*channel, on >> 8]))
        i2c.write(self.address, bytearray([LED0_OFF_L+4*channel, off & 0xFF]))
        i2c.write(self.address, bytearray([LED0_OFF_H+4*channel, off >> 8]))

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        i2c.write(self.address, bytearray([ALL_LED_ON_L, on & 0xFF]))
        i2c.write(self.address, bytearray([ALL_LED_ON_H, on >> 8]))
        i2c.write(self.address, bytearray([ALL_LED_OFF_L, off & 0xFF]))
        i2c.write(self.address, bytearray([ALL_LED_OFF_H, off >> 8]))

    def duty(self, index, value=None, invert=False):
        if value is None:
            pwm = self.set_pwm(index)
            if pwm == (0, 4096):
                value = 0
            elif pwm == (4096, 0):
                value = 4095
            value = pwm[1]
            if invert:
                value = 4095 - value
            return value
        if not 0 <= value <= 4095:
            raise ValueError("Out of range")
        if invert:
            value = 4095 - value
        if value == 0:
            self.set_pwm(index, 0, 4096)
        elif value == 4095:
            self.set_pwm(index, 4096, 0)
        else:
            self.set_pwm(index, 0, value)
