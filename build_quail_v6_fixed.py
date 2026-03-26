#!/usr/bin/env python3
"""
Build Quail Hatch Video v6 - "The Miracle of Hatching"
"""

import os
import sys
from moviepy.editor import *
from moviepy.video.fx.all import resize
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Settings
OUTPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace"
TARGET_W, TARGET_H = 1080, 1920  # 9:16 vertical
FPS = 30
BITRATE = "6000k"

def create_text_clip(text, duration, position="center"):
    """Create a text overlay as a transparent PNG ImageClip."""
    img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (TARGET_W - text_width) // 2
    
    if position == "center":
        y = (TARGET_H - text_height) // 2
    elif position == "top":
        y = 150
    else:
        y = TARGET_H - 250
    
    # Draw stroke
    for dx, dy in [(-4, -4), (-4, 4), (4, -4), (4, 4), (0, -4), (0, 4), (-4, 0), (4, 0)]:
        draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 255))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    temp_path = f"{WORKSPACE}/temp_text_{hash(text) % 10000}.png"
    img.save(temp_path)
    clip = ImageClip(temp_path, duration=duration)
    return clip

def process_video_for_vertical(video_path, start_time, duration):
    """Load a video, extract segment, and make it vertical 9:16."""
    clip = VideoFileClip(video_path).subclip(start_time, start_time + duration)
    w, h = clip.size
    
    if w > h:  # Horizontal video - need to crop
        # Scale to target height first
        scale_factor = TARGET_H / h
        new_w = int(w * scale_factor)
        
        # Use ffmpeg directly for resize to avoid PIL issues
        def resize_frame(frame):
            pil_img = Image.fromarray(frame)
            pil_img = pil_img.resize((new_w, TARGET_H), Image.Resampling.LANCZOS)
            return np.array(pil_img)
        
        clip = clip.fl_image(resize_frame)
        # Crop to center
        crop_x = (new_w - TARGET_W) // 2
        clip = clip.crop(x1=crop_x, y1=0, x2=crop_x + TARGET_W, y2=TARGET_H)
    else:  # Already vertical
        if w != TARGET_W or h != TARGET_H:
            def resize_frame(frame):
                pil_img = Image.fromarray(frame)
                pil_img = pil_img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
                return np.array(pil_img)
            clip = clip.fl_image(resize_frame)
    
    return clip

# Build the narrative
print("Building Quail Hatch v6 - 'The Miracle of Hatching'")
print("=" * 50)

clips = []

# Scene 1: "The Wait"
print("Scene 1: The Wait")
clip1 = process_video_for_vertical(f"{INPUT_DIR}/IMG_6093.MOV", 10, 7)
text1 = create_text_clip("Day 17...", 2, "top")
clips.append(CompositeVideoClip([clip1, text1]))

# Scene 2: "The First Sign" - Pipping
print("Scene 2: The First Sign")
clip2 = process_video_for_vertical(f"{INPUT_DIR}/IMG_6138.MOV", 5, 5)
text2 = create_text_clip("It's starting!", 2, "top")
clips.append(CompositeVideoClip([clip2, text2]))

# Scene 3: "The Struggle"
print("Scene 3: The Struggle")
clip3 = process_video_for_vertical(f"{INPUT_DIR}/IMG_7081.MOV", 30, 8)
text3 = create_text_clip("So much effort...", 2, "top")
clips.append(CompositeVideoClip([clip3, text3]))

# Scene 4: "The Breakthrough"
print("Scene 4: The Breakthrough")
clip4 = process_video_for_vertical(f"{INPUT_DIR}/IMG_7081.MOV", 60, 6)
text4 = create_text_clip("Welcome!", 2, "top")
clips.append(CompositeVideoClip([clip4, text4]))

# Scene 5: "Wet and New"
print("Scene 5: Wet and New")
clip5 = process_video_for_vertical(f"{INPUT_DIR}/IMG_7082.MOV", 2, 5)
text5 = create_text_clip("Just born", 2, "top")
clips.append(CompositeVideoClip([clip5, text5]))

# Scene 6: "The Brooder"
print("Scene 6: The Brooder")
clip6 = process_video_for_vertical(f"{INPUT_DIR}/IMG_6118.MOV", 5, 8)
text6 = create_text_clip("All dry and fluffy", 2, "top")
clips.append(CompositeVideoClip([clip6, text6]))

# Scene 7: Final
print("Scene 7: The Miracle")
clip7 = process_video_for_vertical(f"{INPUT_DIR}/IMG_7083.MOV", 5, 6)
text7 = create_text_clip("The miracle of life", 2.5, "center")
clips.append(CompositeVideoClip([clip7, text7]))

# Combine
print("\nCombining scenes...")
final_video = concatenate_videoclips(clips, method="compose")

# Add audio
print("Adding audio...")
audio = AudioFileClip(f"{INPUT_DIR}/ukulele_source.m4a")

if audio.duration < final_video.duration:
    n_loops = int(final_video.duration / audio.duration) + 1
    audio = concatenate_audioclips([audio] * n_loops)

audio = audio.subclip(0, final_video.duration).volumex(0.4)
final_video = final_video.set_audio(audio)

# Export
output_path = f"{OUTPUT_DIR}/QuailHatchVideo_v6.mp4"
print(f"\nExporting to {output_path}")
print(f"Duration: {final_video.duration:.1f}s")

final_video.write_videofile(
    output_path,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    bitrate=BITRATE,
    threads=4,
    preset="medium"
)

print("\n✅ Done!")
final_video.close()
