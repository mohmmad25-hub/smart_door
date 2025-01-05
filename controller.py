from pyfirmata import Arduino, SERVO, util, INPUT, OUTPUT
import time
# import board
# import digitalio
# import adafruit_character_lcd.character_lcd as characterlcd

# Arduino setup
PORT = "COM3"  # Replace with your Arduino port
servo_pin = 4  # Servo pin
pushbutton_pin = 2  # Pushbutton pin
green_led = 7
red_led = 8



board = Arduino(PORT)
board.digital[servo_pin].mode = SERVO
board.digital[green_led].mode = OUTPUT
board.digital[red_led].mode = OUTPUT


# Start PyFirmata iterator to enable pin reading
it = util.Iterator(board)
it.start()

# Set the pushbutton pin as input
board.digital[pushbutton_pin].mode = INPUT

# Function to rotate the servo motor
def rotateServo(pin, angle):
    board.digital[pin].write(angle)

# Function to automate door control
def doorAutomate(val):
    if val == 0:
        rotateServo(servo_pin, 180)  # Open the door
    elif val == 1:
        rotateServo(servo_pin, 0)  # Close the door

# Function to read the pushbutton state
def readButtonState():
    state = board.digital[pushbutton_pin].read()
    if state is None:
        return False
    return state == 1  # Return True if the button is pressed

# Placeholder function to simulate LCD functionality
# def write_lcd(message):
#     # Replace with actual LCD control logic if needed
#     lcd.clear()
#     lcd.message(message)

def controlLED(green_on, red_on):
    board.digital[green_led].write(1 if green_on else 0)  # Turn green LED on/off
    board.digital[red_led].write(1 if red_on else 0)  # Turn red LED on/off

