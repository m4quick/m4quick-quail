#!/usr/bin/env python3
"""
Build Quail Hatch Video v23b - SHORTS VERSION
- Documentary style but under 60s for YouTube Shorts
- Trimmed scenes, faster pacing
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
os.environ['PYTHONPATH'] = '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages'
from moviepy.editor import *
from moviepy.video.fx.all import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v23b_SHORTS.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v23b_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_text(text, font_size=72, position="bottom"):
    """Create text with smooth Gaussian blur shadow"""
    padding = 60
    img = Image.new('RGBA', (TARGET_W + padding*2, TARGET_H + padding*2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    lines = text.upper().split('\n')
    line_heights = []
    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 18
    
    # Position
    if position == "center":
        start_y = ((TARGET_H + padding*2) - total_height) // 2
    else:  # bottom third
        start_y = (TARGET_H + padding*2) - total_height - 200
    
    positions = []
    current_y = start_y
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = ((TARGET_W + padding*2) - text_width) // 2
        positions.append((x, current_y, line))
        current_y += line_heights[0] + 20
    
    # Shadow layer (black, blurred)
    shadow = Image.new('RGBA', (TARGET_W + padding*2, TARGET_H + padding*2), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    for x, y, line in positions:
        shadow_draw.text((x, y), line, font=font, fill=(0, 0, 0, 255))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=7))
    
    # Text layer (white)
    text_layer = Image.new('RGBA', (TARGET_W + padding*2, TARGET_H + padding*2), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    for x, y, line in positions:
        text_draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
    
    # Composite
    result = Image.alpha_composite(shadow, text_layer)
    result = result.crop((padding, padding, TARGET_W + padding, TARGET_H + padding))
    
    return np.array(result)

def create_title_card(text, subtitle=None, duration=2):
    """Cinematic title with optional subtitle"""
    img = Image.new('RGB', (TARGET_W, TARGET_H), (15, 15, 30))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
        sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
    
    # Main title
    lines = text.upper().split('\n')
    total_height = len(lines) * 120
    if subtitle:
        total_height += 80
    start_y = (TARGET_H - total_height) // 2
    
    current_y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        # Shadow
        shadow_img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_draw.text((x, current_y), line, font=title_font, fill=(0, 0, 0, 255))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=10))
        
        # Text
        text_img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((x, current_y), line, font=title_font, fill=(255, 255, 255, 255))
        
        combined = Image.alpha_composite(shadow_img, text_img)
        img.paste(combined, (0, 0), combined)
        current_y += 120
    
    # Subtitle
    if subtitle:
        current_y += 20
        bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        shadow_img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_draw.text((x, current_y), subtitle, font=sub_font, fill=(0, 0, 0, 255))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=6))
        
        text_img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((x, current_y), subtitle, font=sub_font, fill=(200, 200, 220, 255))
        
        combined = Image.alpha_composite(shadow_img, text_img)
        img.paste(combined, (0, 0), combined)
    
    clip = ImageClip(np.array(img), duration=duration)
    return clip.fadein(0.3).fadeout(0.3)

def add_caption(video_clip, text, position="bottom"):
    txt_array = create_text(text, font_size=70, position=position)
    txt_clip = ImageClip(txt_array, duration=video_clip.duration)
    return CompositeVideoClip([video_clip, txt_clip])

def extract_clip(video_path, start, duration, slow_factor=1.0):
    clip = VideoFileClip(video_path).subclip(start, start + duration)
    if slow_factor != 1.0:
        clip = clip.fx(vfx.speedx, slow_factor)
    return clip

def process_vertical_clip(clip, final_zoom=1.0):
    """Process already-vertical clips (1080x1920) with optional zoom"""
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
        
        zoom_w = int(w / current_zoom)
        zoom_h = int(h / current_zoom)
        left = (w - zoom_w) // 2
        top = (h - zoom_h) // 2
        cropped = pil_img.crop((left, top, left + zoom_w, top + zoom_h))
        resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        
        frames.append(np.array(resized))
    
    return ImageSequenceClip(frames, fps=fps)

def convert_horizontal_to_vertical(clip, final_zoom=1.0):
    """Convert horizontal clips to vertical 9:16"""
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
            # Horizontal: crop sides to get 9:16
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

def build_v23b():
    print("Building Quail Hatch Video v23b - SHORTS VERSION (under 60s)")
    
    clips = []
    
    # === OPENING === (2s)
    print("Opening title...")
    title = create_title_card("THE HATCH", "Day 17", duration=2)
    clips.append(title)
    
    # === SCENE 1: Incubator with temp === (4s)
    print("Scene 1: Incubator...")
    inc_clip = extract_clip(f"{INPUT_DIR}/IMG_6138.MOV", 0, 4)
    inc_processed = process_vertical_clip(inc_clip, final_zoom=1.05)
    inc_scene = add_caption(inc_processed, "99.6°F | 55% HUMIDITY", "bottom")
    clips.append(inc_scene)
    inc_clip.close()
    
    # === SCENE 2: First pip (struggle) === (6s)
    print("Scene 2: The struggle...")
    struggle_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 35, 6, slow_factor=0.5)
    struggle_vertical = convert_horizontal_to_vertical(struggle_clip, final_zoom=1.0)
    struggle_scene = add_caption(struggle_vertical, "FIRST PIP", "center")
    clips.append(struggle_scene)
    struggle_clip.close()
    
    # === SCENE 3: Breaking through === (3s)
    print("Scene 3: Breaking through...")
    break_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 95, 3, slow_factor=0.5)
    break_vertical = convert_horizontal_to_vertical(break_clip, final_zoom=1.0)
    break_scene = add_caption(break_vertical, "ALMOST THERE", "bottom")
    clips.append(break_scene)
    break_clip.close()
    
    # === SCENE 4: Freedom! === (4s)
    print("Scene 4: Freedom...")
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_6144.MOV", 5, 4)
    emerge_processed = process_vertical_clip(emerge_clip, final_zoom=1.0)
    emerge_scene = add_caption(emerge_processed, "WELCOME!", "center")
    clips.append(emerge_scene)
    emerge_clip.close()
    
    # === SCENE 5: Resting === (4s)
    print("Scene 5: Resting...")
    rest_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 0, 4, slow_factor=0.6)
    rest_vertical = convert_horizontal_to_vertical(rest_clip, final_zoom=1.0)
    rest_scene = add_caption(rest_vertical, "EXHAUSTED\nBUT ALIVE", "center")
    clips.append(rest_scene)
    rest_clip.close()
    
    # === SCENE 6: Brooder === (4s)
    print("Scene 6: Brooder...")
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_7091.MOV", 0, 4)
    brooder_processed = process_vertical_clip(brooder_clip, final_zoom=1.0)
    brooder_scene = add_caption(brooder_processed, "NEW HOME", "bottom")
    clips.append(brooder_scene)
    brooder_clip.close()
    
    # === SCENE 7: Thriving === (5s)
    print("Scene 7: Thriving...")
    thrive_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 3, 5)
    thrive_vertical = convert_horizontal_to_vertical(thrive_clip, final_zoom=1.0)
    thrive_scene = add_caption(thrive_vertical, "LIVING THEIR\nBEST LIFE", "bottom")
    clips.append(thrive_scene)
    thrive_clip.close()
    
    # === END === (2s)
    print("End card...")
    end = create_title_card("12 CHICKS", "hatched successfully", duration=2)
    clips.append(end)
    
    # === TRANSITIONS ===
    print("\nApplying transitions...")
    transitioned_clips = []
    
    for i, clip in enumerate(clips):
        if i == 0:
            transitioned_clips.append(clip.fadein(0.3))
        elif i == len(clips) - 1:
            transitioned_clips.append(clip.fadeout(0.3))
        else:
            transitioned_clips.append(clip.fadein(0.2).fadeout(0.2))
    
    print("Combining clips...")
    final = concatenate_videoclips(transitioned_clips, method="compose")
    
    print(f"Total duration: {final.duration:.1f}s")
    
    # === AUDIO ===
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final.duration:
        n_loops = int(final.duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, final.duration).volumex(0.5)
    final = final.set_audio(audio)
    
    # === EXPORT ===
    print(f"\nExporting v23b to {OUTPUT}")
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
    
    print("\n✅ v23b SHORTS complete! Ready for YouTube Shorts.")
    
    final.close()
    for clip in clips:
        clip.close()
    audio.close()

if __name__ == "__main__":
    build_v23b()
