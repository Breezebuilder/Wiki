# balatro_text_to_svg.py v1.0.0
# Breezebuilder 2025-03-02 
# Takes text input formatted with Balatro style modifiers and generates a Balatro-styled text SVG.

# Uses m6x11plus font by Daniel Linssen 2025
# https://managore.itch.io/m6x11

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import math
import re
import argparse

COLOUR_DICT = {
    "red": "#FE5F55FF",
    "mult": "#FE5F55FF",
    "blue": "#009DFFFF",
    "chips": "#009DFFFF",
    "green": "#4BC292FF",
    "money": "#F3B958FF",
    "gold": "#EAC058FF",
    "attention": "#FF9A00FF",
    "purple": "#8867A5FF",
    "white": "#FFFFFFFF",
    "inactive": "#88888899",
    "spades": "#403995FF",
    "hearts": "#F03464FF",
    "clubs": "#235955FF",
    "diamonds": "#F06B3FFF",
    "tarot": "#A782D1FF",
    "planet": "#13AFCEFF",
    "spectral": "#4584FAFF",
    "common": "#009DFFFF",
    "uncommon": "#4BC292FF",
    "rare": "#FE5F55FF",
    "legendary": "#B26CBBFF",
    "enhanced": "#8389DDFF",
    "edition": [ "#E5D7EC", "#FFFEC6", "#FFFFB3", "#FFFFBC", "#E5F3DE", "#C1CCFF", "#B2B4FF", "#C1B8FF", "#E5D7EC" ],
    "dark_edition": [ "#9999CC", "#BDA7A7", "#CC9999", "#BDA7A7", "#9999CB", "#7474F0", "#6565FF", "#7474F0", "#9999CC" ],
    "default": "#4F6367FF"
}

