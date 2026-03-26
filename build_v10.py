#!/usr/bin/env python3
"""
Build Quail Hatch Video v10 - CLEAN rebuild of v9
- Caption "tuff egg to crack" on actual hatching scene
- Brooder chicks at END for progression
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v10.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v10_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_text_img(text, position="top"):
    """Create text image with white text + black outline."""
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
        
        # Black outline
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, -3), (0, 3), (-3, 0), (3, 0)]:
            draw.text((x + dx, current_y + dy), line, font=font, fill=(0, 0, 0, 255))
        # White text
        draw.text((x, current_y), line, font=font, fill=(255, 255, 255, 255))
        
        current_y += line_heights[0] + 15
    
    return np.array(img)

def add_caption(video_clip, text, duration, position="top"):
    """Add caption to video clip."""
    txt_img = create_text_img(text, position)
    txt_clip = ImageClip(txt_img, duration=duration)
    return CompositeVideoClip([video_clip, txt_clip])

def extract_clip(video_path, start, duration, slow_factor=1.0):
    """Extract and optionally slow down clip."""
    clip = VideoFileClip(video_path).subclip(start, start + duration)
    if slow_factor != 1.0:
        clip = clip.fx(vfx.speedx, slow_factor)
    return clip

def zoom_clip(clip, final_zoom=1.25):
    """Apply progressive zoom to clip."""
    frames = []
    fps = 30
    num_frames = int(clip.duration * fps)
    
    for i in range(num_frames):
        t = i / fps
        frame = clip.get_frame(t)
        h, w = frame.shape[:2]
        
        progress = i / num_frames
        current_zoom = 1 + (final_zoom - 1) * progress
        
        new_w = int(w / current_zoom)
        new_h = int(h / current_zoom)
        left = (w - new_w) // 2
        top = (h - new_h) // 2
        
        pil_img = Image.fromarray(frame)
        cropped = pil_img.crop((left, top, left + new_w, top + new_h))
        zoomed = cropped.resize((w, h), Image.Resampling.LANCZOS)
        frames.append(np.array(zoomed))
    
    return ImageSequenceClip(frames, fps=fps)

def build_v10():
    """Build v10 - clean rebuild."""
    print("Building Quail Hatch Video v10...")
    
    clips = []
    
    # Scene 1: Day 17 - Eggs (6s) with zoom
    print("Scene 1: Day 17...")
    egg_clip = extract_clip(f"{INPUT_DIR}/IMG_6093.MOV", 10, 6)
    egg_zoomed = zoom_clip(egg_clip, 1.2)
    egg_scene = add_caption(egg_zoomed, "Day 17...", 6, "top")
    clips.append(egg_scene)
    
    # Scene 2: It's starting - First crack (5s)
    print("Scene 2: It's starting!")
    crack_clip = extract_clip(f"{INPUT_DIR}/IMG_6138.MOV", 5, 5)
    crack_scene = add_caption(crack_clip, "It's starting!", 5, "top")
    clips.append(crack_scene)
    
    # Scene 3: TUFF EGG - Hatching (10s) 40% speed = 2.5x slower
    print("Scene 3: Tuff egg to crack")
    hatch_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 30, 10, slow_factor=0.4)
    hatch_scene = add_caption(hatch_clip, "This is a tuff egg\nto crack", hatch_clip.duration, "top")
    clips.append(hatch_scene)
    
    # Scene 4: FREEDOM - Emerging (6s) 50% speed
    print("Scene 4: FREEDOM!")
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 2, 6, slow_factor=0.5)
    emerge_scene = add_caption(emerge_clip, "FREEDOM!", emerge_clip.duration, "center")
    clips.append(emerge_scene)
    
    # Scene 5: Just hatched - Wet (5s)
    print("Scene 5: Just hatched")
    wet_clip = extract_clip(f"{INPUT_DIR}/IMG_7083.MOV", 5, 5)
    wet_scene = add_caption(wet_clip, "Just a little wet\nbehind the ears", 5, "top")
    clips.append(wet_scene)
    
    # Scene 6: Drying - Food/water (8s)
    print("Scene 6: Food and water")
    dry_clip = extract_clip(f"{INPUT_DIR}/IMG_7083.MOV", 15, 8)
    dry_scene = add_caption(dry_clip, "All they think about is\nfood and water", 8, "top")
    clips.append(dry_scene)
    
    # Scene 7: BROODER FINALE - Running around (12s)
    print("Scene 7: Brooder finale")
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 5, 12)
    brooder_scene = add_caption(brooder_clip, "Living their best life", 12, "center")
    clips.append(brooder_scene)
    
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
    
    # Export clean
    print(f"\nExporting v10 to {OUTPUT}")
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
    
    print("\n✅ v10 is ready! Clean rebuild with proper progression.")
    
    # Cleanup
    final.close()
    for clip in clips:
        clip.close()
    audio.close()

if __name__ == "__main__":
    build_v10()
