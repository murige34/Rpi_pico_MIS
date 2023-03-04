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

# initialize led_1 as output
led_1 = DigitalInOut(board.GP15)
led_1.switch_to_output()
# initialize led_2 as output
led_2 = DigitalInOut(board.GP14)
led_2.switch_to_output()
# initialize led_3 as output
led_3 = DigitalInOut(board.GP13)
led_3.switch_to_output()
# initialize led_4 as output
led_4 = DigitalInOut(board.GP12)
led_4.switch_to_output()
# initialize led_5 as output
led_5 = DigitalInOut(board.GP9)
led_5.switch_to_output()
# initialize led_6 as output
led_6 = DigitalInOut(board.GP5)
led_6.switch_to_output()
# initialize led_7 as output
led_7 = DigitalInOut(board.GP2)
led_7.switch_to_output()

# initialize button_1 as input (active low)
button_1 = DigitalInOut(board.GP19)
button_1.direction = Direction.INPUT
button_1.pull = Pull.UP
# initialize button_2 as input (active low)
button_2 = DigitalInOut(board.GP20)
button_2.direction = Direction.INPUT
button_2.pull = Pull.UP
# initialize button_3 as input (active low)
button_3 = DigitalInOut(board.GP21)
button_3.direction = Direction.INPUT
button_3.pull = Pull.UP
# initialize button_4 as input (active low)
button_4 = DigitalInOut(board.GP22)
button_4.direction = Direction.INPUT
button_4.pull = Pull.UP
# initialize button_5 as input (active low)
button_5 = DigitalInOut(board.GP26)
button_5.direction = Direction.INPUT
button_5.pull = Pull.UP
# initialize button_6 as input (active low)
button_6 = DigitalInOut(board.GP27)
button_6.direction = Direction.INPUT
button_6.pull = Pull.UP
# initialize button_7 as input (active low)
button_7 = DigitalInOut(board.GP28)
button_7.direction = Direction.INPUT
button_7.pull = Pull.UP

# initialize keyboard
keyboard = Keyboard(usb_hid.devices)
kbd = KeyboardLayout(keyboard)

# read settings from json
storage.getmount("/")
file = open("Nastavitve.json", "r")

nastavitve = json.loads(file.read())
file.close()


if len(nastavitve["Datum"]) < 6:
    try:
        # read date from date.txt file
        file = open("date.txt", "r")
        a = file.read()
        file.close()

        if len(a.replace(" ", "")) >= 8:
            a = a.replace(" ", "")
            a = a.split("-")[0]

        else:
            a = ""

        nastavitve["Datum"] = a
    except:
        nastavitve["Datum"] = ""


# function to send N times key press
def keyboard_send_N(control_key, key, N=1):
    for i in range(N):
        keyboard.press(control_key, key)
        keyboard.release_all()


