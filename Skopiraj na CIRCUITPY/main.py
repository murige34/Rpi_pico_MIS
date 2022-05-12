import board
import time
import usb_hid
import json
import storage
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_slv import KeyboardLayout
from keycode_win_slv import Keycode

# settup I/O
# initialize onboard LED as output
led = DigitalInOut(board.LED)
led.switch_to_output()

# initialize button_1 as input (active low)
button_1 = DigitalInOut(board.GP21)
button_1.direction = Direction.INPUT
button_1.pull = Pull.UP

# initialize button_2 as input (active low)
button_2 = DigitalInOut(board.GP20)
button_2.direction = Direction.INPUT
button_2.pull = Pull.UP

# initialize keyboard
keyboard = Keyboard(usb_hid.devices)
kbd = KeyboardLayout(keyboard)

# read settings from json
storage.getmount("/")
file = open("Nastavitve.json", "r")

nastavitve = json.loads(file.read())
file.close()


if(len(nastavitve['Datum']) < 6):
    try:
        # read date from date.txt file
        file = open("date.txt", "r")
        a = file.read()
        file.close()

        if(len(a) >= 8):
            """
            a = a[re.search('\d', a).start():]
            a = a.replace(" ", "")
            a = a.replace("\n","")
            """
            idx_start = 0
            idx_end = 0
            i = 0
            
            for char in a:
                if(char.isdigit()):
                    idx_end = i+1
                    if(idx_start == 0):
                        idx_start = i
                i = i + 1

            a = a[idx_start: idx_end]
            a = a.replace(" ", "")
            
            
        nastavitve['Datum'] = a
    except:
        nastavitve['Datum'] = ""


# function to send N times key press
def keyboard_send_N(control_key, key, N):
    for i in range(N):
        keyboard.press(control_key, key)
        keyboard.release_all()

# wrile led low/high
while 1:
    # define what happens when button_1 is pressed
    if(button_1.value == 0):
        led.value = 0
        kbd.write(nastavitve['Temp_val'])
        kbd.write("\t")
        kbd.write(nastavitve['Temp_inst'])
        kbd.write("\t")
        kbd.write(nastavitve['Vlaga_val'])
        kbd.write("\t")
        kbd.write(nastavitve['Vlaga_inst'])
        kbd.write("\t")
        kbd.write(nastavitve['Tlak_val'])
        kbd.write("\t")
        kbd.write(nastavitve['Tlak_inst'])
        kbd.write("\t")
        kbd.write(nastavitve['Datum'])

        keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB, 6+4)

        kbd.write(nastavitve['Opombe'])

        if(len(nastavitve['Test_inst1'].replace(' ', '')) > 0):
            keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB, 13)
            # vneses 1. instrument
            kbd.write(nastavitve['Test_inst1'].replace(' ', ''))
            keyboard.press(Keycode.DOWN_ARROW)
            
            keyboard.press(Keycode.TAB)
            if(len(nastavitve['Test_inst2'].replace(' ', '')) > 0):
                # vneses 2. instrument
                kbd.write(nastavitve['Test_inst2'].replace(' ', ''))
                keyboard.press(Keycode.DOWN_ARROW)
                
                keyboard.press(Keycode.TAB)
                if(len(nastavitve['Test_inst3'].replace(' ', '')) > 0):
                    # vneses 3. instrument
                    kbd.write(nastavitve['Test_inst3'].replace(' ', ''))
                    keyboard.press(Keycode.DOWN_ARROW)
                    keyboard.release_all()
                else:
                    # pobrises 3. instrument
                    keyboard.press(Keycode.BACKSPACE)
                    keyboard.release_all()
                keyboard.press(Keycode.LEFT_SHIFT, Keycode.TAB)
                keyboard.release_all()
                
            else:
                # pobrises 2. in 3. instrument
                keyboard.press(Keycode.BACKSPACE)
                keyboard.release_all()
                keyboard.press(Keycode.TAB)
                keyboard.press(Keycode.BACKSPACE)
                keyboard.release_all()
                keyboard.press(Keycode.LEFT_SHIFT, Keycode.TAB)
                keyboard.release_all()
            
            keyboard.press(Keycode.LEFT_SHIFT, Keycode.TAB)
            keyboard.release_all()

            keyboard_send_N(0, Keycode.TAB, 13)

        keyboard_send_N(0, Keycode.TAB, 4 + 8)
        keyboard.press(0, Keycode.DOWN_ARROW)
        keyboard.release_all()
        
        Num_pts_Etalon = len(nastavitve['Etalon_val'].split())
        Num_pts_UUT    = len(nastavitve['UUT_val'].split())
        
        
        if(Num_pts_Etalon > 0):
            # vnos vrednosti etalona
            for x in nastavitve['Etalon_val'].split():
                keyboard.press(0, Keycode.DOWN_ARROW)
                kbd.write(x)
                
            keyboard_send_N(0, Keycode.UP_ARROW, Num_pts_Etalon - 1)
            keyboard.press(0, Keycode.RIGHT_ARROW)
        else:
            keyboard.press(0, Keycode.DOWN_ARROW)
        keyboard.release_all()
        
        if(Num_pts_UUT > 0):
            if(Num_pts_Etalon <= 0):
                keyboard.press(0, Keycode.RIGHT_ARROW)
                keyboard.release_all()
            keyboard.press(0, Keycode.UP_ARROW)
            keyboard.release_all()
            # vnos vrednosti merjenca
            for x in nastavitve['UUT_val'].split():
                keyboard.press(0, Keycode.DOWN_ARROW)
                kbd.write(x)
            
            if(Num_pts_Etalon > 0):
                keyboard.press(0, Keycode.ENTER)
            else:
                keyboard_send_N(0, Keycode.UP_ARROW, Num_pts_UUT - 1)
                keyboard.press(0, Keycode.LEFT_ARROW)
        keyboard.release_all()
        
        
    if(button_2.value == 0):
        led.value = 0
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()
        
        time.sleep(0.3)
        kbd.write("cmd\n")
        time.sleep(0.5)
        kbd.write("for /f %D in ('wmic volume get DriveLetter^, Label ^| find \"CIRCUITPY\"') do set piusb=%D\n")
        time.sleep(0.5)
        kbd.write("cmd /c date/t > %piusb%\date.txt\n")
        time.sleep(0.5)
        kbd.write("exit\n")
        time.sleep(0.2)
          
    led.value = 1
    time.sleep(0.2)
