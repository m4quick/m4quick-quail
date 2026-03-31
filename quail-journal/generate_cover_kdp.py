from PIL import Image, ImageDraw, ImageFont

# KDP REQUIRED dimensions (inches at 300 DPI)
# Total: 12.423" x 9.250"
# Trim: 6" x 9", Bleed: 0.125" all sides, Spine: 0.173"
DPI = 300

FULL_WIDTH = int(12.423 * DPI)   # 3727 pixels
FULL_HEIGHT = int(9.250 * DPI)   # 2775 pixels
BLEED = int(0.125 * DPI)         # 37.5 pixels
TRIM_WIDTH = int(6 * DPI)        # 1800 pixels  
TRIM_HEIGHT = int(9 * DPI)       # 2700 pixels
SPINE_WIDTH = int(0.173 * DPI)   # 52 pixels (calculated to match KDP)

print(f"Cover: {FULL_WIDTH}x{FULL_HEIGHT} pixels ({FULL_WIDTH/DPI:.3f}\" x {FULL_HEIGHT/DPI:.3f}\")")

# Create cover
cover = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), '#f5f5dc')
draw = ImageDraw.Draw(cover)

# Colors
DARK_GREEN = '#2d5016'
ACCENT_BLUE = '#667eea'
TEXT_DARK = '#333333'

# Load fonts
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

# Simple egg shapes (no hands!)
for i in range(3):
    egg_x = front_center_x - 150 + i*150
    draw.ellipse([(egg_x - 40, BLEED + 1600), 
                  (egg_x + 40, BLEED + 1700)], 
                 fill='#e8dcc5', outline='#d4c4a8', width=3)

# Author
author_text = "M4Quick Quail Farm"
draw.text((front_center_x, BLEED + 2000), author_text,
          font=author_font, fill=TEXT_DARK, anchor='mm')

# --- SPINE ---
spine_img = Image.new('RGB', (SPINE_WIDTH, TRIM_HEIGHT), '#f5f5dc')
spine_draw = ImageDraw.Draw(spine_img)

spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT//2 - 400), 
                "THE QUAIL", font=spine_font, fill=DARK_GREEN, anchor='mm')
spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT//2), 
                "KEEPER'S", font=spine_font, fill=DARK_GREEN, anchor='mm')
spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT//2 + 400), 
                "JOURNAL", font=spine_font, fill=DARK_GREEN, anchor='mm')
spine_draw.text((SPINE_WIDTH//2, TRIM_HEIGHT - 200), 
                "M4Quick", font=author_font, fill=TEXT_DARK, anchor='mm')

spine_rotated = spine_img.rotate(90, expand=True)
cover.paste(spine_rotated, (int(spine_left), int(BLEED)))

# --- BACK COVER ---
back_center_x = back_left + TRIM_WIDTH//2

back_title = "Track Everything\nYou Need"
draw.multiline_text((back_center_x, BLEED + 400), back_title,
                    font=subtitle_font, fill=DARK_GREEN, align='center',
                    anchor='mm')

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
    draw.text((back_left + 150, y_start), feature, font=back_font, fill=TEXT_DARK)
    y_start += 80

desc = "The essential companion for backyard quail\n" \
       "keepers and homesteaders. Track your flock\n" \
       "from egg to harvest with this comprehensive\n" \
       "journal designed specifically for Coturnix quail."
draw.multiline_text((back_center_x, BLEED + 1700), desc,
                    font=back_font, fill=TEXT_DARK, align='center',
                    anchor='mm')

# Barcode area (white box)
barcode_left = back_right - 400
barcode_bottom = BLEED + TRIM_HEIGHT - 200
draw.rectangle([(barcode_left, barcode_bottom - 300), 
                (back_right - 100, barcode_bottom)],
               fill='white', outline='black', width=2)

# Save
cover.save('Quail_Journal_Cover_KDP.pdf', 'PDF', resolution=DPI)
cover.save('Quail_Journal_Cover_KDP.png', 'PNG', dpi=(DPI, DPI))

print(f"✅ Cover saved: Quail_Journal_Cover_KDP.pdf")
print(f"Dimensions: {FULL_WIDTH/DPI:.3f}\" x {FULL_HEIGHT/DPI:.3f}\"")

# Copy to Desktop
import shutil
shutil.copy('Quail_Journal_Cover_KDP.pdf', '/Users/mirzaie/Desktop/')
print(f"✅ Copied to Desktop")
