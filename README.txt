�e windows javlja napako, da je disk pokvarjen stori slede�e:
1. odklopi USB iz ra�unalnika
2. ti��i tipko na plo��ici in priklopi usb na ra�unalnik (prika�e se RPI-RP2)
3. skopiraj 'flash_nuke.uf2' na 'RPI-RP2'
-. po�aka�, da se zresetira
4. skopiraj 'adafruit-circuitpython-raspberry_pi_pico-en_US-7.2.0.uf2' na 'RPI-RP2'
-. po�aka�, da se zresetira
5. pobri�e� code.py iz 'CIRCUITPY'
6. skopiraj vsebino mape 'Skopiraj na CIRCUITPY' na 'CIRCUITPY'

------------------------------------------------------------------------------------

Uporaba za MIS:
1. v bele�nici odpri CIRCUITPY\Nastavitve.json
2. spremeni� vrednosti, ki jih �eli� vnesti
3. Shrani� z Ctrl+S in zapre� bele�nico
4. Po�aka�, da zelena ledica na plo��ici pome�ikne
5. V MISu se postavi� na polje za vnos temperature in
   pritisne� tipko za vnos

Vnos datuma s tipko:
1. pritisne� tipko za vnos datuma
-. odpre se cmd (�rno komandno okno)
-. po�ene se skripta, ki shrani trenutni �as na 'CIRCUITPY'
2. Po�aka�, da zelena ledica dvakrat utripne (cca 10s)
3. �ele ko zelena ledica gori lahko pritisne� tipko za vnos v MIS
4. Da se uporabi ta vrednost, mora biti v Nastavitve.json:
   "Datum"     : "",

------------------------------------------------------------------------------------

Komentar verzij:
v01: Osnovna verzija vnosa v MIS
v03: MIS - Dodan vnos vrednosti etalona
v03: MIS - Dodan vrednosti merjenca (UUT)