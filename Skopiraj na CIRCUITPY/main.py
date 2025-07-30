# CircuitPython looks for a code file on the board to run. 
# There are four options: code.txt, code.py, main.txt and main.py.  <-- code.py = recommended
# CircuitPython looks for those files, in that order, and then runs the first one it finds.

import board
import time
import usb_hid
import json
import storage
import os
import usb_cdc
import adafruit_datetime
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_slv import KeyboardLayout
from keycode_win_slv import Keycode

# initialize serial communication
COM_PORT = "COM4"
serial = usb_cdc.data
serial.timeout = 0.005
serial.reset_input_buffer()
serial.reset_output_buffer()
time.sleep(0.2)

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


# lahko uporabiš čas zadnje spremembe datoteke Nastavitve.json
if nastavitve["Datum"].replace(" ", "") == "d":
    try:
        datum = adafruit_datetime.date.fromtimestamp(os.stat("Nastavitve.json")[-1])
        nastavitve["Datum"] = str(datum.day) + "." + str(datum.month) + "." + str(datum.year)
    except:
        nastavitve["Datum"] = ""
        

print("Nastavitve:\n" + str(nastavitve))

# function to send N times key press
def keyboard_send_N(control_key, key, N=1):
    for i in range(N):
        keyboard.press(control_key, key)
        keyboard.release_all()

def read_serial():
    global nastavitve
    time.sleep(0.02)
    in_data = bytearray()
    while serial.in_waiting > 0:
        in_data += serial.read(1)     
        
    in_data = in_data.decode('utf-8')
    
    if len(in_data) > 0:
        if in_data.find('{') >= 0 and in_data.rfind('}') >= 0:
            #to so nastavitve v .json obliki
            in_data = in_data[in_data.find('{') : in_data.rfind('}')+1]
            nastavitve = json.loads(in_data)
            
            print("Nove nastavitve:\n" + str(nastavitve))
        elif in_data.find('[') >= 0 and in_data.rfind(']') >= 0:
            # pričakovan datum oblike: [sre. 30. 07. 2025]
            if in_data.count(".") == 3:
                in_data = in_data[in_data.find('.') + 1 : in_data.rfind(']')].replace(" ", "")
            else:
                in_data = in_data[in_data.find('[') + 1 : in_data.rfind(']')].replace(" ", "")
            
            if nastavitve["Datum"].replace(" ", "") == "d":
                nastavitve["Datum"] = in_data
                print("Nov datum: " + in_data)
        else:
            serial.write(bytearray("Preveri podatke!\n\r"))
    del in_data

