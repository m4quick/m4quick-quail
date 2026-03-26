#!/usr/bin/env python3
"""
Build Quail Hatch Video v20 - SHORTS VERSION
- Under 60 seconds for YouTube Shorts
- Fast-paced, viral moments only
- TikTok style: ALL CAPS, thick outline, bottom position
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v20_SHORTS.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v20_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_title_card(text, duration=2):
    """Fast title for Shorts"""
    img = Image.new('RGB', (TARGET_W, TARGET_H), (20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 110)
    except:
        title_font = ImageFont.load_default()
    
    lines = text.upper().split('\n')
    total_height = len(lines) * 140
    start_y = (TARGET_H - total_height) // 2
    
    current_y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        # Thick outline
        for offset in range(10, 0, -1):
            draw.text((x-offset, current_y), line, font=title_font, fill=(0, 0, 0))
            draw.text((x+offset, current_y), line, font=title_font, fill=(0, 0, 0))
            draw.text((x, current_y-offset), line, font=title_font, fill=(0, 0, 0))
            draw.text((x, current_y+offset), line, font=title_font, fill=(0, 0, 0))
        
        draw.text((x, current_y), line, font=title_font, fill=(255, 255, 255))
        current_y += 140
    
    img_array = np.array(img)
    clip = ImageClip(img_array, duration=duration)
    clip = clip.fadein(0.3).fadeout(0.3)
    
    return clip

def create_text_img(text, position="bottom"):
    """Viral TikTok style"""
    img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 76)
    except:
        font = ImageFont.load_default()
    
    text = text.upper()
    lines = text.split('\n')
    line_heights = []
    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 20
    
    if position == "center":
        start_y = (TARGET_H - total_height) // 2
    else:
        start_y = TARGET_H - total_height - 180
    
    current_y = start_y
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        # Thick outline
        for offset in [8, 7, 6, 5, 4, 3, 2, 1]:
            draw.text((x-offset, current_y), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x+offset, current_y), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x, current_y-offset), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x, current_y+offset), line, font=font, fill=(0, 0, 0, 255))
        
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
        
        if w > h:
            target_w = int(h * 0.5625)
            if target_w > w:
                target_h = int(w / 0.5625)
                top = (h - target_h) // 2
                cropped = pil_img.crop((0, top, w, top + target_h))
            else:
                left = (w - target_w) // 2
                cropped = pil_img.crop((left, 0, left + target_w, h))
            resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        else:
            zoom_w = int(w / current_zoom)
            zoom_h = int(h / current_zoom)
            left = (w - zoom_w) // 2
            top = (h - zoom_h) // 2
            cropped = pil_img.crop((left, top, left + zoom_w, top + zoom_h))
            resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        
        frames.append(np.array(resized))
    
    return ImageSequenceClip(frames, fps=fps)

def build_v20():
    print("Building Quail Hatch Video v20 - SHORTS VERSION...")
    print("Fast-paced, viral moments only, under 60 seconds")
    
    clips = []
    
    # === FAST TITLE ===
    print("Title: THE MIRACLE OF HATCHING!")
    title = create_title_card("THE MIRACLE\nOF HATCHING!", duration=2)
    clips.append(title)
    
    # === DAY 17 FLASHBACK (quick) ===
    print("Scene 1: DAY 17")
    egg_clip = extract_clip(f"{INPUT_DIR}/IMG_6093.MOV", 10, 2)
    egg_vertical = convert_to_vertical(egg_clip, final_zoom=1.15)
    egg_scene = add_caption(egg_vertical, "DAY 17...", "bottom")
    clips.append(egg_scene)
    egg_clip.close()
    
    # === THE STRUGGLE (hero moment) ===
    print("Scene 2: THE STRUGGLE")
    effort_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 35, 10, slow_factor=0.5)
    effort_vertical = convert_to_vertical(effort_clip, final_zoom=1.0)
    effort_scene = add_caption(effort_vertical, "THIS IS A TUFF EGG\nTO CRACK", "bottom")
    clips.append(effort_scene)
    effort_clip.close()
    
    # === HERE WE GO! (climax) ===
    print("Scene 3: HERE WE GO!")
    hatch_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 95, 4, slow_factor=0.5)
    hatch_vertical = convert_to_vertical(hatch_clip, final_zoom=1.0)
    hatch_scene = add_caption(hatch_vertical, "HERE WE GO!", "bottom")
    clips.append(hatch_scene)
    hatch_clip.close()
    
    # === FREEDOM! (big moment) ===
    print("Scene 4: FREEDOM!")
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 2, 5, slow_factor=0.5)
    emerge_vertical = convert_to_vertical(emerge_clip, final_zoom=1.0)
    emerge_scene = add_caption(emerge_vertical, "FREEDOM!", "center")
    clips.append(emerge_scene)
    emerge_clip.close()
    
    # === BROODER FINALE (happy ending) ===
    print("Scene 5: LIVING THEIR BEST LIFE")
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 5, 10)
    brooder_vertical = convert_to_vertical(brooder_clip, final_zoom=1.0)
    brooder_scene = add_caption(brooder_vertical, "LIVING THEIR BEST LIFE", "center")
    clips.append(brooder_scene)
    brooder_clip.close()
    
    # === QUICK END ===
    print("End card")
    end_title = create_title_card("THE END", duration=1.5)
    clips.append(end_title)
    
    # Combine
    print("\nCombining Shorts version...")
    final = concatenate_videoclips(clips, method="compose")
    
    total_duration = sum([c.duration for c in clips])
    print(f"Total duration: {total_duration:.1f}s")
    
    # Add audio
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final.duration:
        n_loops = int(final.duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, final.duration).volumex(0.5)
    final = final.set_audio(audio)
    
    # Export
    print(f"\nExporting v20 Shorts to {OUTPUT}")
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
    
    print("\n✅ v20 Shorts ready! Under 60 seconds.")
    
    final.close()
    for clip in clips:
        clip.close()
    audio.close()

if __name__ == "__main__":
    build_v20()
