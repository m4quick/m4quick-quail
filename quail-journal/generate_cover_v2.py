from PIL import Image, ImageDraw, ImageFont
import os

# Cover dimensions with bleed (0.125" on all sides at 300 DPI)
BLEED = 0.125 * 300  # 37.5 pixels
DPI = 300

# Trim size (final book size)
TRIM_WIDTH = 6 * DPI    # 1800 pixels
TRIM_HEIGHT = 9 * DPI   # 2700 pixels

# Spine width for 100 pages (KDP standard: ~0.002252" per page for white paper)
# But KDP expects exact 12.423" total, so spine = 12.423 - 0.125 - 6 - 6 - 0.125 = 0.173"
SPINE_INCHES = 0.173
SPINE_WIDTH = int(SPINE_INCHES * DPI)  # ~52 pixels

# Full cover with bleed: bleed + back + spine + front + bleed
FULL_WIDTH = int(BLEED + TRIM_WIDTH + SPINE_WIDTH + TRIM_WIDTH + BLEED)
FULL_HEIGHT = int(BLEED + TRIM_HEIGHT + BLEED)

print(f"Cover dimensions: {FULL_WIDTH/DPI:.3f}\" x {FULL_HEIGHT/DPI:.3f}\"")
print(f"KDP expects: 12.423\" x 9.250\"")
print(f"Calculated: {FULL_WIDTH/DPI:.3f}\" x {FULL_HEIGHT/DPI:.3f}\"")

# Create cover
cover = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), '#f5f5dc')  # Cream
draw = ImageDraw.Draw(cover)

# Colors
DARK_GREEN = '#2d5016'
ACCENT_BLUE = '#667eea'
TEXT_DARK = '#333333'

# Try to load fonts
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 120)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 50)
    author_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 40)
    spine_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 35)
    back_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 30)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    author_font = ImageFont.load_default()
    spine_font = ImageFont.load_default()
    back_font = ImageFont.load_default()

# Calculate positions
back_left = BLEED
back_right = BLEED + TRIM_WIDTH
spine_left = back_right
spine_right = spine_left + SPINE_WIDTH
front_left = spine_right
front_right = front_left + TRIM_WIDTH

# --- FRONT COVER ---
front_center_x = front_left + TRIM_WIDTH//2

# Title
title_text = "THE QUAIL\nKEEPER'S\nJOURNAL"
draw.multiline_text((front_center_x, BLEED + 600), title_text, 
                    font=title_font, fill=DARK_GREEN, align='center',
                    anchor='mm')

# Subtitle
subtitle = "A Comprehensive Record Book\nfor Coturnix Quail Breeding"
draw.multiline_text((front_center_x, BLEED + 1100), subtitle,
                    font=subtitle_font, fill=TEXT_DARK, align='center',
                    anchor='mm')

# Decorative line
draw.line([(front_left + 200, BLEED + 1300), 
           (front_right - 200, BLEED + 1300)], 
          fill=ACCENT_BLUE, width=8)

# Quail eggs illustration
for i in range(3):
    egg_x = front_center_x - 150 + i*150
    draw.ellipse([(egg_x - 40, BLEED + 1600), 
                  (egg_x + 40, BLEED + 1700)], 
                 fill='#e8dcc5', outline='#d4c4a8', width=3)

# Author
author_text = "M4Quick Quail Farm"
draw.text((front_center_x, BLEED + 2000), author_text,
          font=author_font, fill=TEXT_DARK, align='center',
          anchor='mm')

# --- SPINE ---
spine_center_x = spine_left + SPINE_WIDTH//2

# Spine title (vertical)
spine_img = Image.new('RGB', (SPINE_WIDTH, TRIM_HEIGHT), '#f5f5dc')
spine_draw = ImageDraw.Draw(spine_img)

# Draw text centered on spine
spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT//2 - 400), 
                "THE QUAIL", font=spine_font, fill=DARK_GREEN, anchor='mm')
spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT//2), 
                "KEEPER'S", font=spine_font, fill=DARK_GREEN, anchor='mm')
spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT//2 + 400), 
                "JOURNAL", font=spine_font, fill=DARK_GREEN, anchor='mm')

# Author at bottom
spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT - 200), 
                "M4Quick", font=author_font, fill=TEXT_DARK, anchor='mm')

# Rotate and paste (text runs up the spine)
spine_rotated = spine_img.rotate(90, expand=True)
cover.paste(spine_rotated, (int(spine_left), int(BLEED)))

# --- BACK COVER ---
back_center_x = back_left + TRIM_WIDTH//2

# Back title
back_title = "Track Everything\nYou Need"
draw.multiline_text((back_center_x, BLEED + 400), back_title,
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

y_start = BLEED + 700
for feature in features:
    draw.text((back_left + 150, y_start), feature,
              font=back_font, fill=TEXT_DARK)
    y_start += 80

# Description
desc = "The essential companion for backyard quail\n" \
       "keepers and homesteaders. Track your flock\n" \
       "from egg to harvest with this comprehensive\n" \
       "journal designed specifically for Coturnix quail."
draw.multiline_text((back_center_x, BLEED + 1700), desc,
                    font=back_font, fill=TEXT_DARK, align='center',
                    anchor='mm')

# Barcode area (white box at bottom right of back cover)
barcode_left = back_right - 400
barcode_bottom = BLEED + TRIM_HEIGHT - 200
draw.rectangle([(barcode_left, barcode_bottom - 300), 
                (back_right - 100, barcode_bottom)],
               fill='white', outline='black', width=2)
draw.text((barcode_left + 150, barcode_bottom - 150), "[BARCODE]",
          font=back_font, fill='black', anchor='mm')

# Save with proper DPI
cover.save('Quail_Journal_Cover_v2.png', 'PNG', dpi=(DPI, DPI))
cover.save('Quail_Journal_Cover_v2.pdf', 'PDF', resolution=DPI)

print(f"\n✅ Cover saved!")
print(f"File: Quail_Journal_Cover_v2.pdf")
print(f"Dimensions: {FULL_WIDTH}x{FULL_HEIGHT} pixels")
print(f"In inches: {FULL_WIDTH/DPI:.3f}\" x {FULL_HEIGHT/DPI:.3f}\"")
