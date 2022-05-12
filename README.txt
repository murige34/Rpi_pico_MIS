Èe windows javlja napako, da je disk pokvarjen stori sledeèe:
1. odklopi USB iz raèunalnika
2. tišèi tipko na plošèici in priklopi usb na raèunalnik (prikaže se RPI-RP2)
3. skopiraj 'flash_nuke.uf2' na 'RPI-RP2'
-. poèakaš, da se zresetira
4. skopiraj 'adafruit-circuitpython-raspberry_pi_pico-en_US-7.2.0.uf2' na 'RPI-RP2'
-. poèakaš, da se zresetira
5. pobrišeš code.py iz 'CIRCUITPY'
6. skopiraj vsebino mape 'Skopiraj na CIRCUITPY' na 'CIRCUITPY'

------------------------------------------------------------------------------------

Uporaba za MIS:
1. v beležnici odpri CIRCUITPY\Nastavitve.json
2. spremeniš vrednosti, ki jih želiš vnesti
3. Shraniš z Ctrl+S in zapreš beležnico
4. Poèakaš, da zelena ledica na plošèici pomežikne
5. V MISu se postaviš na polje za vnos temperature in
   pritisneš tipko za vnos

Vnos datuma s tipko:
1. pritisneš tipko za vnos datuma
-. odpre se cmd (èrno komandno okno)
-. požene se skripta, ki shrani trenutni èas na 'CIRCUITPY'
2. Poèakaš, da zelena ledica dvakrat utripne (cca 10s)
3. Šele ko zelena ledica gori lahko pritisneš tipko za vnos v MIS
4. Da se uporabi ta vrednost, mora biti v Nastavitve.json:
   "Datum"     : "",

------------------------------------------------------------------------------------

Komentar verzij:
v01: Osnovna verzija vnosa v MIS
v03: MIS - Dodan vnos vrednosti etalona
v03: MIS - Dodan vrednosti merjenca (UUT)