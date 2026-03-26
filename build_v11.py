#!/usr/bin/env python3
"""
Build Quail Hatch Video v11 - FIXED aspect ratio
- Proper vertical output 1080x1920
- Horizontal video (IMG_6093) converted to vertical with crop/zoom
- All other videos are already vertical
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v11.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v11_build"

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

def add_caption(video_clip, text, position="top"):
    """Add caption to video clip."""
    txt_img = create_text_img(text, position)
    txt_clip = ImageClip(txt_img, duration=video_clip.duration)
    return CompositeVideoClip([video_clip, txt_clip])

def extract_clip(video_path, start, duration, slow_factor=1.0):
    """Extract and optionally slow down clip."""
    clip = VideoFileClip(video_path).subclip(start, start + duration)
    if slow_factor != 1.0:
        clip = clip.fx(vfx.speedx, slow_factor)
    return clip

def convert_to_vertical(clip, final_zoom=1.0):
    """Convert any video to 1080x1920 vertical format."""
    frames = []
    fps = 30
    num_frames = int(clip.duration * fps)
    
    for i in range(num_frames):
        t = i / fps
        frame = clip.get_frame(t)
        h, w = frame.shape[:2]
        
        pil_img = Image.fromarray(frame)
        
        # Calculate zoom progress
        progress = i / num_frames
        current_zoom = 1 + (final_zoom - 1) * progress
        
        if w > h:  # Horizontal video - need to crop to vertical
            # Target aspect ratio: 1080/1920 = 0.5625
            target_w = int(h * 0.5625)
            if target_w > w:
                # Video is too narrow, crop height instead
                target_h = int(w / 0.5625)
                top = (h - target_h) // 2
                cropped = pil_img.crop((0, top, w, top + target_h))
            else:
                # Crop width
                left = (w - target_w) // 2
                cropped = pil_img.crop((left, 0, left + target_w, h))
            # Resize to target
            resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        else:  # Vertical video - just resize or zoom
            # Apply zoom
            zoom_w = int(w / current_zoom)
            zoom_h = int(h / current_zoom)
            left = (w - zoom_w) // 2
            top = (h - zoom_h) // 2
            cropped = pil_img.crop((left, top, left + zoom_w, top + zoom_h))
            resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        
        frames.append(np.array(resized))
    
    return ImageSequenceClip(frames, fps=fps)

def build_v11():
    """Build v11 - fixed aspect ratio."""
    print("Building Quail Hatch Video v11 (FIXED)...")
    
    clips = []
    
    # Scene 1: Day 17 - Eggs (6s) - HORIZONTAL video, convert to vertical
    print("Scene 1: Day 17... (converting horizontal to vertical)")
    egg_clip = extract_clip(f"{INPUT_DIR}/IMG_6093.MOV", 10, 6)
    egg_vertical = convert_to_vertical(egg_clip, final_zoom=1.15)
    egg_scene = add_caption(egg_vertical, "Day 17...", "top")
    clips.append(egg_scene)
    egg_clip.close()
    
    # Scene 2: It's starting - First crack (5s) - already vertical
    print("Scene 2: It's starting!")
    crack_clip = extract_clip(f"{INPUT_DIR}/IMG_6138.MOV", 5, 5)
    crack_vertical = convert_to_vertical(crack_clip, final_zoom=1.0)
    crack_scene = add_caption(crack_vertical, "It's starting!", "top")
    clips.append(crack_scene)
    crack_clip.close()
    
    # Scene 3: TUFF EGG - Hatching (10s) 40% speed
    print("Scene 3: Tuff egg to crack")
    hatch_clip = extract_clip(f"{INPUT_DIR}/IMG_7081.MOV", 30, 10, slow_factor=0.4)
    hatch_vertical = convert_to_vertical(hatch_clip, final_zoom=1.0)
    hatch_scene = add_caption(hatch_vertical, "This is a tuff egg\nto crack", "top")
    clips.append(hatch_scene)
    hatch_clip.close()
    
    # Scene 4: FREEDOM - Emerging (6s) 50% speed
    print("Scene 4: FREEDOM!")
    emerge_clip = extract_clip(f"{INPUT_DIR}/IMG_7082.MOV", 2, 6, slow_factor=0.5)
    emerge_vertical = convert_to_vertical(emerge_clip, final_zoom=1.0)
    emerge_scene = add_caption(emerge_vertical, "FREEDOM!", "center")
    clips.append(emerge_scene)
    emerge_clip.close()
    
    # Scene 5: Just hatched - Wet (5s)
    print("Scene 5: Just hatched")
    wet_clip = extract_clip(f"{INPUT_DIR}/IMG_7083.MOV", 5, 5)
    wet_vertical = convert_to_vertical(wet_clip, final_zoom=1.0)
    wet_scene = add_caption(wet_vertical, "Just a little wet\nbehind the ears", "top")
    clips.append(wet_scene)
    wet_clip.close()
    
    # Scene 6: Drying - Food/water (8s)
    print("Scene 6: Food and water")
    dry_clip = extract_clip(f"{INPUT_DIR}/IMG_7083.MOV", 15, 8)
    dry_vertical = convert_to_vertical(dry_clip, final_zoom=1.0)
    dry_scene = add_caption(dry_vertical, "All they think about is\nfood and water", "top")
    clips.append(dry_scene)
    dry_clip.close()
    
    # Scene 7: BROODER FINALE (12s)
    print("Scene 7: Brooder finale")
    brooder_clip = extract_clip(f"{INPUT_DIR}/IMG_6118.MOV", 5, 12)
    brooder_vertical = convert_to_vertical(brooder_clip, final_zoom=1.0)
    brooder_scene = add_caption(brooder_vertical, "Living their best life", "center")
    clips.append(brooder_scene)
    brooder_clip.close()
    
    # Combine
    print("\nCombining all scenes...")
    final = concatenate_videoclips(clips, method="compose")
    
    total_duration = sum([c.duration for c in clips])
    print(f"Total duration: {total_duration:.1f}s")
    print(f"Output size: {TARGET_W}x{TARGET_H} (vertical)")
    
    # Add audio
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final.duration:
        n_loops = int(final.duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, final.duration).volumex(0.4)
    final = final.set_audio(audio)
    
    # Export
    print(f"\nExporting v11 to {OUTPUT}")
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
    
    print("\n✅ v11 is ready! Fixed vertical format 1080x1920.")
    
    # Cleanup
    final.close()
    for clip in clips:
        clip.close()
    audio.close()

if __name__ == "__main__":
    build_v11()
