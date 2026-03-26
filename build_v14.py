#!/usr/bin/env python3
"""
Build Quail Hatch Video v14 - FIXED AGAIN
- Replace IMG_6138 (brooder) with IMG_6107 (incubator)
- Add humidity caption during hatch
- Brooder ONLY at end
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v14.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v14_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_text_img(text, position="top"):
    img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
    except:
        font = ImageFont.load_default()
    
    lines = text.split('\n')
    line_heights = []
    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 12
    
    if position == "center":
        start_y = (TARGET_H - total_height) // 2
    else:
        start_y = 180
    
    current_y = start_y
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, -3), (0, 3), (-3, 0), (3, 0)]:
            draw.text((x + dx, current_y + dy), line, font=font, fill=(0, 0, 0, 255))
        draw.text((x, current_y), line, font=font, fill=(255, 255, 255, 255))
        
        current_y += line_heights[0] + 15
    
    return np.array(img)

def add_caption(video_clip, text, position="top"):
    txt_img = create_text_img(text, position)
    txt_clip = ImageClip(txt_img, duration=video_clip.duration)
    return CompositeVideoClip([video_clip, txt_clip])

def extract_clip(video_path, start, duration, slow_factor=1.0):
    clip = VideoFileClip(video_path).subclip(start, start + duration)
    if slow_factor != 1.0:
        clip = clip.fx(vfx.speedx, slow_factor)
    return clip

def convert_to_vertical(clip, final_zoom=1.0):
    frames = []
    fps = 30
    num_frames = int(clip.duration * fps)
    
    for i in range(num_frames):
        t = i / fps
        if t >= clip.duration:
            t = clip.duration - 0.001
        frame = clip.get_frame(t)
        h, w = frame.shape[:2]
        
        pil_img = Image.fromarray(frame)
        progress = i / num_frames if num_frames > 1 else 0
        current_zoom = 1 + (final_zoom - 1) * progress
        
        if w > h:  # Horizontal
            target_w = int(h * 0.5625)
            if target_w > w:
                target_h = int(w / 0.5625)
                top = (h - target_h) // 2
                cropped = pil_img.crop((0, top, w, top + target_h))
            else:
                left = (w - target_w) // 2
                cropped = pil_img.crop((left, 0, left + target_w, h))
            resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        else:  # Vertical
            zoom_w = int(w / current_zoom)
            zoom_h = int(h / current_zoom)
            left = (w - zoom_w) // 2
            top = (h - zoom_h) // 2
            cropped = pil_img.crop((left, top, left + zoom_w, top + zoom_h))
            resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        
        frames.append(np.array(resized))
    
    return ImageSequenceClip(frames, fps=fps)

def build_v14():
    print("Building Quail Hatch Video v14 (BROODER-FREE MIDDLE)...")
    
    clips = []
    
    # ===== DAY 1 SETUP (TODAY) =====
    print("Scene 1: Perfect conditions")
    setup_clip = extract_clip(f"{INPUT_DIR}/IMG_0123.MOV", 0, 8)
    setup_vertical = convert_to_vertical(setup_clip, final_zoom=1.1)
    setup_scene = add_caption(setup_vertical, "Perfect conditions for Day 1", "top")
    clips.append(setup_scene)
    setup_clip.close()
    
    print("Scene 2: Temperature")
    temp_clip = extract_clip(f"{INPUT_DIR}/IMG_0123.MOV", 8, 6)
    temp_vertical = convert_to_vertical(temp_clip, final_zoom=1.0)
    temp_scene = add_caption(temp_vertical, "Temp 99.5°F or 37.5°C", "top")
    clips.append(temp_scene)
    temp_clip.close()
    
    print("Scene 3: Humidity")
    hum_clip = extract_clip(f"{INPUT_DIR}/IMG_0123.MOV", 14, 6)
    hum_vertical = convert_to_vertical(hum_clip, final_zoom=1.0)
    hum_scene = add_caption(hum_vertical, "Humidity should be low\\nat this point", "top")
    clips.append(hum_scene)
    hum_clip.close()
    
    # ===== FLASHBACK: HATCHING =====
    print("Scene 4: Day 17 flashback")
    egg_clip = extract_clip(f"{INPUT_DIR}/IMG_6093.MOV", 10, 5)
    egg_vertical = convert_to_vertical(egg_clip, final_zoom=1.15)
    egg_scene = add_caption(egg_vertical, "Day 17...", "top")
    clips.append(egg_scene)
    egg_clip.close()
    
    # ===== USE IMG_6107 (wet chicks) instead of IMG_6138 (brooder) =====
    print("Scene 5: First hatchlings - NOT brooder")
    first_clip = extract_clip(f"{INPUT_DIR}/IMG_6107.MOV", 5, 5)
    first_vertical = convert_to_vertical(first_clip, final_zoom=1.0)
    first_scene = add_caption(first_vertical, "It's starting!", "top")
    clips.append(first_scene)
    first_clip.close()
    
    print("Scene 6: The struggle")
    effort_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 20, 15, slow_factor=0.5)
    effort_vertical = convert_to_vertical(effort_clip, final_zoom=1.0)
    effort_scene = add_caption(effort_vertical, "This is a tuff egg\\nto crack", "top")
    clips.append(effort_scene)
    effort_clip.close()
    
    print("Scene 7: The nap")
    nap_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 60, 8, slow_factor=0.6)
    nap_vertical = convert_to_vertical(nap_clip, final_zoom=1.0)
    nap_scene = add_caption(nap_vertical, "Quick nap...\\nback to work soon", "top")
    clips.append(nap_scene)
    nap_clip.close()
    
    # ===== ACTIVE HATCH with humidity caption =====
    print("Scene 8: ACTIVE HATCH")
    hatch_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 95, 10, slow_factor=0.5)
    hatch_vertical = convert_to_vertical(hatch_clip, final_zoom=1.0)
    hatch_scene = add_caption(hatch_vertical, "Here we go!", "top")
    clips.append(hatch_scene)
    hatch_clip.close()
    
    # ===== ADD HUMIDITY TIP during hatch =====
    print("Scene 9: Humidity tip")
    tip_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 110, 8, slow_factor=0.5)
    tip_vertical = convert_to_vertical(tip_clip, final_zoom=1.0)
    tip_scene = add_caption(tip_vertical, "Higher Humidity at least 75%\\nmakes it easier to break 🐣", "top")
    clips.append(tip_scene)
    tip_clip.close()
    
    print("Scene 10: FREEDOM")
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 2, 6, slow_factor=0.5)
    emerge_vertical = convert_to_vertical(emerge_clip, final_zoom=1.0)
    emerge_scene = add_caption(emerge_vertical, "FREEDOM!", "center")
    clips.append(emerge_scene)
    emerge_clip.close()
    
    # ===== BROODER FINALE ONLY =====
    print("Scene 11: Brooder finale")
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 5, 15)
    brooder_vertical = convert_to_vertical(brooder_clip, final_zoom=1.0)
    brooder_scene = add_caption(brooder_vertical, "Living their best life", "center")
    clips.append(brooder_scene)
    brooder_clip.close()
    
    # Combine
    print("\nCombining all scenes...")
    final = concatenate_videoclips(clips, method="compose")
    
    total_duration = sum([c.duration for c in clips])
    print(f"Total duration: {total_duration:.1f}s")
    
    # Add audio
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final.duration:
        n_loops = int(final.duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, final.duration).volumex(0.4)
    final = final.set_audio(audio)
    
    # Export
    print(f"\nExporting v14 to {OUTPUT}")
    final.write_videofile(
        OUTPUT,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="8000k",
        threads=4,
        preset="medium",
        logger=None
    )
    
    print("\n✅ v14 ready! No brooder in middle, added humidity tip.")
    
    final.close()
    for clip in clips:
        clip.close()
    audio.close()

if __name__ == "__main__":
    build_v14()
