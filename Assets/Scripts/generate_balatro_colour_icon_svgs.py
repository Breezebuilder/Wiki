# generate_balatro_colour_icon_svgs.py
# Breezebuilder 2025-03-01
# Generates circular colour icon SVG files for all LOC_COLOURS used in Balatro.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import math

HEIGHT = 32
NUM_ANIM_FRAMES = 8
OUTPUT_PATH = "../Colour-Icons/"

colours_vanilla = {
	"G.C.RED":  "#fe5f55ff",
	"G.C.MULT": "#fe5f55ff",
	"G.C.BLUE": "#009dffff",
	"G.C.CHIPS": "#009dffff",
	"G.C.GREEN": "#4bc292ff",
	"G.C.MONEY": "#f3b958ff",
	"G.C.GOLD": "#eac058ff",
	"G.C.FILTER": "#ff9a00ff",
	"G.C.PURPLE": "#8867a5ff",
	"G.C.WHITE": "#ffffffff",
	"G.C.UI.TEXT_INACTIVE": "#88888899",
	"G.C.SECONDARY_SET.Tarot": "#a782d1ff",
	"G.C.SECONDARY_SET.Planet": "#13afceff",
	"G.C.SECONDARY_SET.Spectral": "#4584faff",
	"G.C.RARITY[4]": "#b26cbbff",
	"G.C.SECONDARY_SET.Enhanced": "#8389ddff",
	"G.C.UI.TEXT_DARK": "#4f6367ff",
}

colours_smods_rarity = {
	"G.C.RARITY.Common": "#009dffff",
	"G.C.RARITY.Uncommon": "#4bc292ff",
	"G.C.RARITY.Rare": "#fe5f55ff",
	"G.C.RARITY.Legendary": "#b26cbbff",
}

colours_suits = {
	"G.C.SUITS.Hearts": ("#f03464ff", "#f83b2fff"),
	"G.C.SUITS.Diamonds": ("#f06b3fff", "#e29000ff"),
	"G.C.SUITS.Spades": ("#403995ff", "#4f31b9ff"),
	"G.C.SUITS.Clubs": ("#235955ff", "#008ee6ff"),
}

def generate_single_colour_svgs(colour_table):
	for name, hex_colour in colour_table.items():
		svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" height="{HEIGHT}" viewBox="0 0 16 16">
	<circle fill="{hex_colour}" cx="8" cy="8" r="8"/>
</svg>'''
		with open(f"{OUTPUT_PATH}{name}.svg", "w") as file:
			file.write(svg_content)

def generate_dual_colour_svgs(colour_table):
	for name, (hex_colour1, hex_colour2) in colour_table.items():
		svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" height="{HEIGHT}" viewBox="0 0 16 16">
	<path fill="{hex_colour1}" d="M 8 0 a 1 1 0 1 0 0 16 Z"/>
	<path fill="{hex_colour2}" d="M 8 0 a 1 1 0 0 1 0 16 Z"/>
</svg>'''
		with open(f"{OUTPUT_PATH}{name}.svg", "w") as file:
			file.write(svg_content)

def generate_edition_colour_svg(num_gradient_samples):
	colours = generate_edition_colours(num_gradient_samples)
	colour_codes = "\n"
	for i, colour in enumerate(colours):
		colour_codes += "\t" * 4 + colour_to_hex(colour) + ";\n"
	colour_codes += "\t" * 4 + colour_to_hex(colours[0]) + ";\n" + "\t" * 3
	svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" height="{HEIGHT}" viewBox="0 0 16 16">
<circle cx="8" cy="8" r="8">
	<animate
		attributeName="fill"
		values="{colour_codes}"
		dur="4s"
		repeatCount="indefinite" />
	</circle>
</svg>'''
	with open(f"{OUTPUT_PATH}G.C.EDITION.svg", "w") as file:
		file.write(svg_content)

def generate_dark_edition_colour_svg(num_gradient_samples):
	colours = generate_dark_edition_colours(num_gradient_samples)
	colour_codes = "\n"
	for i, colour in enumerate(colours):
		colour_codes += "\t" * 4 + colour_to_hex(colour) + ";\n"
	colour_codes += "\t" * 4 + colour_to_hex(colours[0]) + ";\n" + "\t" * 3
	svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" height="{HEIGHT}" viewBox="0 0 16 16">
<circle cx="8" cy="8" r="8">
	<animate
		attributeName="fill"
		values="{colour_codes}"
		dur="4s"
		repeatCount="indefinite" />
	</circle>
</svg>'''
	with open(f"{OUTPUT_PATH}G.C.DARK_EDITION.svg", "w") as file:
		file.write(svg_content)

def generate_edition_colours(num_gradient_samples):
	colours = []
	angle = (math.pi * 2) / num_gradient_samples
	for i in range(num_gradient_samples):
		r = min(255, int(255 * (0.7 + 0.2 * (1 + math.sin(i * angle + 0)))))
		b = min(255, int(255 * (0.7 + 0.2 * (1 + math.sin(i * angle + 3)))))
		g = min(255, int(255 * (0.7 + 0.2 * (1 + math.sin(i * angle + 6)))))
		colours.append((r, g, b))
	return colours

def generate_dark_edition_colours(num_gradient_samples):
	colours = []
	angle = (math.pi * 2) / num_gradient_samples
	for i in range(num_gradient_samples):
		r = min(255, int(255 * (0.6 + 0.2 * math.sin(i * angle))))
		b = min(255, int(255 * (0.6 + 0.2 * (1 - math.sin(i * angle)))))
		g = min(r, b)
		colours.append((r, g, b))
	return colours

def colour_to_hex(colour_tuple):
	return '#%02x%02x%02x' % colour_tuple

if __name__ == "__main__":
	generate_single_colour_svgs(colours_vanilla)
	generate_single_colour_svgs(colours_smods_rarity)
	generate_dual_colour_svgs(colours_suits)
	generate_edition_colour_svg(NUM_ANIM_FRAMES)
	generate_dark_edition_colour_svg(NUM_ANIM_FRAMES)