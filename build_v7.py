#!/usr/bin/env python3
"""
Add humorous captions to Quail Hatch Video v6 -> v7
"""

import os
import sys
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

INPUT = "/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v6.mp4"
OUTPUT = "/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v7.mp4"
AUDIO = "/Users/mirzaie/Pictures/QuailHatch/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v7_build"
TARGET_W, TARGET_H = 1080, 1920

os.makedirs(WORKSPACE, exist_ok=True)

# Caption schedule: (start_time, end_time, text, position)
# position: "top" or "center"
captions = [
    (0, 7, "Day 17...", "top"),
    (7, 12, "This is a tuff egg\nto crack", "top"),
    (12, 20, "Almost there...", "top"),
    (20, 26, "FREEDOM!", "center"),
    (26, 31, "Just a little wet\nbehind the ears", "top"),
    (31, 39, "All they think about is\nfood and water", "top"),
    (39, 45, "Living their best life", "center"),
]

def create_text_image(text, position):
    """Create a text overlay image."""
    img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 64)
    except:
        font = ImageFont.load_default()
    
    # Handle multi-line text
    lines = text.split('\n')
    total_height = 0
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 10
    
    if position == "center":
        start_y = (TARGET_H - total_height) // 2
    else:  # top
        start_y = 150
    
    current_y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        # Draw stroke/outline
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, -3), (0, 3), (-3, 0), (3, 0)]:
            draw.text((x + dx, current_y + dy), line, font=font, fill=(0, 0, 0, 255))
        # Draw text
        draw.text((x, current_y), line, font=font, fill=(255, 255, 255, 255))
        
        current_y += line_heights[0] + 15
    
    return np.array(img)

print("Loading video...")
video = VideoFileClip(INPUT)

# Create text clips
print("Creating captions...")
text_clips = []
for start, end, text, position in captions:
    # Create text overlay
    txt_img = create_text_image(text, position)
    txt_clip = (ImageClip(txt_img)
                .set_duration(end - start)
                .set_start(start))
    text_clips.append(txt_clip)

# Composite everything
print("Compositing...")
final = CompositeVideoClip([video] + text_clips)

# Add audio
print("Adding audio...")
audio = AudioFileClip(AUDIO)
if audio.duration < final.duration:
    n_loops = int(final.duration / audio.duration) + 1
    audio = concatenate_audioclips([audio] * n_loops)
audio = audio.subclip(0, final.duration).volumex(0.4)
final = final.set_audio(audio)

# Export
print(f"\nExporting to {OUTPUT}")
final.write_videofile(
    OUTPUT,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    bitrate="6000k",
    threads=4,
    preset="medium"
)

print("\n✅ v7 is ready with captions!")
final.close()
video.close()
