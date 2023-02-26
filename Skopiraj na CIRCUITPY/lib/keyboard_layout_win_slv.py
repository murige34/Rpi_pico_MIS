# SPDX-FileCopyrightText: 2021 Martin Urigelj
#
# I modified code from adafruit & neradoc for Slovenian keyboard
#
# SPDX-License-Identifier: MIT

"""
`keyboard_layout_win_slv.KeyboardLayout`
=======================================================

* Author(s): Martin Urigelj
"""

from keyboard_layout import KeyboardLayoutBase


class KeyboardLayoutSLV(KeyboardLayoutBase):
    """Map ASCII characters to appropriate keypresses on a standard SLV PC keyboard.

    Non-ASCII characters and most control characters will raise an exception.
    """

    # The ASCII_TO_KEYCODE bytes object is used as a table to maps ASCII 0-127
    # to the corresponding # keycode on a US 104-key keyboard.
    # The user should not normally need to use this table,
    # but it is not marked as private.
    #
    # Because the table only goes to 127, we use the top bit of each byte (ox80) to indicate
    # that the shift key should be pressed. So any values 0x{8,9,a,b}* are shifted characters.
    #
    # The Python compiler will concatenate all these bytes literals into a single bytes object.
    # Micropython/CircuitPython will store the resulting bytes constant in flash memory
    # if it's in a .mpy file, so it doesn't use up valuable RAM.
    #
    # \x00 entries have no keyboard key and so won't be sent.
    ASCII_TO_KEYCODE = (
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x2a'  # BACKSPACE
        b'\x2b'  # '\t'
        b'\x28'  # '\n'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x29'  # ESC
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x00'
        b'\x2c'  # ' '
        b'\x9e'  # '!'
        b'\x9f'  # '"'
        b'\xa0'  # '#'
        b'\xa1'  # '$'
        b'\xa2'  # '%'
        b'\xa3'  # '&'
        b'\x2d'  # "'"
        b'\xa5'  # '('
        b'\xa6'  # ')'
        b'\x55'  # '*'
        b'\x57'  # '+'
        b'\x36'  # ','
        b'\x56'  # '-'
        b'\x37'  # '.'
        b'\xa4'  # '/'
        b'\x27'  # '0'
        b'\x1e'  # '1'
        b'\x1f'  # '2'
        b'\x20'  # '3'
        b'\x21'  # '4'
        b'\x22'  # '5'
        b'\x23'  # '6'
        b'\x24'  # '7'
        b'\x25'  # '8'
        b'\x26'  # '9'
        b'\xb7'  # ':'
        b'\xb6'  # ';'
        b'\x64'  # '<'
        b'\xa7'  # '='
        b'\xe4'  # '>'
        b'\xad'  # '?'
        b'\x19'  # '@'
        b'\x84'  # 'A'
        b'\x85'  # 'B'
        b'\x86'  # 'C'
        b'\x87'  # 'D'
        b'\x88'  # 'E'
        b'\x89'  # 'F'
        b'\x8a'  # 'G'
        b'\x8b'  # 'H'
        b'\x8c'  # 'I'
        b'\x8d'  # 'J'
        b'\x8e'  # 'K'
        b'\x8f'  # 'L'
        b'\x90'  # 'M'
        b'\x91'  # 'N'
        b'\x92'  # 'O'
        b'\x93'  # 'P'
        b'\x94'  # 'Q'
        b'\x95'  # 'R'
        b'\x96'  # 'S'
        b'\x97'  # 'T'
        b'\x98'  # 'U'
        b'\x99'  # 'V'
        b'\x9a'  # 'W'
        b'\x9b'  # 'X'
        b'\x9d'  # 'Z'
        b'\x9c'  # 'Y'
        b'\x09'  # '['
        b'\x14'  # '\\'
        b'\x0a'  # ']'
        b'\x20'  # '^'
        b'\xb8'  # '_'
        b'\x24'  # '`'
        b'\x04'  # 'a'
        b'\x05'  # 'b'
        b'\x06'  # 'c'
        b'\x07'  # 'd'
        b'\x08'  # 'e'
        b'\x09'  # 'f'
        b'\x0a'  # 'g'
        b'\x0b'  # 'h'
        b'\x0c'  # 'i'
        b'\x0d'  # 'j'
        b'\x0e'  # 'k'
        b'\x0f'  # 'l'
        b'\x10'  # 'm'
        b'\x11'  # 'n'
        b'\x12'  # 'o'
        b'\x13'  # 'p'
        b'\x14'  # 'q'
        b'\x15'  # 'r'
        b'\x16'  # 's'
        b'\x17'  # 't'
        b'\x18'  # 'u'
        b'\x19'  # 'v'
        b'\x1a'  # 'w'
        b'\x1b'  # 'x'
        b'\x1d'  # 'z'
        b'\x1c'  # 'y'
        b'\x05'  # '{'
        b'\x1a'  # '|'
        b'\x11'  # '}'
        b'\x1e'  # '~'
        b'\x4c'  # 'DEL'
    )
    NEED_ALTGR = '~^@[]\\|{}€÷×łŁß¤ˇ˘°˛`˙´˝¨¸§'
    HIGHER_ASCII = {
        0x20ac: 0x08,  # '€'
        0x161:  0x2f,  # 'š'
        0x160:  0xaf,  # 'Š'
        0x111:  0x30,  # 'đ'
        0x110:  0xb0,  # 'Đ'
        0x10d:  0x33,  # 'č'
        0x10c:  0xb3,  # 'Č'
        0x107:  0x34,  # 'ć'
        0x106:  0xb4,  # 'Ć'
        0x17e:  0x31,  # 'ž'
        0x17d:  0xb1,  # 'Ž'
        0xf7:   0x2f,  # '÷'
        0xd7:   0x30,  # '×'
        0x142:  0x0e,  # 'ł'
        0x141:  0x0f,  # 'Ł'
        0xdf:   0x34,  # 'ß'
        0xa4:   0x31,  # '¤'
        0x2c7:  0x1f,  # 'ˇ'
        0x2d8:  0x21,  # '˘'
        0xb0:   0x22,  # '°'
        0x2db:  0x23,  # '˛'
        0x60:   0x24,  # '`'
        0x2d9:  0x25,  # '˙'
        0xb4:   0x26,  # '´'
        0x2dd:  0x27,  # '˝'
        0xa8:   0x2d,  # '¨'
        0xb8:   0x2e,  # '¸'
        0xa7:   0x10   # '§'
    }
    COMBINED_KEYS = {
        0xe4: 0x2de1,  # 'ä'
        0xeb: 0x2de5,  # 'ë'
        0xf6: 0x2def,  # 'ö'
        0xfc: 0x2df5,  # 'ü'
        0xc4: 0x2dc1,  # 'Ä'
        0xcb: 0x2dc5,  # 'Ë'
        0xd6: 0x2dcf,  # 'Ö'
        0xdc: 0x2dd5,  # 'Ü'
        
        0xe1: 0x26e1,  # 'á'
        0xe9: 0x26e5,  # 'é'
        0xed: 0x26e9,  # 'í'
        0xf3: 0x26ef,  # 'ó'
        0xfa: 0x26f5,  # 'ú'
        0xfd: 0x26f9,  # 'ý'
        0xc1: 0x26c1,  # 'Á'
        0xc9: 0x26c5,  # 'É'
        0xcd: 0x26c9,  # 'Í'
        0xd3: 0x26cf,  # 'Ó'
        0xda: 0x26d5,  # 'Ú'
        0xdd: 0x26d9,  # 'Ý'
    }


KeyboardLayout = KeyboardLayoutSLV
