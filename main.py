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
