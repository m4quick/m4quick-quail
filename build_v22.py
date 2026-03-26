#!/usr/bin/env python3
"""
Build Quail Hatch Video v22 - SMOOTH TEXT SHADOWS
- Gaussian blur for soft shadows (not blocky)
- Cleaner, professional look
- Still TikTok style ALL CAPS
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *
from moviepy.video.fx.all import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v22_SMOOTH.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v22_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_smooth_text(text, font_size=76, position="center"):
    """Create text with smooth blur shadow"""
    # Create larger canvas for shadow
    padding = 50
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
        total_height += line_height + 20
    
    # Center vertically on padded canvas
    if position == "center":
        start_y = ((TARGET_H + padding*2) - total_height) // 2
    else:
        start_y = (TARGET_H + padding*2) - total_height - 180
    
    # Calculate positions
    positions = []
    current_y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = ((TARGET_W + padding*2) - text_width) // 2
        positions.append((x, current_y, line))
        current_y += line_heights[0] + 25
    
    # Create shadow layer (black text)
    shadow = Image.new('RGBA', (TARGET_W + padding*2, TARGET_H + padding*2), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    for x, y, line in positions:
        shadow_draw.text((x, y), line, font=font, fill=(0, 0, 0, 255))
    
    # Blur the shadow (smooth!)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=8))
    
    # Create text layer (white text)
    text_layer = Image.new('RGBA', (TARGET_W + padding*2, TARGET_H + padding*2), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    for x, y, line in positions:
        text_draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
    
    # Composite: shadow first, then text
    result = Image.alpha_composite(shadow, text_layer)
    
    # Crop to target size
    result = result.crop((padding, padding, TARGET_W + padding, TARGET_H + padding))
    
    return np.array(result)

def create_title_card(text, duration=2):
    """Title with smooth shadow"""
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
        
        # Draw smooth shadow using blur technique
        shadow_img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_draw.text((x, current_y), line, font=title_font, fill=(0, 0, 0, 255))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=10))
        
        # Draw text on top
        text_img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((x, current_y), line, font=title_font, fill=(255, 255, 255, 255))
        
        # Composite
        combined = Image.alpha_composite(shadow_img, text_img)
        img.paste(combined, (0, 0), combined)
        
        current_y += 140
    
    img_array = np.array(img)
    clip = ImageClip(img_array, duration=duration)
    clip = clip.fadein(0.5).fadeout(0.5)
    
    return clip

def add_caption(video_clip, text, position="bottom"):
    txt_array = create_smooth_text(text, font_size=76, position=position)
    txt_clip = ImageClip(txt_array, duration=video_clip.duration)
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

def build_v22():
    print("Building Quail Hatch Video v22 - SMOOTH TEXT SHADOWS...")
    print("Features: Gaussian blur shadows, no blocky edges")
    
    clips = []
    
    # === TITLE CARD ===
    print("Title...")
    title = create_title_card("THE MIRACLE\nOF HATCHING!", duration=2)
    clips.append(title)
    
    # === DAY 17 ===
    print("Day 17...")
    egg_clip = extract_clip(f"{INPUT_DIR}/IMG_6093.MOV", 10, 2)
    egg_vertical = convert_to_vertical(egg_clip, final_zoom=1.15)
    egg_scene = add_caption(egg_vertical, "DAY 17...", "bottom")
    clips.append(egg_scene)
    egg_clip.close()
    
    # === THE STRUGGLE ===
    print("The struggle...")
    effort_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 35, 10, slow_factor=0.5)
    effort_vertical = convert_to_vertical(effort_clip, final_zoom=1.0)
    effort_scene = add_caption(effort_vertical, "THIS IS A TUFF EGG\nTO CRACK", "bottom")
    clips.append(effort_scene)
    effort_clip.close()
    
    # === HERE WE GO! ===
    print("Here we go...")
    hatch_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 95, 4, slow_factor=0.5)
    hatch_vertical = convert_to_vertical(hatch_clip, final_zoom=1.0)
    hatch_scene = add_caption(hatch_vertical, "HERE WE GO!", "bottom")
    clips.append(hatch_scene)
    hatch_clip.close()
    
    # === FREEDOM! ===
    print("Freedom...")
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 2, 5, slow_factor=0.5)
    emerge_vertical = convert_to_vertical(emerge_clip, final_zoom=1.0)
    emerge_scene = add_caption(emerge_vertical, "FREEDOM!", "center")
    clips.append(emerge_scene)
    emerge_clip.close()
    
    # === BROODER ===
    print("Brooder...")
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 5, 10)
    brooder_vertical = convert_to_vertical(brooder_clip, final_zoom=1.0)
    brooder_scene = add_caption(brooder_vertical, "LIVING THEIR BEST LIFE", "center")
    clips.append(brooder_scene)
    brooder_clip.close()
    
    # === END ===
    print("End card...")
    end_title = create_title_card("THE END", duration=1.5)
    clips.append(end_title)
    
    # Apply smooth transitions
    print("\nApplying smooth transitions...")
    transitioned_clips = []
    
    for i, clip in enumerate(clips):
        if i == 0:
            transitioned_clips.append(clip.fadein(0.5))
        elif i == len(clips) - 1:
            transitioned_clips.append(clip.fadeout(0.5))
        else:
            transitioned_clips.append(clip.fadein(0.3).fadeout(0.3))
    
    print("Combining...")
    final = concatenate_videoclips(transitioned_clips, method="compose")
    
    print(f"Total duration: {final.duration:.1f}s")
    
    # Add audio
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final.duration:
        n_loops = int(final.duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, final.duration).volumex(0.5)
    final = final.set_audio(audio)
    
    # Export
    print(f"\nExporting v22 to {OUTPUT}")
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
    
    print("\n✅ v22 ready! Smooth blur shadows.")
    
    final.close()
    for clip in clips:
        clip.close()
    audio.close()

if __name__ == "__main__":
    build_v22()
