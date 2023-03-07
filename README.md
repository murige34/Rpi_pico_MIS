# Raspberry Pi Pico MIS
S pomočjo Raspberry Pi Pico razvojne plošče sem ustvaril pripomoček za pomoč pri vnosu ponavljajočih se podatkov v Meroslovni informacijski sistem.

### Opozorilo: Ne odgovarjam za nikakršno neposredno ali posredno škodo ali neprijetnosti, ki bi lahko nastale zaradi uporabe razvojne plošče ali objavljenih programov.

# Navodila za uporabo
### Če windows javlja napako, da je disk pokvarjen stori [sledeče](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython):
1. odklopi USB kabel iz računalnika
2. tišči tipko na ploščici (BOOTSEL) in priklopi usb kabel na računalnik (prikaže se disk z imenom RPI-RP2)
3. skopiraj 'flash_nuke.uf2' na 'RPI-RP2'
4. počakaš, da se zresetira
5. skopiraj 'adafruit-circuitpython-raspberry_pi_pico-en_US-8.0.3.uf2' na 'RPI-RP2', zadnjo verzijo si lahko preneseš s spletne strani: https://circuitpython.org/board/raspberry_pi_pico/
6. počakaš, da se resetira
7. pobrišeš code.py iz 'CIRCUITPY'
8. skopiraj vsebino mape 'Skopiraj na CIRCUITPY' na 'CIRCUITPY'

### Uporaba v programu MIS:
1. v beležnici odpri CIRCUITPY\Nastavitve.json (pritisk na tipko T2)
2. spremeniš vrednosti, ki jih želiš vnesti
3. Shraniš z Ctrl+S in zapreš beležnico
4. Počakaš, da zelena ledica na ploščici pomežikne
5. V MISu odpreš delovni nalog, ki ga želiš izpolniti in pritisneš tipko za vnos T1

#### Vnos datuma s tipko (ni v uporabi):
1. pritisneš tipko za vnos datuma
-. odpre se cmd (črno komandno okno)
-. požene se skripta, ki shrani trenutni čas na 'CIRCUITPY'
2. Počakaš, da zelena ledica dvakrat utripne (cca 10s)
3. Šele ko zelena ledica gori lahko pritisneš tipko za vnos v MIS
4. Da se uporabi ta vrednost, mora biti v Nastavitve.json: "Datum"     : "",


### Razvil sem svojo knjižnico z končnico .py in bi jo rad prevedel v *.mpy:
1. S strani https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/ preneseš križni prevajalnik (ang. cross compiler), glede na sistem, ki ga uporabljaš.
> Npr. če uporabljaš PC z 64-bitnimi Windowsi in si na ploščico prenecel CircuitPython verzije 7.2.0 izbereš mpy-cross.static-x64-windows-7.2.0-alpha.2.exe
2. V isto mapo, kamor si shranil prenesen program shraniš tudi svojo datoteko s končnico .py
3. Odpreš pozivno okno (CMD).
> To najlažje storiš tako, da na tipkovnici pritisneš **Windows + R** vneseš **cmd** in pritisneš **Enter** ali klikneš **V redu**
4. Z ukazom cd se premakneš v mapo, kamor si shranil prevajalnik in *.py datoteko
> Npr. se želimo premakniti v mapo prenosi vnesemo **cd Downloads** ali celotno pot, do katere pridemo, če v  Raziskovalcu odpremo željeno mapo **cd C:\Users\urige\Downloads**
5. Poženemo prevajalnik tako, da vnesemo **polno_ime_prenesenega_prevajalnika moj_program.py** in potrdimo vnos z Enter. V kolikor program ne javi napake smo uspešno prevedli naš program in nas že čaka v naši mapi z končnico .mpy
> Npr. če imamo program test.py in smo prenesli prevajalnik iz primera pod točko 1 vnesemo: **mpy-cross.static-x64-windows-7.2.0-alpha.2.exe test.py**

### Uporabne povezave:
- Adafruit Getting Started tutorial: https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython
- Zadnja verzija CircuitPythona: https://circuitpython.org/board/raspberry_pi_pico/
- Circuitpython REPL navodila: https://learn.adafruit.com/welcome-to-circuitpython/the-repl
- Raspberry Pi Pico datasheet: https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
- Raspberry Pi Pico C/C++ getting started: https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf
- Priporočeni **IDE**ji za začetnike:
  - CircuitPython - Mu: https://codewith.mu/en/download
  - MicroPython - Thonny: https://thonny.org/
  - C/C++ - Arduino: https://www.arduino.cc/en/software
  - C/C++ - Visual Studio Code: https://code.visualstudio.com/
