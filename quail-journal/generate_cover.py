from PIL import Image, ImageDraw, ImageFont
import os

# Cover dimensions with bleed (0.125" on all sides)
BLEED = 0.125 * 300  # 37.5 pixels bleed
WIDTH = 6 * 300  # 1800 pixels (trim)
HEIGHT = 9 * 300  # 2700 pixels (trim)

# Spine width
PAGE_COUNT = 100
SPINE_WIDTH = int(PAGE_COUNT * 0.002252 * 300)

# Total with bleed: back + spine + front + bleed on both ends
TOTAL_WIDTH = int((BLEED + WIDTH + SPINE_WIDTH + WIDTH + BLEED))
TOTAL_HEIGHT = int((BLEED + HEIGHT + BLEED))

# Create cover
cover = Image.new('RGB', (TOTAL_WIDTH, HEIGHT), '#f5f5dc')  # Cream background
draw = ImageDraw.Draw(cover)

# Colors
DARK_GREEN = '#2d5016'
ACCENT_BLUE = '#667eea'
TEXT_DARK = '#333333'

# Try to load fonts, fallback to default
try:
    # System fonts (may not exist)
    title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 120)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 50)
    author_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 40)
    spine_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 35)
    back_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 30)
except:
    # Fallback to default
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    author_font = ImageFont.load_default()
    spine_font = ImageFont.load_default()
    back_font = ImageFont.load_default()

# FRONT COVER (right side)
front_x = WIDTH + SPINE_WIDTH

# Title
title_text = "THE QUAIL\nKEEPER'S\nJOURNAL"
draw.multiline_text((front_x + WIDTH//2, 600), title_text, 
                    font=title_font, fill=DARK_GREEN, align='center',
                    anchor='mm')

# Subtitle
subtitle = "A Comprehensive Record Book\nfor Coturnix Quail Breeding"
draw.multiline_text((front_x + WIDTH//2, 1100), subtitle,
                    font=subtitle_font, fill=TEXT_DARK, align='center',
                    anchor='mm')

# Decorative line
draw.line([(front_x + 200, 1300), (front_x + WIDTH - 200, 1300)], 
          fill=ACCENT_BLUE, width=8)

# Quail illustration (simplified as egg shapes)
for i in range(3):
    egg_x = front_x + WIDTH//2 - 150 + i*150
    draw.ellipse([(egg_x - 40, 1600), (egg_x + 40, 1700)], 
                 fill='#e8dcc5', outline='#d4c4a8', width=3)

# Author
author_text = "M4Quick Quail Farm"
draw.text((front_x + WIDTH//2, 2000), author_text,
          font=author_font, fill=TEXT_DARK, align='center',
          anchor='mm')

# SPINE (middle)
spine_center_x = WIDTH + SPINE_WIDTH//2

# Spine text (rotated 90 degrees)
from PIL import ImageOps
spine_img = Image.new('RGB', (SPINE_WIDTH, HEIGHT), '#f5f5dc')
spine_draw = ImageDraw.Draw(spine_img)
spine_draw.text((SPINE_WIDTH//2, HEIGHT//2), "THE QUAIL KEEPER'S JOURNAL",
                font=spine_font, fill=DARK_GREEN, anchor='mm')
spine_draw.text((SPINE_WIDTH//2, HEIGHT - 200), "M4Quick",
                font=author_font, fill=TEXT_DARK, anchor='mm')
# Rotate and paste
spine_rotated = spine_img.rotate(90, expand=True)
cover.paste(spine_img, (WIDTH, 0))

# BACK COVER (left side)
back_x = 0

# Back cover text
back_title = "Track Everything You Need"
draw.text((back_x + WIDTH//2, 400), back_title,
          font=subtitle_font, fill=DARK_GREEN, align='center',
          anchor='mm')

# Features list
features = [
    "✓ Daily Egg Production Log",
    "✓ Hatch Success Records",
    "✓ Health & Treatment Tracker",
    "✓ Breeding Pair Lineages",
    "✓ Expense & Revenue Tracking",
    "✓ 12 Months of Records",
    "✓ Quick Reference Guide",
]

y_start = 700
for feature in features:
    draw.text((back_x + 150, y_start), feature,
              font=back_font, fill=TEXT_DARK)
    y_start += 80

# Description
desc = "The essential companion for backyard quail\n" \
       "keepers and homesteaders. Track your flock\n" \
       "from egg to harvest with this comprehensive\n" \
       "journal designed specifically for Coturnix quail."
draw.multiline_text((back_x + WIDTH//2, 1700), desc,
                    font=back_font, fill=TEXT_DARK, align='center',
                    anchor='mm')

# Barcode area (white box)
draw.rectangle([(back_x + WIDTH - 400, HEIGHT - 500), 
                (back_x + WIDTH - 100, HEIGHT - 200)],
               fill='white', outline='black', width=2)
draw.text((back_x + WIDTH - 250, HEIGHT - 350), "[BARCODE]",
          font=back_font, fill='black', anchor='mm')

# Save
cover.save('Quail_Journal_Cover.png', 'PNG', dpi=(300, 300))
cover.save('Quail_Journal_Cover.pdf', 'PDF', resolution=300.0)

print("Cover created: Quail_Journal_Cover.png and .pdf")
print(f"Dimensions: {TOTAL_WIDTH}x{HEIGHT} pixels ({TOTAL_WIDTH/300:.2f}\" x {HEIGHT/300:.2f}\")")
print(f"Spine width: {SPINE_WIDTH/300:.3f}\" ({SPINE_WIDTH} pixels)")
