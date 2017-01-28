# Microbit Python Driver for PCA9685

This is a simple python class for using the PCA9685 16-Channel 12-bit PWM/Servo Driver - I2C interface (https://www.adafruit.com/product/815).

#### Using the driver

There is an example of how to use the driver to control a server in main.py. The example sets the servo at channel 0 to it's minimum value, sleeps for 1 second, then set's channel 0 to it's maximum value:
```
pwm.set_pwm(0, 0, servo_min)
sleep(1000)
pwm.set_pwm(0, 0, servo_max)
sleep(1000)
```
If you do not know how to load additional files onto your microbit (so main.py can read the PCA9685 driver from PCA9685.py) read https://microbit-playground.co.uk/howto/add-python-module-microbit-micropython.

#### Acknowledgement

This driver is adapted from Tony DiCola's driver at https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/Adafruit_PCA9685/PCA9685.py

#### Contributing

I am an experienced software developer but very new to Pythong and I2C. There are bound to be many improvements that could be made to the basic code as well as new helper classes (a servo class is the next plan). If you wish to contribute feel free to send PR's and chat to me on http://microbit-community.slack.com username 'MicroMonsters'.

#### Finally

Don't forget to check our youtube channel http://youtube.com/c/micromonsters to find inspiration using the microbit to code with your children.