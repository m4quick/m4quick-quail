#!/usr/bin/env python3
"""
Build Quail Hatch Video v21 - WITH AI-STYLE TRANSITIONS
- Smooth crossfades between scenes
- Zoom transitions
- Motion blur effects
- Professional flow
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *
from moviepy.video.fx.all import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v21_TRANS.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v21_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_title_card(text, duration=2):
    """Title with zoom animation"""
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
        
        for offset in range(10, 0, -1):
            draw.text((x-offset, current_y), line, font=title_font, fill=(0, 0, 0))
            draw.text((x+offset, current_y), line, font=title_font, fill=(0, 0, 0))
            draw.text((x, current_y-offset), line, font=title_font, fill=(0, 0, 0))
            draw.text((x, current_y+offset), line, font=title_font, fill=(0, 0, 0))
        
        draw.text((x, current_y), line, font=title_font, fill=(255, 255, 255))
        current_y += 140
    
    img_array = np.array(img)
    clip = ImageClip(img_array, duration=duration)
    
    # Zoom in effect
    clip = clip.fx(resize, lambda t: 1 + 0.1 * t)
    clip = clip.fadein(0.5)
    
    return clip

def create_text_img(text, position="bottom"):
    """Text overlay"""
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

def crossfade_transition(clip1, clip2, duration=1.0):
    """Smooth crossfade between clips"""
    # Fade out clip1
    clip1_fade = clip1.fadeout(duration)
    # Fade in clip2
    clip2_fade = clip2.fadein(duration)
    return concatenate_videoclips([clip1_fade, clip2_fade], method="compose")

def zoom_transition(clip1, clip2, duration=1.0):
    """Zoom out then zoom in transition"""
    # Zoom out at end of clip1
    clip1_zoom = clip1.fx(resize, lambda t: 1 + 0.15 * (t / clip1.duration))
    # Zoom in at start of clip2
    clip2_zoom = clip2.fx(resize, lambda t: 1.15 - 0.15 * (t / clip2.duration))
    
    clip1_fade = clip1_zoom.fadeout(duration)
    clip2_fade = clip2_zoom.fadein(duration)
    
    return concatenate_videoclips([clip1_fade, clip2_fade], method="compose")

def build_v21():
    print("Building Quail Hatch Video v21 - WITH AI-STYLE TRANSITIONS...")
    print("Features: Crossfade, zoom transitions, smooth flow")
    
    clips = []
    
    # === TITLE CARD ===
    print("Building scenes...")
    title = create_title_card("THE MIRACLE\nOF HATCHING!", duration=2)
    
    # === DAY 17 ===
    egg_clip = extract_clip(f"{INPUT_DIR}/IMG_6093.MOV", 10, 2)
    egg_vertical = convert_to_vertical(egg_clip, final_zoom=1.15)
    egg_scene = add_caption(egg_vertical, "DAY 17...", "bottom")
    
    # === THE STRUGGLE ===
    effort_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 35, 10, slow_factor=0.5)
    effort_vertical = convert_to_vertical(effort_clip, final_zoom=1.0)
    effort_scene = add_caption(effort_vertical, "THIS IS A TUFF EGG\nTO CRACK", "bottom")
    
    # === HERE WE GO! ===
    hatch_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 95, 4, slow_factor=0.5)
    hatch_vertical = convert_to_vertical(hatch_clip, final_zoom=1.0)
    hatch_scene = add_caption(hatch_vertical, "HERE WE GO!", "bottom")
    
    # === FREEDOM! ===
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 2, 5, slow_factor=0.5)
    emerge_vertical = convert_to_vertical(emerge_clip, final_zoom=1.0)
    emerge_scene = add_caption(emerge_vertical, "FREEDOM!", "center")
    
    # === BROODER ===
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 5, 10)
    brooder_vertical = convert_to_vertical(brooder_clip, final_zoom=1.0)
    brooder_scene = add_caption(brooder_vertical, "LIVING THEIR BEST LIFE", "center")
    
    # === END ===
    end_title = create_title_card("THE END", duration=1.5)
    
    print("Applying transitions...")
    
    # Build with crossfade transitions
    # Title -> Day 17 (zoom transition)
    transition1 = zoom_transition(title, egg_scene, 0.5)
    clips.append(transition1)
    egg_clip.close()
    
    # Day 17 -> Struggle (crossfade)
    transition2 = crossfade_transition(transition1, effort_scene, 0.5)
    clips.append(transition2)
    effort_clip.close()
    
    # Struggle -> Here we go (zoom)
    transition3 = zoom_transition(transition2, hatch_scene, 0.5)
    clips.append(transition3)
    hatch_clip.close()
    
    # Here we go -> Freedom (flash cut - hard cut with flash)
    hatch_fade = hatch_scene.fadeout(0.3)
    emerge_fade = emerge_scene.fadein(0.3)
    transition4 = concatenate_videoclips([hatch_fade, emerge_fade], method="compose")
    clips.append(transition4)
    emerge_clip.close()
    
    # Freedom -> Brooder (smooth crossfade)
    emerge_fade2 = emerge_scene.fadeout(0.5)
    brooder_fade = brooder_scene.fadein(0.5)
    transition5 = concatenate_videoclips([emerge_fade2, brooder_fade], method="compose")
    clips.append(transition5)
    brooder_clip.close()
    
    # Brooder -> End (fade out)
    brooder_fade2 = transition5.fadeout(0.5)
    end_fade = end_title.fadein(0.3)
    final_sequence = concatenate_videoclips([brooder_fade2, end_fade], method="compose")
    
    print("\nFinalizing...")
    
    total_duration = final_sequence.duration
    print(f"Total duration: {total_duration:.1f}s")
    
    # Add audio
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final_duration:
        n_loops = int(final_duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, total_duration).volumex(0.5)
    final = final_sequence.set_audio(audio)
    
    # Export
    print(f"\nExporting v21 to {OUTPUT}")
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
    
    print("\n✅ v21 ready! AI-style smooth transitions.")
    
    final.close()
    audio.close()

if __name__ == "__main__":
    build_v21()