# wrile led low/high
while 1:
    # define what happens when button_1 is pressed
    if button_1.value == 0:
        led.value = 0
        led_1.value = 1
        # Spremembe / spremeni <- odklenes obrazec za urejanje
        keyboard_send_N(0, Keycode.ALT)
        keyboard_send_N(0, Keycode.ENTER, 2)

        # Vnos klimatskih pogojev
        kbd.write(nastavitve["Temp_val"])
        kbd.write("\t")
        kbd.write(nastavitve["Temp_inst"])
        kbd.write("\t")
        kbd.write(nastavitve["Vlaga_val"])
        kbd.write("\t")
        kbd.write(nastavitve["Vlaga_inst"])
        kbd.write("\t")
        kbd.write(nastavitve["Tlak_val"])
        kbd.write("\t")
        kbd.write(nastavitve["Tlak_inst"])
        kbd.write("\t")
        kbd.write(nastavitve["Datum"])

        keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB, 6 + 4)

        kbd.write(nastavitve["Opombe"])


        # Vnos testnih instrumentov
        if len(nastavitve["Test_inst1"].replace(" ", "")) > 0:
            keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB, 13)
            # vneses 1. instrument
            kbd.write(nastavitve["Test_inst1"].replace(" ", ""))
            keyboard.press(Keycode.DOWN_ARROW)

            keyboard.press(Keycode.TAB)
            if len(nastavitve["Test_inst2"].replace(" ", "")) > 0:
                # vneses 2. instrument
                kbd.write(nastavitve["Test_inst2"].replace(" ", ""))
                keyboard.press(Keycode.DOWN_ARROW)

                keyboard.press(Keycode.TAB)
                if len(nastavitve["Test_inst3"].replace(" ", "")) > 0:
                    # vneses 3. instrument
                    kbd.write(nastavitve["Test_inst3"].replace(" ", ""))
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

            keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB)

            keyboard_send_N(0, Keycode.TAB, 13)

        keyboard_send_N(0, Keycode.TAB, 4 + 8)
        keyboard_send_N(0, Keycode.DOWN_ARROW)

        Num_pts_Etalon = len(nastavitve["Etalon_val"].split())
        Num_pts_UUT = len(nastavitve["UUT_val"].split())

        Num_pts_Rocno = 0
        if len(nastavitve["St_vrstic"].replace(" ", "")) > 0 and len(nastavitve["St_vrstic"].replace(" ", "")) <= 2 :
            try:
                Num_pts_Rocno = int(nastavitve["St_vrstic"])
            except:
                Num_pts_Rocno = 0

        # Je potrebno spremeniti stevilo vrstic?
        Num_pts_max = max(Num_pts_Etalon, Num_pts_UUT, Num_pts_Rocno)
        if Num_pts_max > 0 and Num_pts_max < 100:
            # Pobrises vse vrstice (pricakujes jih najvec 8)
            for x in range(8):
                keyboard_send_N(0, Keycode.ALT)
                keyboard_send_N(0, Keycode.RIGHT_ARROW)
                keyboard_send_N(0, Keycode.ENTER)
                keyboard_send_N(0, Keycode.DOWN_ARROW)
                keyboard_send_N(0, Keycode.ENTER)

            # Dodas zeljeno stevilo vrstic
            for x in range(Num_pts_max):
                keyboard_send_N(0, Keycode.ALT)
                keyboard_send_N(0, Keycode.RIGHT_ARROW)
                keyboard_send_N(0, Keycode.ENTER, 2)

        if Num_pts_Etalon > 0:
            # vnos vrednosti etalona
            for x in nastavitve["Etalon_val"].split():
                keyboard.press(0, Keycode.DOWN_ARROW)
                kbd.write(x)

            keyboard_send_N(0, Keycode.UP_ARROW, Num_pts_Etalon - 1)
            keyboard.press(0, Keycode.RIGHT_ARROW)
        else:
            keyboard.press(0, Keycode.DOWN_ARROW)
        keyboard.release_all()

        if Num_pts_UUT > 0:
            if Num_pts_Etalon <= 0:
                keyboard_send_N(0, Keycode.RIGHT_ARROW)
            keyboard_send_N(0, Keycode.UP_ARROW)
            # vnos vrednosti merjenca
            for x in nastavitve["UUT_val"].split():
                keyboard.press(0, Keycode.DOWN_ARROW)
                kbd.write(x)

            if Num_pts_Etalon > 0:
                keyboard.press(0, Keycode.ENTER)
            else:
                keyboard_send_N(0, Keycode.UP_ARROW, Num_pts_UUT - 1)
                keyboard.press(0, Keycode.LEFT_ARROW)
        keyboard.release_all()
        led_1.value = 0

    if button_2.value == 0:
        led.value = 0
        led_2.value = 1
        keyboard.press(Keycode.WINDOWS, Keycode.E)
        keyboard.release_all()
        time.sleep(1.2)
        kbd.write("c")
        time.sleep(0.2)
        kbd.write("\n")
        time.sleep(0.5)
        kbd.write("n")
        time.sleep(0.2)
        kbd.write("\n")
        led_2.value = 0

    if 0:
        led.value = 0
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()

        time.sleep(0.3)
        kbd.write("cmd\n")
        time.sleep(0.5)
        # poisces crko pogona z imenom "CIRCUITPY"
        kbd.write("for /f %D in ('wmic volume get DriveLetter^, Label ^| find \"CIRCUITPY\"') do set piusb=%D\n")
        time.sleep(0.7)

        kbd.write("%piusb%\n")
        time.sleep(0.1)
        kbd.write("Nastavitve.json\n")

    if 0:
        led.value = 0
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()

        time.sleep(0.3)
        kbd.write("cmd\n")
        time.sleep(0.5)
        # poisces crko pogona z imenom "CIRCUITPY"
        kbd.write("for /f %D in ('wmic volume get DriveLetter^, Label ^| find \"CIRCUITPY\"') do set piusb=%D\n")
        time.sleep(0.7)
        # shranis datum (format: "pon. 07.03.2022 ") v date.txt
        # kbd.write("cmd /c date/t > %piusb%\date.txt\n")
        # time.sleep(0.5)

        kbd.write("for /f \"tokens=2\" %i in ('date /t') do set mydate=%i\n")
        time.sleep(0.5)
        kbd.write("set mytime=%time%\n")
        time.sleep(0.5)
        kbd.write("echo %mydate%-%mytime% > %piusb%\date.txt\n")
        time.sleep(0.5)
        kbd.write("exit\n")
        time.sleep(0.2)

    led.value = 1
    time.sleep(0.2)