while 1:
    # pricakovano podatke prilepiš iz beležnice in jih ne prepisuješ ročno (timeout)
    if serial.in_waiting > 0:
        read_serial()
    
    # define what happens when button_1 is pressed: Vnos v MIS
    if button_1.value == 0:
        led.value = 0
        led_1.value = 1
        
        # kopiranje starih opomb preden odkleneš nalog za urejanje
        if nastavitve["OpombeCopy"].replace(" ", "").lower() == "d":
            keyboard_send_N(0, Keycode.ALT)
            keyboard_send_N(0, Keycode.RIGHT_ARROW, 2)
            #keyboard_send_N(0, Keycode.DOWN_ARROW)
            keyboard_send_N(0, Keycode.ENTER)
            kbd.write("p")
            #time.sleep(0.4)
            keyboard_send_N(Keycode.CONTROL, Keycode.C)
            keyboard_send_N(Keycode.ALT, Keycode.F4)
            #time.sleep(0.4)
            keyboard_send_N(Keycode.CONTROL, Keycode.V)
        else:
            # opombe lahko pišeš že preden odkleneš DN za urejanje
            kbd.write(nastavitve["Opombe"])
        
        
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

        # keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB, 6 + 4)
        kbd.write("\t")

        # Vnos testnih instrumentov
        if len(nastavitve["Test_inst1"].replace(" ", "")) > 0:
            keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB, 16 + 7)
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
                    #keyboard.release_all()
                    
                    #keyboard.press(Keycode.TAB)
                    keyboard_send_N(0, Keycode.TAB, 4)
                    if len(nastavitve["Test_inst4"].replace(" ", "")) > 0:
                        # vneses 4. instrument
                        kbd.write(nastavitve["Test_inst4"].replace(" ", ""))
                        keyboard.press(Keycode.DOWN_ARROW)
                        keyboard.release_all()
                    else:
                        # pobrises 4. instrument
                        keyboard.press(Keycode.BACKSPACE)
                        keyboard.release_all()
                    
                    keyboard_send_N(Keycode.LEFT_SHIFT, Keycode.TAB, 4)
                    
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

            keyboard_send_N(0, Keycode.TAB, 16 + 7)
            
        keyboard_send_N(0, Keycode.TAB, 8)
        keyboard_send_N(0, Keycode.DOWN_ARROW)

        Num_pts_Etalon = len(nastavitve["Etalon_val"].split())
        Num_pts_UUT = len(nastavitve["UUT_val"].split())
        Num_pts_Komentar = len(nastavitve["Komentar"].split())

        Num_pts_Rocno = 0
        if len(nastavitve["St_vrstic"].replace(" ", "")) > 0 and len(nastavitve["St_vrstic"].replace(" ", "")) <= 2 :
            try:
                Num_pts_Rocno = int(nastavitve["St_vrstic"])
            except:
                Num_pts_Rocno = 0

        # Je potrebno spremeniti stevilo vrstic?
        Num_pts_max = max(Num_pts_Etalon, Num_pts_UUT, Num_pts_Komentar, Num_pts_Rocno)
        if Num_pts_max > 0 and Num_pts_max < 100:
            # Pobrises vse vrstice (pricakujes jih najvec 10)
            for x in range(10):
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

        if Num_pts_Komentar > 0:
            # vnos komentarjev
            keyboard_send_N(0, Keycode.RIGHT_ARROW, 4)
            for x in nastavitve["Komentar"].split():
                keyboard.press(0, Keycode.DOWN_ARROW)
                kbd.write(x)

            keyboard_send_N(0, Keycode.UP_ARROW, Num_pts_Komentar)
            keyboard_send_N(0, Keycode.LEFT_ARROW, 4)
        keyboard.release_all()
        
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
        
    # define what happens when button_2 is pressed: Odpiranje CIRCUITPY/Nastavitve.json - preko raziskovalca (manj zanesljivo a hitreje)
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
        
    # define what happens when button_3 is pressed: Odpiranje CIRCUITPY/Nastavitve.json - preko cmd
    if button_3.value == 0:
        led.value = 0
        led_3.value = 1
        
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()

        time.sleep(0.3)
        kbd.write("cmd\n")
        time.sleep(0.5)
        # poisces crko pogona z imenom "CIRCUITPY"
        kbd.write("for /f %D in ('wmic volume get DriveLetter^, Label ^| find \"CIRCUITPY\"') do set piusb=%D\n")
        time.sleep(0.9)

        kbd.write("%piusb%\n")
        time.sleep(0.1)
        kbd.write("Nastavitve.json\n")
        
        led_3.value = 0

    # define what happens when button_4 is pressed: Create Nastavitve.json na računalniku
    if button_4.value == 0:
        led.value = 0
        led_4.value = 1
        
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()
        
        time.sleep(0.4)
        kbd.write("notepad desktop/Nastavitve.json\n")
        time.sleep(0.6)
        kbd.write("\n\n")
        keyboard.press(Keycode.CONTROL, Keycode.A)
        keyboard.release_all()
        keyboard.press(Keycode.DELETE)
        keyboard.release_all()
        
        kbd.write("{\n")
        kbd.write('\t"Temp_val"   : "",\n')
        kbd.write('\t"Temp_inst"  : "",\n')
        kbd.write('\t"Vlaga_val"  : "",\n')
        kbd.write('\t"Vlaga_inst" : "",\n')
        kbd.write('\t"Tlak_val"   : "/",\n')
        kbd.write('\t"Tlak_inst"  : "/",\n')        
        kbd.write('\t"Datum"      : "d",\n')        
        kbd.write('\n')
        kbd.write('\t"Opombe"     : "",\n')
        kbd.write('\t"OpombeCopy" : "d",\n')
        kbd.write('\n')
        kbd.write('\t"Test_inst1" : "",\n')
        kbd.write('\t"Test_inst2" : "",\n')
        kbd.write('\t"Test_inst3" : "",\n')
        kbd.write('\t"Test_inst4" : "",\n')
        kbd.write('\n')
        kbd.write('\t"St_vrstic"  : "",\n')
        kbd.write('\n')
        kbd.write('\t"Etalon_val" : "",\n')
        kbd.write('\t"UUT_val"    : "",\n')
        kbd.write('\t"Komentar"   : ""\n')
        kbd.write("}")
        
        #keyboard.press(Keycode.CONTROL, Keycode.S)
        #keyboard.release_all()
        
        led_4.value = 0
        
    # define what happens when button_5 is pressed: Odpre Nastavitve.json iz računalnika
    if button_5.value == 0:
        led.value = 0
        led_5.value = 1
        
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()
        
        time.sleep(0.3)
        kbd.write("notepad desktop/Nastavitve.json\n")
        
        led_5.value = 0
        
    # define what happens when button_6 is pressed: Pošlje Nastavitve.json iz računalnika na ploščico preko COM porta
    if button_6.value == 0:
        led.value = 0
        led_6.value = 1
        
        print("Nastavitve:")
        print(nastavitve)
        
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()

        time.sleep(0.3)
        kbd.write("cmd\n")
        time.sleep(0.5)
        
        # plink.exe je cmd interface od Puttyja (docs: https://documentation.help/putty/plink-usage.html )
        # pošlje nastavitve
        kbd.write("plink.exe -serial " + COM_PORT + " -sercfg 9600,8,n,1,N -batch < desktop/Nastavitve.json\n")
        time.sleep(0.2)
        read_serial()
        keyboard.press(Keycode.CONTROL, Keycode.C)
        keyboard.release_all()
        # pošlje datum
        kbd.write("echo [%date%] | plink.exe -serial " + COM_PORT + " -sercfg 9600,8,n,1,N -batch\n")
        time.sleep(0.2)
        read_serial()
        keyboard.press(Keycode.CONTROL, Keycode.C)
        keyboard.release_all()
        kbd.write("exit\n")
        
        led_6.value = 0
        
    # define what happens when button_7 is pressed:
    if button_7.value == 0:
        # write date to date.txt file in cmd
        led.value = 0
        led_7.value = 1
        keyboard.press(Keycode.WINDOWS, Keycode.R)
        keyboard.release_all()

        time.sleep(0.3)
        kbd.write("cmd\n")
        time.sleep(0.5)
        # poisces crko pogona z imenom "CIRCUITPY"
        kbd.write("for /f %D in ('wmic volume get DriveLetter^, Label ^| find \"CIRCUITPY\"') do set piusb=%D\n")
        time.sleep(0.5)
        # shranis datum (format: "pon. 07.03.2022 ") v date.txt
        kbd.write("cmd /c date/t > %piusb%\date.txt & exit\n")
        
        # Ta vrstica se nikoli ne izvrši, ker se po shranjevanju v katerokoli dateteko na Circuitpy ploščica resetira...
        led_7.value = 1

    led.value = 1