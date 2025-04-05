#!/bin/bash

# usage: balatro_text_to_svg.py [-h] [-c COLOURS] [-d] [-f FILE] [-r] [-s] [-t] [-x WIDTH] [-y HEIGHT] input

# Balatro Text to SVG
# Converts text with Balatro styling modifiers to animated SVG. Supports the following modifiers:
#     Defined text colour  ................ {C:colour-key}
#     Defined background colour ........... {X:colour-key}
#     Variable/custom text colour ......... {V:colour-index}
#     Variable/custom background colour ... {B:colour-index}
#     Text motion ......................... {E:motion-index}
#     Text scale .......................... {s:scale}

# Uses m6x11plus font by Daniel Linssen.

# positional arguments:
#   input                 Text to convert to SVG

# options:
#   -h, --help            show this help message and exit
#   -c COLOURS, --colours COLOURS
#                         String of comma-separated hex or named colours to be used by {V:} and {B:} modifiers
#   -d, --dual-theme      Output both dark-mode and light-mode versions
#   -f FILE, --file FILE  Filename for the output SVG
#   -r, --raw             Disable all style parsing of input text
#   -s, --shadow          Add shadow to the text
#   -t, --text-selectable
#                         Enable text selection feature in the SVG
#   -x WIDTH, --width WIDTH
#                         Set svg display width. Default: -1
#   -y HEIGHT, --height HEIGHT
#                         Set svg display height. Default: 32

path="../Text-Styling/"

python3 ./balatro_text_to_svg.py "{C:blue}+1{} hand" -d -s -f "${path}example_+1_hand"
python3 ./balatro_text_to_svg.py "{X:mult,C:white}X0.5{}" -s -f "${path}example_X0.5"

python3 ./balatro_text_to_svg.py "{C:mult}+4{} Mult" -d -s -f "${path}example_+4_Mult"
python3 ./balatro_text_to_svg.py "{C:attention}1{} free {C:green}Reroll" -d -s -f "${path}example_1_free_Reroll"
python3 ./balatro_text_to_svg.py "{C:green}1 in 6{} chance" -d -s -f "${path}example_1_in_6_chance"

python3 ./balatro_text_to_svg.py "{X:mult,C:white}X3{} Mult" -d -s -f "${path}example_X3_Mult"
python3 ./balatro_text_to_svg.py "{X:gold} W I D E {}" -s -f "${path}example_WIDE"

python3 ./balatro_text_to_svg.py "{X:chips,C:white} X 1 . 5 {} Chips{}" -d -s -f "${path}example_X1.5_Chips"

python3 ./balatro_text_to_svg.py "{V:1}FF00FF{}" -c "#FF00FF" -s -f "${path}example_FF00FF"
python3 ./balatro_text_to_svg.py "{V:1}Heart{} suit" -c "hearts" -d -s -f "${path}example_Heart_suit"

python3 ./balatro_text_to_svg.py "{B:1}00FF00{}" -c "#00FF00" -f "${path}example_00FF00"
python3 ./balatro_text_to_svg.py "{B:1,V:2}Oh no!{} Anyway..." -c "#FF0000,#000000" -d -s -f "${path}example_Oh_no_Anyway"
python3 ./balatro_text_to_svg.py "{B:1,V:2}Spa{B:2,V:1}rts{}" -c "spades,hearts" -f "${path}example_Spa-rts"

python3 ./balatro_text_to_svg.py "{E:1,C:green}probabilities{}" -s -f "${path}example_probabilities"
python3 ./balatro_text_to_svg.py "{E:2}Joker" -d -s -f "${path}example_Joker"
python3 ./balatro_text_to_svg.py "{E:2,C:red}self destructs{}" -s -f "${path}example_self_destructs"

python3 ./balatro_text_to_svg.py "{s:0.8}0.8 {s:1.0}1.0 {s:1.1}1.1" -d -s -f "${path}example_0.8_1.0_1.1"

python3 ./balatro_text_to_svg.py "{E:1,C:edition,s:2}YOU WIN!{}" -s -f "${path}example_YOU_WIN!"
python3 ./balatro_text_to_svg.py "{s:0.8}({V:1,s:0.8}lvl.2{s:0.8}){} Level up" -c "#89A4FF" -d -s -f "${path}example_lvl.2_Level_up"

python3 ./balatro_text_to_svg.py "{C:red}+1{} discard" -d -s -f "${path}example_+1_discard"
python3 ./balatro_text_to_svg.py "{C:chips}+50{} Chips" -d -s -f "${path}example_+50_Chips"
python3 ./balatro_text_to_svg.py "Earn {C:money}\$4" -d -s -f "${path}example_Earn_\$4"
python3 ./balatro_text_to_svg.py "{C:gold}Android{}" -s -f "${path}example_Android"
python3 ./balatro_text_to_svg.py "{C:attention}+1{} hand size" -d -s -f "${path}example_+1_hand_size"
python3 ./balatro_text_to_svg.py "{C:purple}Purple Seal{}" -s -f "${path}example_Purple_Seal"
python3 ./balatro_text_to_svg.py "{C:inactive}(Must have room){}" -s -f "${path}example_Must_have_room"
python3 ./balatro_text_to_svg.py "{C:spades}Spades{}" -s -f "${path}example_suit_Spades"
python3 ./balatro_text_to_svg.py "{C:hearts}Hearts{}" -s -f "${path}example_suit_Hearts"
python3 ./balatro_text_to_svg.py "{C:clubs}Clubs{}" -s -f "${path}example_suit_Clubs"
python3 ./balatro_text_to_svg.py "{C:diamonds}Diamonds{}" -s -f "${path}example_suit_Diamonds"
python3 ./balatro_text_to_svg.py "{C:tarot}Tarot{} card" -d -s -f "${path}example_Tarot_card"
python3 ./balatro_text_to_svg.py "{C:planet}Planet{} card" -d -s -f "${path}example_Planet_card"
python3 ./balatro_text_to_svg.py "{C:spectral}Spectral{} card" -d -s -f "${path}example_Spectral_card"
python3 ./balatro_text_to_svg.py "Add {C:dark_edition}Negative" -d -s -f "${path}example_Add_Negative"
python3 ./balatro_text_to_svg.py "{E:1,C:legendary}Legendary{} Joker" -d -s -f "${path}example_Legendary_Joker"
python3 ./balatro_text_to_svg.py "{C:enhanced}Enhancement{}" -s -f "${path}example_Enhancement"

python3 ./balatro_text_to_svg.py "{C:tarot}The Fool{}" -s -f "${path}example_The_Fool"
python3 ./balatro_text_to_svg.py "{C:attention}+1{} consumable slot" -t -s -f "${path}tooltip_+1_consumable_slot"