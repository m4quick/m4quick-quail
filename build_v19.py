#!/usr/bin/env python3
"""
Build Quail Hatch Video v19 - TIKTOK VIRAL STYLE
- ALL CAPS text
- Thick black outline (8-10px)
- Lower position (bottom third)
- Impact-style bold text
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v19.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v19_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_title_card(text, duration=3):
    """Viral style title - BIG, BOLD, CENTERED"""
    img = Image.new('RGB', (TARGET_W, TARGET_H), (20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to get a bold/heavy font
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
    except:
        title_font = ImageFont.load_default()
    
    lines = text.upper().split('\n')  # ALL CAPS
    total_height = len(lines) * 130
    start_y = (TARGET_H - total_height) // 2
    
    current_y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        # THICK viral-style outline (8-10px)
        for offset in range(10, 0, -1):
            draw.text((x-offset, current_y), line, font=title_font, fill=(0, 0, 0))
            draw.text((x+offset, current_y), line, font=title_font, fill=(0, 0, 0))
            draw.text((x, current_y-offset), line, font=title_font, fill=(0, 0, 0))
            draw.text((x, current_y+offset), line, font=title_font, fill=(0, 0, 0))
            draw.text((x-offset, current_y-offset), line, font=title_font, fill=(0, 0, 0))
            draw.text((x+offset, current_y+offset), line, font=title_font, fill=(0, 0, 0))
        
        # Bright white text for pop
        draw.text((x, current_y), line, font=title_font, fill=(255, 255, 255))
        current_y += 130
    
    img_array = np.array(img)
    clip = ImageClip(img_array, duration=duration)
    clip = clip.fadein(0.5).fadeout(0.5)
    
    return clip

def create_text_img(text, position="bottom"):
    """Viral TikTok style - ALL CAPS, thick outline, bottom position"""
    img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        # Larger font for impact
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    except:
        font = ImageFont.load_default()
    
    # ALL CAPS
    text = text.upper()
    lines = text.split('\n')
    line_heights = []
    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 20
    
    # Position: bottom third of screen (viral style)
    if position == "center":
        start_y = (TARGET_H - total_height) // 2
    else:
        start_y = TARGET_H - total_height - 200  # Bottom third with padding
    
    current_y = start_y
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        # THICK viral outline (8px)
        for offset in [8, 7, 6, 5, 4, 3, 2, 1]:
            draw.text((x-offset, current_y), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x+offset, current_y), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x, current_y-offset), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x, current_y+offset), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x-offset, current_y-offset), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x+offset, current_y+offset), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x-offset, current_y+offset), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x+offset, current_y-offset), line, font=font, fill=(0, 0, 0, 255))
        
        # Bright white fill
        draw.text((x, current_y), line, font=font, fill=(255, 255, 255, 255))
        
        current_y += line_heights[0] + 25
    
    return np.array(img)

def add_caption(video_clip, text, position="bottom"):
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

def build_v19():
    print("Building Quail Hatch Video v19 (TIKTOK VIRAL STYLE)...")
    print("Features: ALL CAPS, thick outline, bottom position")
    
    clips = []
    
    # === TITLE CARD ===
    print("Title: THE MIRACLE OF HATCHING!")
    title = create_title_card("THE MIRACLE\nOF HATCHING!", duration=3)
    clips.append(title)
    
    # === DAY 1 SETUP ===
    print("Scene 1: PERFECT CONDITIONS")
    setup_clip = extract_clip(f"{INPUT_DIR}/IMG_0123.MOV", 0, 8)
    setup_vertical = convert_to_vertical(setup_clip, final_zoom=1.1)
    setup_scene = add_caption(setup_vertical, "PERFECT CONDITIONS\nFOR DAY 1", "bottom")
    clips.append(setup_scene)
    setup_clip.close()
    
    print("Scene 2: TEMPERATURE")
    temp_clip = extract_clip(f"{INPUT_DIR}/IMG_0123.MOV", 8, 6)
    temp_vertical = convert_to_vertical(temp_clip, final_zoom=1.0)
    temp_scene = add_caption(temp_vertical, "TEMP 99.5F OR 37.5C", "bottom")
    clips.append(temp_scene)
    temp_clip.close()
    
    print("Scene 3: HUMIDITY")
    hum_clip = extract_clip(f"{INPUT_DIR}/IMG_0123.MOV", 14, 5)
    hum_vertical = convert_to_vertical(hum_clip, final_zoom=1.0)
    hum_scene = add_caption(hum_vertical, "HUMIDITY SHOULD BE LOW\nat this point", "bottom")
    clips.append(hum_scene)
    hum_clip.close()
    
    # Scene 4: Day 17
    print("Scene 4: DAY 17")
    egg_clip = extract_clip(f"{INPUT_DIR}/IMG_6093.MOV", 10, 3)
    egg_vertical = convert_to_vertical(egg_clip, final_zoom=1.15)
    egg_scene = add_caption(egg_vertical, "DAY 17...", "bottom")
    clips.append(egg_scene)
    egg_clip.close()
    
    # Scene 5: The struggle
    print("Scene 5: THE STRUGGLE")
    effort_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 35, 15, slow_factor=0.5)
    effort_vertical = convert_to_vertical(effort_clip, final_zoom=1.0)
    effort_scene = add_caption(effort_vertical, "THIS IS A TUFF EGG\nTO CRACK", "bottom")
    clips.append(effort_scene)
    effort_clip.close()
    
    # Scene 6: The nap
    print("Scene 6: THE NAP")
    nap_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 60, 8, slow_factor=0.6)
    nap_vertical = convert_to_vertical(nap_clip, final_zoom=1.0)
    nap_scene = add_caption(nap_vertical, "QUICK NAP...\nBACK TO WORK SOON", "bottom")
    clips.append(nap_scene)
    nap_clip.close()
    
    # Scene 7: Here we go!
    print("Scene 7: HERE WE GO!")
    hatch_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 95, 4, slow_factor=0.5)
    hatch_vertical = convert_to_vertical(hatch_clip, final_zoom=1.0)
    hatch_scene = add_caption(hatch_vertical, "HERE WE GO!", "bottom")
    hatch_scene = hatch_scene.fadeout(0.5)
    clips.append(hatch_scene)
    hatch_clip.close()
    
    # Scene 8: First hatchlings
    print("Scene 8: FIRST HATCHLINGS")
    first_clip = extract_clip(f"{INPUT_DIR}/IMG_6107.MOV", 5, 5)
    first_vertical = convert_to_vertical(first_clip, final_zoom=1.0)
    first_scene = add_caption(first_vertical, "IT'S STARTING!", "bottom")
    first_scene = first_scene.fadein(0.5)
    clips.append(first_scene)
    first_clip.close()
    
    # Scene 9: Humidity tip
    print("Scene 9: HUMIDITY TIP")
    tip_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 110, 6, slow_factor=0.5)
    tip_vertical = convert_to_vertical(tip_clip, final_zoom=1.0)
    tip_scene = add_caption(tip_vertical, "HIGHER HUMIDITY HELPS\nTHE SHELLS BREAK EASIER", "bottom")
    clips.append(tip_scene)
    tip_clip.close()
    
    # Scene 10: FREEDOM
    print("Scene 10: FREEDOM!")
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 2, 6, slow_factor=0.5)
    emerge_vertical = convert_to_vertical(emerge_clip, final_zoom=1.0)
    emerge_scene = add_caption(emerge_vertical, "FREEDOM!", "center")
    clips.append(emerge_scene)
    emerge_clip.close()
    
    # Scene 11: Brooder finale
    print("Scene 11: LIVING THEIR BEST LIFE")
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 5, 15)
    brooder_vertical = convert_to_vertical(brooder_clip, final_zoom=1.0)
    brooder_scene = add_caption(brooder_vertical, "LIVING THEIR BEST LIFE", "center")
    clips.append(brooder_scene)
    brooder_clip.close()
    
    # Scene 12: End card
    print("End card")
    end_title = create_title_card("THE END", duration=2)
    clips.append(end_title)
    
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
    print(f"\nExporting v19 to {OUTPUT}")
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
    
    print("\n✅ v19 ready! Viral TikTok style.")
    
    final.close()
    for clip in clips:
        clip.close()
    audio.close()

if __name__ == "__main__":
    build_v19()