CHAR_PATHS_DICT = {
    32: ('space', 12, 0, 6, ''),
    33: ('exclam', 6, 0, 8, 'h4v16h-4v-16zm0 18h4v4h-4v-4z'),
    34: ('quotedbl', 12, 0, 8, 'h4v6h-2v-2h-2v-4zm6 0h4v6h-2v-2h-2v-4z'),
    35: ('numbersign', 16, 2, 8, 'h4v6h2v-6h4v6h2v4h-2v2h2v4h-2v6h-4v-6h-2v6h-4v-6h-2v-4h2v-2h-2v-4h2v-6zm4 10v2h2v-2h-2z'),
    36: ('dollar', 14, 4, 8, 'h4v4h4v4h-8v2h6v2h2v6h-2v2h-2v4h-4v-4h-4v-4h8v-2h-6v-2h-2v-6h2v-2h2v-4z'),
    37: ('percent', 14, 0, 12, 'h4v4h-4v-4zm8 2h4v4h-2v2h-2v2h-2v2h-2v2h-4v-4h2v-2h2v-2h2v-2h2v-2zm0 10h4v4h-4v-4z'),
    38: ('ampersand', 20, 4, 8, 'h8v2h2v8h-2v2h2v-2h4v4h-2v2h-2v2h4v4h-6v-2h-2v2h-8v-2h-2v-10h2v-8h2v-2zm2 4v4h4v-4h-4zm-2 8v6h4v-4h-2v-2h-2z'),
    39: ('quotesingle', 6, 0, 8, 'h4v6h-2v-2h-2v-4z'),
    40: ('parenleft', 10, 2, 8, 'h6v4h-4v18h4v4h-6v-2h-2v-22h2v-2z'),
    41: ('parenright', 10, 0, 8, 'h6v2h2v22h-2v2h-6v-4h4v-18h-4v-4z'),
    42: ('asterisk', 12, 0, 8, 'h4v2h2v-2h4v4h-2v2h2v4h-4v-2h-2v2h-4v-4h2v-2h-2v-4z'),
    43: ('plus', 14, 4, 14, 'h4v4h4v4h-4v4h-4v-4h-4v-4h4v-4z'),
    44: ('comma', 6, 0, 26, 'h4v6h-2v-2h-2v-4z'),
    45: ('hyphen', 14, 0, 18, 'h12v4h-12v-4z'),
    46: ('period', 6, 0, 26, 'h4v4h-4v-4z'),
    47: ('slash', 14, 8, 8, 'h4v6h-2v4h-2v4h-2v4h-2v4h-4v-6h2v-4h2v-4h2v-4h2v-4z'),
    48: ('zero', 14, 2, 8, 'h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    49: ('one', 14, 4, 8, 'h4v18h4v4h-12v-4h4v-12h-4v-4h4v-2z'),
    50: ('two', 14, 2, 8, 'h8v2h2v10h-2v2h-2v2h-2v2h6v4h-12v-6h2v-2h2v-2h2v-2h2v-6h-4v2h-4v-4h2v-2z'),
    51: ('three', 14, 2, 8, 'h8v2h2v6h-2v2h2v10h-2v2h-8v-2h-2v-4h4v2h4v-6h-4v-4h4v-4h-4v2h-4v-4h2v-2z'),
    52: ('four', 14, 0, 8, 'h4v10h4v-10h4v22h-4v-8h-6v-2h-2v-12z'),
    53: ('five', 14, 0, 8, 'h12v4h-8v4h6v2h2v10h-2v2h-10v-4h8v-6h-8v-12z'),
    54: ('six', 14, 2, 8, 'h8v2h2v4h-4v-2h-4v4h6v2h2v10h-2v2h-8v-2h-2v-18h2v-2zm2 12v6h4v-6h-4z'),
    55: ('seven', 14, 0, 8, 'h12v10h-2v4h-2v8h-4v-10h2v-4h2v-4h-8v-4z'),
    56: ('eight', 14, 2, 8, 'h8v2h2v6h-2v2h2v10h-2v2h-8v-2h-2v-10h2v-2h-2v-6h2v-2zm2 4v4h4v-4h-4zm0 8v6h4v-6h-4z'),
    57: ('nine', 14, 2, 8, 'h8v2h2v18h-2v2h-8v-2h-2v-4h4v2h4v-4h-6v-2h-2v-10h2v-2zm2 4v6h4v-6h-4z'),
    58: ('colon', 6, 0, 14, 'h4v4h-4v-4zm0 12h4v4h-4v-4z'),
    59: ('semicolon', 6, 0, 14, 'h4v4h-4v-4zm0 12h4v6h-2v-2h-2v-4z'),
    60: ('less', 12, 6, 14, 'h4v4h-2v2h-2v4h2v2h2v4h-4v-2h-2v-2h-2v-2h-2v-4h2v-2h2v-2h2v-2z'),
    61: ('equal', 14, 0, 14, 'h12v4h-12v-4zm0 8h12v4h-12v-4z'),
    62: ('greater', 12, 0, 14, 'h4v2h2v2h2v2h2v4h-2v2h-2v2h-2v2h-4v-4h2v-2h2v-4h-2v-2h-2v-4z'),
    63: ('question', 14, 2, 8, 'h8v2h2v8h-2v2h-2v4h-4v-6h2v-2h2v-4h-4v2h-4v-4h2v-2zm2 18h4v4h-4v-4z'),
    64: ('at', 20, 4, 8, 'h10v2h2v2h2v10h-2v2h-8v-2h-2v-6h2v-2h4v-2h-6v2h-2v10h2v2h12v4h-14v-2h-2v-2h-2v-14h2v-2h2v-2zm6 10v2h2v-2h-2z'),
    65: ('A', 14, 2, 8, 'h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    66: ('B', 14, 0, 8, 'h10v2h2v8h-2v2h2v8h-2v2h-10v-22zm4 4v4h4v-4h-4zm0 8v6h4v-6h-4z'),
    67: ('C', 14, 2, 8, 'h10v4h-8v14h8v4h-10v-2h-2v-18h2v-2z'),
    68: ('D', 14, 0, 8, 'h10v2h2v18h-2v2h-10v-22zm4 4v14h4v-14h-4z'),
    69: ('E', 14, 2, 8, 'h10v4h-8v4h6v4h-6v6h8v4h-10v-2h-2v-18h2v-2z'),
    70: ('F', 14, 2, 8, 'h10v4h-8v4h6v4h-6v10h-4v-20h2v-2z'),
    71: ('G', 14, 2, 8, 'h10v4h-8v14h4v-6h-2v-4h6v12h-2v2h-8v-2h-2v-18h2v-2z'),
    72: ('H', 14, 0, 8, 'h4v8h4v-8h4v22h-4v-10h-4v10h-4v-22z'),
    73: ('I', 14, 0, 8, 'h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    74: ('J', 14, 0, 8, 'h12v20h-2v2h-8v-2h-2v-4h4v2h4v-14h-8v-4z'),
    75: ('K', 14, 0, 8, 'h4v8h2v-2h2v-6h4v8h-2v2h-2v2h2v2h2v8h-4v-6h-2v-2h-2v8h-4v-22z'),
    76: ('L', 14, 0, 8, 'h4v18h8v4h-10v-2h-2v-20z'),
    77: ('M', 18, 0, 8, 'h14v2h2v20h-4v-18h-2v14h-4v-14h-2v18h-4v-22z'),
    78: ('N', 14, 0, 8, 'h10v2h2v20h-4v-18h-4v18h-4v-22z'),
    79: ('O', 14, 2, 8, 'h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    80: ('P', 14, 0, 8, 'h10v2h2v10h-2v2h-6v8h-4v-22zm4 4v6h4v-6h-4z'),
    81: ('Q', 16, 2, 8, 'h8v2h2v16h2v4h-4v-2h-2v2h-6v-2h-2v-18h2v-2zm2 4v14h2v-2h2v-12h-4z'),
    82: ('R', 14, 0, 8, 'h10v2h2v8h-2v2h2v10h-4v-8h-2v-2h-2v10h-4v-22zm4 4v4h4v-4h-4z'),
    83: ('S', 14, 2, 8, 'h10v4h-8v4h6v2h2v10h-2v2h-10v-4h8v-6h-6v-2h-2v-8h2v-2z'),
    84: ('T', 14, 0, 8, 'h12v4h-4v18h-4v-18h-4v-4z'),
    85: ('U', 14, 0, 8, 'h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    86: ('V', 14, 0, 8, 'h4v16h4v-16h4v18h-2v2h-2v2h-4v-2h-2v-2h-2v-18z'),
    87: ('W', 18, 0, 8, 'h4v18h2v-10h4v10h2v-18h4v20h-2v2h-12v-2h-2v-20z'),
    88: ('X', 16, 0, 8, 'h4v6h2v2h2v-2h2v-6h4v8h-2v2h-2v2h2v2h2v8h-4v-6h-2v-2h-2v2h-2v6h-4v-8h2v-2h2v-2h-2v-2h-2v-8z'),
    89: ('Y', 14, 0, 8, 'h4v8h4v-8h4v10h-2v2h-2v10h-4v-10h-2v-2h-2v-10z'),
    90: ('Z', 14, 0, 8, 'h12v6h-2v4h-2v4h-2v4h6v4h-12v-6h2v-4h2v-4h2v-4h-6v-4z'),
    91: ('bracketleft', 10, 0, 8, 'h8v4h-4v18h4v4h-8v-26z'),
    92: ('backslash', 14, 0, 8, 'h4v4h2v4h2v4h2v4h2v6h-4v-4h-2v-4h-2v-4h-2v-4h-2v-6z'),
    93: ('bracketright', 10, 0, 8, 'h8v26h-8v-4h4v-18h-4v-4z'),
    94: ('asciicircum', 14, 4, 8, 'h4v2h2v2h2v4h-4v-2h-4v2h-4v-4h2v-2h2v-2z'),
    95: ('underscore', 14, 0, 26, 'h12v4h-12v-4z'),
    97: ('a', 14, 0, 14, 'h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    98: ('b', 14, 0, 8, 'h4v6h6v2h2v12h-2v2h-10v-22zm4 10v8h4v-8h-4z'),
    99: ('c', 14, 2, 14, 'h10v4h-8v8h8v4h-10v-2h-2v-12h2v-2z'),
    100: ('d', 14, 8, 8, 'h4v22h-10v-2h-2v-12h2v-2h6v-6zm-4 10v8h4v-8h-4z'),
    101: ('e', 14, 2, 14, 'h8v2h2v8h-8v2h8v4h-10v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    102: ('f', 14, 4, 8, 'h8v4h-6v2h4v4h-4v12h-4v-12h-2v-4h2v-4h2v-2z'),
    103: ('g', 14, 2, 14, 'h8v2h2v18h-2v2h-10v-4h8v-2h-6v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    104: ('h', 14, 0, 8, 'h4v6h6v2h2v14h-4v-12h-4v12h-4v-22z'),
    105: ('i', 6, 0, 8, 'h4v4h-4v-4zm0 6h4v16h-4v-16z'),
    106: ('j', 10, 4, 8, 'h4v4h-4v-4zm0 6h4v20h-2v2h-6v-4h4v-18z'),
    107: ('k', 14, 0, 8, 'h4v6h6v2h2v6h-2v2h2v6h-4v-4h-2v-2h-2v6h-4v-22zm4 10v2h4v-2h-4z'),
    108: ('l', 6, 0, 8, 'h4v22h-4v-22z'),
    109: ('m', 18, 0, 14, 'h14v2h2v14h-4v-12h-2v12h-4v-12h-2v12h-4v-16z'),
    110: ('n', 14, 0, 14, 'h10v2h2v14h-4v-12h-4v12h-4v-16z'),
    111: ('o', 14, 2, 14, 'h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    112: ('p', 14, 2, 14, 'h8v2h2v12h-2v2h-6v6h-4v-20h2v-2zm2 4v8h4v-8h-4z'),
    113: ('q', 14, 2, 14, 'h8v2h2v20h-4v-6h-6v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    114: ('r', 14, 0, 14, 'h4v2h2v-2h6v4h-6v2h-2v10h-4v-16z'),
    115: ('s', 14, 2, 14, 'h10v4h-8v2h6v2h2v6h-2v2h-10v-4h8v-2h-6v-2h-2v-6h2v-2z'),
    116: ('t', 14, 2, 8, 'h4v6h6v4h-6v8h6v4h-8v-2h-2v-10h-2v-4h2v-6z'),
    117: ('u', 14, 0, 14, 'h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    118: ('v', 14, 0, 14, 'h4v10h4v-10h4v12h-2v2h-2v2h-4v-2h-2v-2h-2v-12z'),
    119: ('w', 18, 0, 14, 'h4v12h2v-10h4v10h2v-12h4v14h-2v2h-12v-2h-2v-14z'),
    120: ('x', 16, 0, 14, 'h4v2h2v2h2v-2h2v-2h4v4h-2v2h-2v4h2v2h2v4h-4v-2h-2v-2h-2v2h-2v2h-4v-4h2v-2h2v-4h-2v-2h-2v-4z'),
    121: ('y', 14, 0, 14, 'h4v12h4v-12h4v20h-2v2h-10v-4h8v-2h-6v-2h-2v-14z'),
    122: ('z', 14, 0, 14, 'h12v6h-2v2h-2v2h-2v2h6v4h-12v-6h2v-2h2v-2h2v-2h-6v-4z'),
    123: ('braceleft', 12, 4, 8, 'h6v4h-4v8h-2v2h2v8h4v4h-6v-2h-2v-10h-2v-4h2v-8h2v-2z'),
    124: ('bar', 6, 0, 8, 'h4v26h-4v-26z'),
    125: ('braceright', 12, 0, 8, 'h6v2h2v8h2v4h-2v10h-2v2h-6v-4h4v-8h2v-2h-2v-8h-4v-4z'),
    126: ('asciitilde', 14, 2, 16, 'h4v2h2v2h2v-2h2v4h-2v2h-4v-2h-2v-2h-2v2h-2v-4h2v-2z'),
    161: ('exclamdown', 6, 0, 14, 'h4v4h-4v-4zm0 6h4v16h-4v-16z'),
    162: ('cent', 14, 4, 10, 'h4v4h4v4h-8v8h8v4h-4v4h-4v-4h-2v-2h-2v-12h2v-2h2v-4z'),
    163: ('sterling', 16, 4, 8, 'h8v2h2v4h-4v-2h-4v6h6v4h-6v4h8v4h-14v-4h2v-4h-2v-4h2v-8h2v-2z'),
    164: ('currency', 18, 0, 10, 'h4v2h8v-2h4v4h-2v8h2v4h-4v-2h-8v2h-4v-4h2v-8h-2v-4zm6 6v4h4v-4h-4z'),
    165: ('yen', 14, 0, 8, 'h4v6h4v-6h4v8h-2v2h-2v2h4v2h-4v2h4v2h-4v4h-4v-4h-4v-2h4v-2h-4v-2h4v-2h-2v-2h-2v-8z'),
    166: ('brokenbar', 6, 0, 8, 'h4v10h-4v-10zm0 16h4v10h-4v-10z'),
    167: ('section', 14, 2, 8, 'h10v4h-8v2h4v2h2v2h2v8h-2v2h2v6h-2v2h-10v-4h8v-2h-4v-2h-2v-2h-2v-8h2v-2h-2v-6h2v-2zm2 12v4h4v-4h-4z'),
    168: ('dieresis', 12, 0, 8, 'h4v4h-4v-4zm6 0h4v4h-4v-4z'),
    169: ('copyright', 20, 4, 8, 'h10v2h2v2h2v14h-2v2h-2v2h-10v-2h-2v-2h-2v-14h2v-2h2v-2zm2 4v2h-2v10h2v2h6v-2h-4v-2h-2v-6h2v-2h4v-2h-6zm6 2v2h-4v6h4v2h2v-10h-2zm-4 0h4v2h-4v-2zm-2 2h2v6h-2v-6z m2 6h4v2h-4v-2z'),
    170: ('ordfeminine', 8, 0, 8, 'h4v2h-4v-2zm4 2h2v8h-4v-2h2v-2h-2v-2h2v-2zm-4 4h2v2h-2v-2z'),
    171: ('guillemotleft', 20, 6, 14, 'h4v4h-2v2h-2v4h2v2h2v4h-4v-2h-2v-2h-2v-2h-2v-4h2v-2h2v-2h2v-2zm8 0h4v4h-2v2h-2v4h2v2h2v4h-4v-2h-2v-2h-2v-2h-2v-4h2v-2h2v-2h2v-2z'),
    172: ('logicalnot', 14, 0, 8, 'h12v8h-4v-4h-8v-4z'),
    174: ('registered', 20, 4, 8, 'h10v2h2v2h2v14h-2v2h-2v2h-10v-2h-2v-2h-2v-14h2v-2h2v-2zm2 4v2h4v2h2v2h-2v2h2v4h2v-10h-2v-2h-6zm-2 2v10h2v-10h-2zm2 0h4v2h-2v2h2v2h-2v4h-2v-10zm2 2v2h2v-2h-2zm0 4v4 h-2v2h6v-2h-2v-4h-2zm2 -4h2v2h-2v-2zm0 4h2v4h-2v-4z'),
    176: ('degree', 12, 2, 8, 'h6v2h2v6h-2v2h-6v-2h-2v-6h2v-2zm2 4v2h2v-2h-2z'),
    177: ('plusminus', 14, 4, 14, 'h4v4h4v4h-4v4h4v4h-12v-4h4v-4h-4v-4h4v-4z'),
    182: ('paragraph', 18, 2, 8, 'h14v28h-4v-24h-2v24h-4v-16h-4v-2h-2v-8h2v-2z'),
    186: ('ordmasculine', 12, 2, 8, 'h6v2h2v8h-2v2h-6v-2h-2v-8h2v-2zm2 4v4h2v-4h-2z'),
    187: ('guillemotright', 20, 0, 14, 'h4v2h2v2h2v2h2v4h-2v2h-2v2h-2v2h-4v-4h2v-2h2v-4h-2v-2h-2v-4zm8 0h4v2h2v2h2v2h2v4h-2v2h-2v2h-2v2h-4v-4h2v-2h2v-4h-2v-2h-2v-4z'),
    191: ('questiondown', 14, 4, 8, 'h4v4h-4v-4zm0 6h4v6h-2v2h-2v4h4v-2h4v4h-2v2h-8v-2h-2v-8h2v-2h2v-4z'),
    192: ('Agrave', 14, 4, 0, 'h4v6h-2v-2h-2v-4zm-2 8h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    193: ('Aacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-2 8h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    195: ('Atilde', 14, 2, 0, 'h4v2h4v-2h2v4h-2v2h-4v-2h-4v2h-2v-4h2v-2zm0 8h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    196: ('Adieresis', 14, 0, 2, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-6 6h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    197: ('Aring', 14, 4, 0, 'h6v6h-6v-6zm2 2v2h2v-2h-2zm-4 6h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    198: ('AE', 22, 2, 8, 'h18v4h-8v4h6v4h-6v6h8v4h-12v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    199: ('Ccedilla', 14, 2, 8, 'h10v4h-8v14h8v4h-2v4h-6v-2h4v-2h-6v-2h-2v-18h2v-2z'),
    200: ('Egrave', 14, 4, 0, 'h4v6h-2v-2h-2v-4zm-2 8h10v4h-8v4h6v4h-6v6h8v4h-10v-2h-2v-18h2v-2z'),
    201: ('Eacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-2 8h10v4h-8v4h6v4h-6v6h8v4h-10v-2h-2v-18h2v-2z'),
    202: ('Ecircumflex', 14, 4, 0, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-2 8h10v4h-8v4h6v4h-6v6h8v4h-10v-2h-2v-18h2v-2z'),
    203: ('Edieresis', 14, 0, 2, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-6 6h10v4h-8v4h6v4h-6v6h8v4h-10v-2h-2v-18h2v-2z'),
    204: ('Igrave', 14, 4, 0, 'h4v6h-2v-2h-2v-4zm-4 8h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    205: ('Iacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-4 8h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    206: ('Icircumflex', 14, 4, 0, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-4 8h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    207: ('Idieresis', 14, 0, 2, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-8 6h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    209: ('Ntilde', 14, 2, 0, 'h4v2h4v-2h2v4h-2v2h-4v-2h-4v2h-2v-4h2v-2zm-2 8h10v2h2v20h-4v-18h-4v18h-4v-22z'),
    210: ('Ograve', 14, 4, 0, 'h4v6h-2v-2h-2v-4zm-2 8h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    211: ('Oacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-2 8h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    212: ('Ocircumflex', 14, 4, 0, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-2 8h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    213: ('Otilde', 14, 2, 0, 'h4v2h4v-2h2v4h-2v2h-4v-2h-4v2h-2v-4h2v-2zm0 8h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    214: ('Odieresis', 14, 0, 2, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-6 6h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    215: ('multiply', 12, 0, 16, 'h4v2h2v-2h4v4h-2v2h2v4h-4v-2h-2v2h-4v-4h2v-2h-2v-4z'),
    216: ('Oslash', 18, 4, 8, 'h8v2h2v-2h2v4h-2v16h-2v2h-8v-2h-2v2h-2v-4h2v-16h2v-2zm2 4v6h2v-2h2v-4h-4zm2 8v2h-2v4h4v-6h-2z'),
    217: ('Ugrave', 14, 4, 0, 'h4v6h-2v-2h-2v-4zm-4 8h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    218: ('Uacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-4 8h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    219: ('Ucircumflex', 14, 4, 0, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-4 8h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    220: ('Udieresis', 14, 0, 2, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-8 6h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    221: ('Yacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-4 8h4v8h4v-8h4v10h-2v2h-2v10h-4v-10h-2v-2h-2v-10z'),
    222: ('Thorn', 14, 0, 8, 'h4v4h6v2h2v10h-2v2h-6v4h-4v-22zm4 8v6h4v-6h-4z'),
    223: ('germandbls', 16, 0, 8, 'h10v2h2v6h-2v2h2v2h2v8h-2v2h-6v-4h4v-4h-2v-2h-2v-4h2v-4h-4v18h-4v-22z'),
    224: ('agrave', 14, 4, 6, 'h4v6h-2v-2h-2v-4zm-4 8h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    225: ('aacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-4 8h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    226: ('acircumflex', 14, 4, 6, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-4 8h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    227: ('atilde', 14, 2, 6, 'h4v2h4v-2h2v4h-2v2h-4v-2h-4v2h-2v-4h2v-2zm-2 8h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    228: ('adieresis', 14, 0, 8, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-8 6h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    229: ('aring', 14, 4, 6, 'h6v6h-6v-6zm2 2v2h2v-2h-2zm-6 6h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    230: ('ae', 22, 0, 14, 'h18v2h2v8h-8v2h8v4h-18v-2h-2v-6h2v-2h6v-2h-8v-4zm12 4v2h4v-2h-4zm-8 6v2h4v-2h-4z'),
    231: ('ccedilla', 14, 2, 14, 'h10v4h-8v8h8v4h-2v4h-6v-2h4v-2h-6v-2h-2v-12h2v-2z'),
    232: ('egrave', 14, 4, 6, 'h4v6h-2v-2h-2v-4zm-2 8h8v2h2v8h-8v2h8v4h-10v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    233: ('eacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-2 8h8v2h2v8h-8v2h8v4h-10v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    234: ('ecircumflex', 14, 4, 6, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-2 8h8v2h2v8h-8v2h8v4h-10v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    235: ('edieresis', 14, 0, 8, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-6 6h8v2h2v8h-8v2h8v4h-10v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    236: ('igrave', 6, 0, 6, 'h4v6h-2v-2h-2v-4zm0 8h4v16h-4v-16z'),
    237: ('iacute', 6, 0, 6, 'h4v4h-2v2h-2v-6zm0 8h4v16h-4v-16z'),
    238: ('icircumflex', 10, 2, 6, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm0 8h4v16h-4v-16z'),
    239: ('idieresis', 14, 0, 8, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-4 6h4v16h-4v-16z'),
    241: ('ntilde', 14, 2, 6, 'h4v2h4v-2h2v4h-2v2h-4v-2h-4v2h-2v-4h2v-2zm-2 8h10v2h2v14h-4v-12h-4v12h-4v-16z'),
    242: ('ograve', 14, 4, 6, 'h4v6h-2v-2h-2v-4zm-2 8h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    243: ('oacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-2 8h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    244: ('ocircumflex', 14, 4, 6, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-2 8h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    245: ('otilde', 14, 2, 6, 'h4v2h4v-2h2v4h-2v2h-4v-2h-4v2h-2v-4h2v-2zm0 8h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    246: ('odieresis', 14, 0, 8, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-6 6h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    247: ('divide', 14, 4, 12, 'h4v4h-4v-4zm-4 6h12v4h-12v-4zm4 6h4v4h-4v-4z'),
    248: ('oslash', 18, 4, 14, 'h8v2h2v-2h2v4h-2v10h-2v2h-8v-2h-2v2h-2v-4h2v-10h2v-2zm2 4v4h2v-2h2v-2h-4zm2 4v2h-2v2h4v-4h-2z'),
    249: ('ugrave', 14, 4, 6, 'h4v6h-2v-2h-2v-4zm-4 8h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    250: ('uacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-4 8h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    251: ('ucircumflex', 14, 4, 6, 'h4v2h2v4h-2v-2h-4v2h-2v-4h2v-2zm-4 8h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    252: ('udieresis', 14, 0, 8, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-8 6h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    253: ('yacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-4 8h4v12h4v-12h4v20h-2v2h-10v-4h8v-2h-6v-2h-2v-14z'),
    254: ('thorn', 14, 0, 8, 'h4v6h6v2h2v12h-2v2h-6v4h-4v-26zm4 10v8h4v-8h-4z'),
    255: ('ydieresis', 14, 0, 8, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-8 6h4v12h4v-12h4v20h-2v2h-10v-4h8v-2h-6v-2h-2v-14z'),
    256: ('Amacron', 14, 2, 2, 'h8v4h-8v-4zm0 6h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    257: ('amacron', 14, 2, 8, 'h8v4h-8v-4zm-2 6h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    258: ('Abreve', 14, 2, 0, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm0 8h8v2h2v20h-4v-8h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    259: ('abreve', 14, 2, 6, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm-2 8h10v2h2v14h-10v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    260: ('Aogonek', 16, 2, 8, 'h8v2h2v20h-2v2h4v2h-6v-12h-4v8h-4v-20h2v-2zm2 4v6h4v-6h-4z'),
    261: ('aogonek', 16, 0, 14, 'h10v2h2v14h-2v2h4v2h-6v-4h-6v-2h-2v-6h2v-2h6v-2h-8v-4zm4 10v2h4v-2h-4z'),
    262: ('Cacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-2 8h10v4h-8v14h8v4h-10v-2h-2v-18h2v-2z'),
    263: ('cacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-2 8h10v4h-8v8h8v4h-10v-2h-2v-12h2v-2z'),
    272: ('Dcroat', 16, 2, 8, 'h10v2h2v18h-2v2h-10v-10h-2v-2h2v-10zm4 4v6h2v2h-2v6h4v-14h-4z'),
    273: ('dcroat', 16, 8, 8, 'h4v2h2v2h-2v16h-2v2h-8v-2h-2v-12h2v-2h6v-2h-2v-2h2v-2zm-4 10v8h4v-8h-4z'),
    274: ('Emacron', 14, 2, 2, 'h8v4h-8v-4zm0 6h10v4h-8v4h6v4h-6v6h8v4h-10v-2h-2v-18h2v-2z'),
    275: ('emacron', 14, 2, 8, 'h8v4h-8v-4zm0 6h8v2h2v8h-8v2h8v4h-10v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    276: ('Ebreve', 14, 2, 0, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm0 8h10v4h-8v4h6v4h-6v6h8v4h-10v-2h-2v-18h2v-2z'),
    277: ('ebreve', 14, 2, 6, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm0 8h8v2h2v8h-8v2h8v4h-10v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    280: ('Eogonek', 16, 2, 8, 'h10v4h-8v4h6v4h-6v6h8v4h-2v2h4v2h-6v-4h-6v-2h-2v-18h2v-2z'),
    281: ('eogonek', 16, 2, 14, 'h8v2h2v8h-8v2h8v4h-2v2h4v2h-6v-4h-6v-2h-2v-12h2v-2zm2 4v2h4v-2h-4z'),
    286: ('Gbreve', 14, 2, 0, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm0 8h10v4h-8v14h4v-6h-2v-4h6v12h-2v2h-8v-2h-2v-18h2v-2z'),
    287: ('gbreve', 14, 2, 6, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm0 8h8v2h2v18h-2v2h-10v-4h8v-2h-6v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    298: ('Imacron', 14, 2, 2, 'h8v4h-8v-4zm-2 6h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    299: ('imacron', 10, 0, 8, 'h8v4h-8v-4zm2 6h4v16h-4v-16z'),
    300: ('Ibreve', 14, 2, 0, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm-2 8h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    301: ('ibreve', 10, 0, 6, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm2 8h4v16h-4v-16z'),
    304: ('Idotaccent', 14, 4, 2, 'h4v4h-4v-4zm-4 6h12v4h-4v14h4v4h-12v-4h4v-14h-4v-4z'),
    305: ('dotlessi', 6, 0, 14, 'h4v16h-4v-16z'),
    321: ('Lslash', 18, 4, 8, 'h4v8h2v2h-2v8h8v4h-10v-2h-2v-6h-2v-2h2v-12zm6 6h2v2h-2v-2zm-10 8h2v2h-2v-2z'),
    322: ('lslash', 14, 4, 8, 'h4v8h2v2h-2v12h-4v-8h-2v-2h2v-12zm6 6h2v2h-2v-2zm-10 8h2v2h-2v-2z'),
    323: ('Nacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-4 8h10v2h2v20h-4v-18h-4v18h-4v-22z'),
    324: ('nacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-4 8h10v2h2v14h-4v-12h-4v12h-4v-16z'),
    332: ('Omacron', 14, 2, 2, 'h8v4h-8v-4zm0 6h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    333: ('omacron', 14, 2, 8, 'h8v4h-8v-4zm0 6h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    334: ('Obreve', 14, 2, 0, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm0 8h8v2h2v18h-2v2h-8v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    335: ('obreve', 14, 2, 6, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm0 8h8v2h2v12h-2v2h-8v-2h-2v-12h2v-2zm2 4v8h4v-8h-4z'),
    338: ('OE', 22, 2, 8, 'h18v4h-8v4h6v4h-6v6h8v4h-18v-2h-2v-18h2v-2zm2 4v14h4v-14h-4z'),
    339: ('oe', 22, 2, 14, 'h16v2h2v8h-8v2h8v4h-18v-2h-2v-12h2v-2zm2 4v8h4v-8h-4zm8 0v2h4v-2h-4z'),
    346: ('Sacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-2 8h10v4h-8v4h6v2h2v10h-2v2h-10v-4h8v-6h-6v-2h-2v-8h2v-2z'),
    347: ('sacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-2 8h10v4h-8v2h6v2h2v6h-2v2h-10v-4h8v-2h-6v-2h-2v-6h2v-2z'),
    350: ('Scedilla', 14, 2, 8, 'h10v4h-8v4h6v2h2v10h-2v2h-2v4h-6v-2h4v-2h-6v-4h8v-6h-6v-2h-2v-8h2v-2z'),
    351: ('scedilla', 14, 2, 14, 'h10v4h-8v2h6v2h2v6h-2v2h-2v4h-6v-2h4v-2h-6v-4h8v-2h-6v-2h-2v-6h2v-2z'),
    362: ('Umacron', 14, 2, 2, 'h8v4h-8v-4zm-2 6h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    363: ('umacron', 14, 2, 8, 'h8v4h-8v-4zm-2 6h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    364: ('Ubreve', 14, 2, 0, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm-2 8h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    365: ('ubreve', 14, 2, 6, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm-2 8h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    376: ('Ydieresis', 14, 0, 2, 'h4v4h-4v-4zm8 0h4v4h-4v-4zm-8 6h4v8h4v-8h4v10h-2v2h-2v10h-4v-10h-2v-2h-2v-10z'),
    377: ('Zacute', 14, 4, 0, 'h4v4h-2v2h-2v-6zm-4 8h12v6h-2v4h-2v4h-2v4h6v4h-12v-6h2v-4h2v-4h2v-4h-6v-4z'),
    378: ('zacute', 14, 4, 6, 'h4v4h-2v2h-2v-6zm-4 8h12v6h-2v2h-2v2h-2v2h6v4h-12v-6h2v-2h2v-2h2v-2h-6v-4z'),
    379: ('Zdotaccent', 14, 4, 2, 'h4v4h-4v-4zm-4 6h12v6h-2v4h-2v4h-2v4h6v4h-12v-6h2v-4h2v-4h2v-4h-6v-4z'),
    380: ('zdotaccent', 14, 4, 8, 'h4v4h-4v-4zm-4 6h12v6h-2v2h-2v2h-2v2h6v4h-12v-6h2v-2h2v-2h2v-2h-6v-4z'),
    467: ('uni01D3', 14, 2, 0, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm-2 8h4v18h4v-18h4v20h-2v2h-8v-2h-2v-20z'),
    468: ('uni01D4', 14, 2, 6, 'h2v2h4v-2h2v4h-2v2h-4v-2h-2v-4zm-2 8h4v12h4v-12h4v14h-2v2h-8v-2h-2v-14z'),
    956: ('uni03BC', 14, 0, 14, 'h4v12h4v-12h4v14h-2v2h-6v4h-4v-20z'),
}

COMMENT_HEADER = "Generated by balatro_text_to_svg.py"
COMMENT_LINK = "https://github.com/Breezebuilder/Steamodded-Wiki/blob/dev/Assets/Scripts/balatro_text_to_svg.py"
SHADOW_COLOUR = "rgba(0,0,0,0.3)"
SHADOW_OFFSET_X = 2
SHADOW_OFFSET_Y = 2
BORDER_X = 5
ANIM_DURATION = 2.4
CHAR_KERN_DEFAULT = 2
MIN_SVG_WIDTH = 40


def calculate_text_width(text, size = 1):
    width = 0
    for char in text:
        char_code = ord(char)
        if char_code in CHAR_PATHS_DICT:
            width += CHAR_PATHS_DICT[char_code][1]
        else:
            width += CHAR_KERN_DEFAULT
    return (width * size)


def prepare_char_array(text):
    chars = []
    adv_x = 0
    for char in text:
        char_code = ord(char)
        if char_code in CHAR_PATHS_DICT:
            char_name, char_adv, _, _, _ = CHAR_PATHS_DICT[char_code]
            chars.append((char_code, char, char_name, char_adv, adv_x))
            adv_x += char_adv
        else:
            adv_x += CHAR_KERN_DEFAULT
    return chars, adv_x


def parse_control_groups(text_line):
    format_groups = []
    plain_text = ""
    start_text_pattern = re.compile(r'^([^\{]+)(\{.*)')
    command_group_pattern = re.compile(r'\{([^\}]*)\}([^{}]*)(\{?.*)')
    inner_command_pattern = re.compile(r'([a-zA-Z]):([^,;]+)')

    match = start_text_pattern.match(text_line)
    if match:
        text, remainder = match.groups()
        format_groups.append(({}, text))
        plain_text += text
        text_line = remainder

    while text_line:
        match = command_group_pattern.match(text_line)
        if match:
            command, text, remainder = match.groups()
            commands = inner_command_pattern.findall(command)
            if commands:
                command_dict = {k.upper(): v for k, v in commands}
                if "X" in command_dict:
                    text = text.replace(" ", "")
                format_groups.append((command_dict, text))
                plain_text += text
            else:
                format_groups.append(({}, text))
                plain_text += text
            text_line = remainder
        else:
            format_groups.append(({}, text_line))
            plain_text += text_line
            break

    return plain_text, format_groups


def populate_styling_groups(text_groups, default_colour, loc_var_colours):
    styling_groups = []
    i = 0
    for control, text in text_groups:

        control_colour = default_colour
        control_anim = 0
        control_background_colour = None
        control_size = 1.0

        part_chars, part_width = prepare_char_array(text)

        if "C" in control:
            control_colour_string = control["C"]
            if control_colour_string in COLOUR_DICT:
                control_colour = COLOUR_DICT[control_colour_string]
            else:
                control_colour = COLOUR_DICT["default"]

        if "E" in control:
            try:
                control_anim = int(control["E"])
            except ValueError:
                control_anim = 0

        if "X" in control:
            control_background_string = control["X"]
            if control_background_string in COLOUR_DICT:
                control_background_colour = COLOUR_DICT[control_background_string]

        if "S" in control:
            control_size = float(control["S"])

        if "V" in control:
            try:
                control_colour_index = int(control["V"]) - 1
                control_colour = loc_var_colours[control_colour_index]
            except ValueError:
                control_colour = default_colour

        if "B" in control:
            try:
                control_background_colour_index = int(control["B"]) - 1
                control_background_colour = loc_var_colours[control_background_colour_index]
            except ValueError:
                control_background_colour = None

        styling_groups.append((control, text, part_chars, part_width, control_colour, control_anim, control_background_colour, control_size))
    
    return styling_groups


def build_svg_defs(text):
    used_chars = set()
    for char in text:
        char_code = ord(char)
        if char_code != 32 and char_code in CHAR_PATHS_DICT:
            used_chars.add(char_code)
    
    svg_content = "\t<defs>\n"
    for char_code in sorted(used_chars):
        if char_code in CHAR_PATHS_DICT:
            char_name, _, mx, my, char_path = CHAR_PATHS_DICT[char_code]
            svg_content += f'\t\t<path id="{char_name}" d="m{mx} {my}{char_path}"/>\n'
    svg_content += "\t</defs>\n"
    
    return svg_content


def format_control_group(control_dict):
    return "{{{}}}".format(",".join(f"{str(k)}:{str(v)}" for k, v in control_dict.items()))


def group_animated_chars(text):
    group_count = min(len(text), 6)

    groups = [[] for _ in range(group_count)]

    adv_x = 0
    for i, char in enumerate(text):
        char_code = ord(char)
        if char_code in CHAR_PATHS_DICT:
            char_name, char_adv, _, _, _ = CHAR_PATHS_DICT[char_code]
            group_index = i % 6
            groups[group_index].append((char_code, char, char_name, adv_x))
            adv_x += char_adv
        else:
            adv_x += CHAR_KERN_DEFAULT

    return groups


def build_raw_svg(raw_text, colour, do_shadow, selectable, filename):
    part_chars, part_width = prepare_char_array(raw_text)
    text_width = calculate_text_width(raw_text)
    width = BORDER_X * 2 + text_width

    svg_comment = f'''<!-- {COMMENT_HEADER} - {COMMENT_LINK} -->\n'''
    svg_comment += f'''<!--\n\t {raw_text}\n-->\n\n'''

    svg_content += f'''<svg xmlns="http://www.w3.org/2000/svg" height="40" viewBox="0 0 {width} 40">\n'''
    svg_content += build_svg_defs(raw_text)

    if do_shadow:
        svg_content += f'''\t<g transform="translate({SHADOW_OFFSET_X},{SHADOW_OFFSET_Y})" fill="{SHADOW_COLOUR}">\n'''
        for char_code, _, char_name, _, adv_x in part_chars:
            if char_code != 32:
                svg_content += f'''\t\t<use href="#{char_name}" x="{BORDER_X + adv_x}"/>\n'''
        svg_content += "\t</g>\n"

    svg_content += f'''\t<g fill="{colour}">\n'''
    for char_code, _, char_name, _, adv_x in part_chars:
        if char_code != 32:
            svg_content += f'''\t\t<use href="#{char_name}" x="{BORDER_X + adv_x}"/>\n'''
    svg_content += "\t</g>\n"

    if selectable:
        svg_content += f'''\t<text font-family="m6x11plus,Courier New" fill="transparent">\n'''

        text_string = raw_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;").replace('"', "&quot;")
        svg_content += f'''\t\t<tspan font-size="32" xml:space="preserve" lengthAdjust="spacingAndGlyphs" x="{BORDER_X}" y="26" textLength="{text_width}">{text_string}</tspan>'''

        svg_content += "\n\t</text>\n"

    svg_content += "</svg>"

    export_svg(svg_content, filename)


def build_styled_svg(input_text, plain_text, text_groups, default_colour, loc_vars_colours, svg_size, do_shadow, selectable, filename):
    if not text_groups:
        build_raw_svg(plain_text, default_colour, do_shadow, selectable, filename)
        return

    largest_size = 0
    width = 0
    has_X_controls = False

    styling_groups = populate_styling_groups(text_groups, default_colour, loc_vars_colours)

    svg_comment = f'''<!-- {COMMENT_HEADER} - {COMMENT_LINK} -->\n'''
    svg_comment += f'''<!--\n\t {input_text}\n'''
    svg_comment += f'''\t {plain_text}\n-->\n\n'''

    for _, _, _, part_width, _, control_anim, control_background_colour, control_size in styling_groups:
        width += (control_size * part_width)
        largest_size = (max(largest_size, control_size))
        if control_background_colour:
            has_X_controls = True
            width += (6 * control_size)

    total_width = math.ceil(max(2 * BORDER_X + width, MIN_SVG_WIDTH))
    height = math.ceil(max(largest_size * MIN_SVG_WIDTH, MIN_SVG_WIDTH))

    svg_width, svg_height = svg_size
    svg_width_string = ""
    if svg_width > 0:
        svg_width_string = f''' width="{svg_width}"'''

    svg_head = f'''<svg xmlns="http://www.w3.org/2000/svg" height="{svg_height}"{svg_width_string} viewBox="0 0 {total_width} {height}">\n'''
    svg_defs = build_svg_defs(plain_text)

    if do_shadow:
        svg_shadow_head = f'''\t<g fill="{SHADOW_COLOUR}">\n'''
        svg_shadow_mid = ""
        svg_shadow_tail = "\t</g>\n"

    svg_shapes = "\t<g>\n" if has_X_controls else ""
    svg_content = "\t<g>\n"
    svg_text = f'''\t<text font-family="m6x11plus,Courier New" fill="transparent">\n\t\t''' if selectable else ""
    svg_tail = "</svg>"

    width = BORDER_X
    px = 0
    for controls, text, part_chars, part_width, control_colour, control_anim, control_background_colour, control_size in styling_groups:
        if text == "":
            continue

        dx = width

        scale_text = ""
        if control_size != 1.0:
            scale_text = f''' scale({control_size:g})'''

        if control_background_colour:
            dy = (1 - (control_size / largest_size)) * 12
        else:
            dy = (1 - (control_size / largest_size)) * height / 2
        
            if do_shadow:
                dsx = round(px + dx + (control_size * SHADOW_OFFSET_X), 3)
                dsy = round(dy + control_size * SHADOW_OFFSET_Y, 3)

                svg_shadow_mid += f'''\t\t<g transform="translate({dsx:g},{dsy:g}){scale_text}">\n'''
                for char_code, _, char_name, _, adv_x in part_chars:
                    if char_code != 32:
                        svg_shadow_mid += f'''\t\t\t<use href="#{char_name}" x="{adv_x:g}"/>\n'''
                svg_shadow_mid += "\t\t</g>\n"

        if isinstance(control_colour, list):
            gradient_values = "; ".join(control_colour)
            svg_content += f'''\t\t<g transform="translate({dx:g},{dy:g}){scale_text}">\n'''
            svg_content += f'''\t\t\t<animate attributeName="fill" values="{gradient_values}" dur="4s" repeatCount="indefinite"/>\n'''
        else:
            svg_content += f'''\t\t<g fill="{control_colour}" transform="translate({dx:g},{dy:g}){scale_text}">\n'''
        
        if control_background_colour:
            px += (3 * control_size)
            bw = (part_width * control_size) - 2
            bh = height * 0.7
            dh = (height - 12 - bh) / 2

            if isinstance(control_background_colour, list):
                gradient_values = ";".join(control_background_colour)
                svg_shapes += f'''\t\t<path d="m{(px + dx):g} {dh:g}h{bw:g}l4 4v{bh:g}l-4 4h-{bw:g}l-4-4v-{bh:g}z">\n'''
                svg_shapes += f'''\t\t\t<animate attributeName="fill" values="{gradient_values}" dur="4s" repeatCount="indefinite"/>\n'''
                svg_shapes += "\t\t</path>\n"
            else:
                svg_shapes += f'''\t\t<path d="m{(px + dx):g} {dh:g}h{bw:g}l4 4v{bh:g}l-4 4h-{bw:g}l-4-4v-{bh:g}z" fill="{control_background_colour}"/>\n'''

        if control_anim == 1 or control_anim == 2:
            animation_parts = group_animated_chars(text)

            anim_scale = round(math.sqrt(control_size) * 0.6, 2)

            for i, group in enumerate(animation_parts):
                svg_content += "\t\t\t<g>\n"
                svg_content += f'''\t\t\t\t<g>\n'''
                for char_code, _, char_name, adv_x in group:
                    if char_code != 32:
                        svg_content += f'''\t\t\t\t\t<use href="#{char_name}" x="{px + adv_x}"/>\n'''
                
                if control_anim == 1:
                    svg_content += f'''\t\t\t\t\t<animateMotion path="m0 0 a{anim_scale:g} {anim_scale:g} 0 0 1 {(2 * anim_scale):g} 0 a{anim_scale:g} {anim_scale:g} 0 0 1 -{(2 * anim_scale):g} 0" dur="{ANIM_DURATION:g}" begin="{(-ANIM_DURATION + i * 0.4):g}" repeatCount="indefinite"/>\n'''
                    svg_content += "\t\t\t\t</g>\n"
                    svg_content += f'''\t\t\t\t<animateMotion path="m0 0 a{anim_scale:g} {anim_scale:g} 0 0 0 -{(2 * anim_scale):g} 0 a{anim_scale:g} {anim_scale:g} 0 0 0 {(2 * anim_scale):g} 0" dur="{ANIM_DURATION:g}" begin="{(-ANIM_DURATION + i * 0.4):g}" repeatCount="indefinite"/>\n'''
                    svg_content += "\t\t\t</g>\n" 
                
                else:
                    svg_content += f'''\t\t\t\t\t<animateMotion path="m0 0 a{anim_scale:g} {anim_scale:g} 0 0 1 {(2 * anim_scale):g} 0" dur="{ANIM_DURATION:g}" begin="{(i * 0.4):g}" keyTimes="0;0.25;1" keyPoints="0;1;1" repeatCount="indefinite"/>\n'''
                    svg_content += "\t\t\t\t</g>\n"
                    svg_content += f'''\t\t\t\t<animateMotion path="m0 0 a{anim_scale:g} {anim_scale:g} 0 0 0 -{(2 * anim_scale):g} 0" dur="{ANIM_DURATION:g}" begin="{(i * 0.4):g}" keyTimes="0;0.25;1" keyPoints="0;1;1" repeatCount="indefinite"/>\n'''
                    svg_content += "\t\t\t</g>\n"
        else:
            for char_code, _, char_name, _, adv_x in part_chars:
                if char_code != 32:
                    svg_content += f'''\t\t\t<use href="#{char_name}" x="{px + adv_x}"/>\n'''
        
        if control_background_colour:
            px += (3 * control_size)

        svg_content += "\t\t</g>\n"

        if selectable:
            control_string = format_control_group(controls)
            dty = (height *  0.7) - ((1 - (control_size / largest_size)) * height / 5)

            text_string = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;").replace('"', "&quot;")

            preserve_string = ''' xml:space="preserve"''' if " " in text_string else ""
            
            svg_text += f'''<tspan font-size="{control_size * 32:g}" lengthAdjust="spacingAndGlyphs" x="{px + width-1:g}" y="{dty:g}" textLength="{1}">{control_string}</tspan>'''
            svg_text += f'''<tspan font-size="{control_size * 32:g}"{preserve_string} lengthAdjust="spacingAndGlyphs" x="{px + width:g}" y="{dty:g}" textLength="{control_size * part_width:g}">{text_string}</tspan>'''

        width += control_size * part_width

    svg_shadows = ""
    if do_shadow and svg_shadow_mid != "":
        svg_shadows = svg_shadow_head + svg_shadow_mid + svg_shadow_tail

    svg_shapes += "\t</g>\n" if has_X_controls else ""
    svg_content += "\t</g>\n"
    svg_text += "\n\t</text>\n" if selectable else ""
   
    svg = svg_comment + svg_head + svg_defs + svg_shadows + svg_shapes + svg_content + svg_text + svg_tail
    export_svg(svg, filename)


def export_svg(svg_content, filename):
    if filename.endswith(".svg"):
        filename = filename[:-4]

    print(f"Exporting to {filename}.svg")

    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename + ".svg", 'w', encoding='utf-8') as file:
        file.write(svg_content)


def full_char_test():
    all_chars = ''.join(chr(char_code) for char_code in CHAR_PATHS_DICT.keys())
    return all_chars


def parse_colour(colour_string):
    colour_string = colour_string.strip()
    if colour_string.startswith("#"):
        return colour_string
    elif colour_string in COLOUR_DICT:
        return COLOUR_DICT[colour_string]
    elif len(colour_string) in (6, 8):
        return f"#{colour_string}"
    else:
        raise ValueError(f"Unknown colour: {colour_string}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''
Balatro Text to SVG
Converts text with Balatro styling modifiers to animated SVG. Supports the following modifiers:
    Defined text colour	 ................ {C:colour-key}
    Defined background colour ........... {X:colour-key}
    Variable/custom text colour	......... {V:colour-index}
    Variable/custom background colour ... {B:colour-index}
    Text motion	......................... {E:motion-index}
    Text scale .......................... {s:scale}
                                     
Uses m6x11plus font by Daniel Linssen.''')
    
    parser.add_argument('input', type=str, help='Text to convert to SVG')
    parser.add_argument('-c', '--colours', type=str, help='String of comma-separated hex or named colours to be used by {V:} and {B:} modifiers')
    parser.add_argument('-d', '--dual-theme', action='store_true', help='Output both dark-mode and light-mode versions')
    parser.add_argument('-f', '--file', type=str, help='Filename for the output SVG')
    parser.add_argument('-r', '--raw', action='store_true', help='Disable all style parsing of input text')
    parser.add_argument('-s', '--shadow', action='store_true', help='Add shadow to the text')
    parser.add_argument('-t', '--text-selectable', action='store_true', help='Enable text selection feature in the SVG')
    parser.add_argument('-x', '--width', type=float, default = -1, help='Set svg display width. Default: -1')
    parser.add_argument('-y', '--height', type=float, default = 128, help='Set svg display height. Default: 32')

    args = parser.parse_args()

    plain_text, text_groups = parse_control_groups(args.input)

    if args.file:
        file = args.file
        if file.endswith(".svg"):
            file = file[:-4]
    else:
        file = re.sub(r'[\\/*?:"<>| ]', '_', plain_text[:16])

    colours = []
    if args.colours:
        colours = [parse_colour(colour.strip()) for colour in args.colours.split(',')]

    svg_size = (args.width, args.height)

    if args.dual_theme:
        light_file = file + "_light"
        dark_file = file + "_dark"

        if args.raw:
            build_raw_svg(args.input, COLOUR_DICT["default"], args.shadow, args.text_selectable, light_file)
            build_raw_svg(args.input, COLOUR_DICT["white"], args.shadow, args.text_selectable, dark_file)
        else:
            build_styled_svg(args.input, plain_text, text_groups, COLOUR_DICT["default"], colours, svg_size, args.shadow, args.text_selectable, light_file)
            build_styled_svg(args.input, plain_text, text_groups, COLOUR_DICT["white"], colours, svg_size, args.shadow, args.text_selectable, dark_file)
    else:
        if args.raw:
            build_raw_svg(args.input, COLOUR_DICT["default"], args.shadow, args.text_selectable, file)
        else:
            build_styled_svg(args.input, plain_text, text_groups, COLOUR_DICT["default"], colours, svg_size, args.shadow, args.text_selectable, file)
        