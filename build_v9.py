#!/usr/bin/env python3
"""
Build Quail Hatch Video v9 - REARRANGED for better progression
- Caption "tuff egg to crack" moved to actual cracking scene
- Brooder chicks at the END to show progression
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *

INPUT_DIR = "/Users/mirzaie/Pictures/QuailHatch"
OUTPUT = f"{INPUT_DIR}/QuailHatchVideo_v9.mp4"
AUDIO = f"{INPUT_DIR}/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v9_build"

os.makedirs(WORKSPACE, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def create_text_clip(text, duration, position="top"):
    """Create text overlay with white text + black stroke."""
    img = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
    except:
        font = ImageFont.load_default()
    
    # Handle multi-line
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
        start_y = 180
    
    current_y = start_y
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (TARGET_W - text_width) // 2
        
        # Draw stroke
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, -3), (0, 3), (-3, 0), (3, 0)]:
            draw.text((x + dx, current_y + dy), line, font=font, fill=(0, 0, 0, 255))
        draw.text((x, current_y), line, font=font, fill=(255, 255, 255, 255))
        
        current_y += line_heights[0] + 15
    
    temp_path = f"{WORKSPACE}/text_{hash(text) % 10000}.png"
    img.save(temp_path)
    clip = ImageClip(temp_path, duration=duration)
    return clip

def process_video(video_path, start_time, duration, slow_factor=1.0):
    """Extract and optionally slow down video segment."""
    clip = VideoFileClip(video_path).subclip(start_time, start_time + duration)
    if slow_factor != 1.0:
        clip = clip.fx(vfx.speedx, slow_factor)
    return clip

def zoom_frame(frame_array, zoom_factor):
    """Zoom into center of frame."""
    h, w = frame_array.shape[:2]
    pil_img = Image.fromarray(frame_array)
    new_w = int(w / zoom_factor)
    new_h = int(h / zoom_factor)
    left = (w - new_w) // 2
    top = (h - new_h) // 2
    right = left + new_w
    bottom = top + new_h
    cropped = pil_img.crop((left, top, right, bottom))
    zoomed = cropped.resize((w, h), Image.Resampling.LANCZOS)
    return np.array(zoomed)

def create_zoom_clip(video_clip, start_time, duration, final_zoom=1.3):
    """Create progressive zoom effect."""
    frames = []
    fps = 30
    num_frames = int(duration * fps)
    
    for i in range(num_frames):
        t = start_time + (i / fps)
        if t > video_clip.duration:
            t = video_clip.duration - 0.01
        frame = video_clip.get_frame(t)
        progress = i / num_frames
        current_zoom = 1 + (final_zoom - 1) * progress
        zoomed = zoom_frame(frame, current_zoom)
        frames.append(zoomed)
    
    return ImageSequenceClip(frames, fps=fps)

def build_v9():
    """Build v9 with rearranged scenes for better progression."""
    
    # Load source videos
    print("Loading source videos...")
    egg_vid = VideoFileClip(f"{INPUT_DIR}/IMG_6093.MOV")  # Eggs waiting
    crack_vid = VideoFileClip(f"{INPUT_DIR}/IMG_6138.MOV")  # Pipping
    hatch_vid = VideoFileClip(f"{INPUT_DIR}/IMG_7081.MOV")  # Hatching
    emerge_vid = VideoFileClip(f"{INPUT_DIR}/IMG_7082.MOV")  # Emergence
    dry_vid = VideoFileClip(f"{INPUT_DIR}/IMG_7083.MOV")  # Drying
    brooder_vid = VideoFileClip(f"{INPUT_DIR}/IMG_6118.MOV")  # Brooder - ENDING
    
    clips = []
    
    # Scene 1: "Day 17" - Eggs waiting (6s) with zoom
    print("Scene 1: Day 17 - Eggs waiting")
    egg_scene = create_zoom_clip(egg_vid, 10, 6, final_zoom=1.2)
    txt1 = create_text_clip("Day 17...", 6, "top")
    clips.append(CompositeVideoClip([egg_scene, txt1]))
    
    # Scene 2: "It's starting!" - First crack (5s)
    print("Scene 2: It's starting!")
    crack_scene = process_video(f"{INPUT_DIR}/IMG_6138.MOV", 5, 5)
    txt2 = create_text_clip("It's starting!", 5, "top")
    clips.append(CompositeVideoClip([crack_scene, txt2]))
    
    # Scene 3: "TUFF EGG TO CRACK" - ACTIVE HATCHING (10s) SLOW MOTION
    print("Scene 3: Tuff egg to crack - Hatching")
    hatch_scene = process_video(f"{INPUT_DIR}/IMG_7081.MOV", 30, 10, slow_factor=0.4)
    txt3 = create_text_clip("This is a tuff egg\nto crack", 10, "top")
    clips.append(CompositeVideoClip([hatch_scene, txt3]))
    
    # Scene 4: "FREEDOM!" - Chick emerging (6s) SLOW MOTION
    print("Scene 4: FREEDOM!")
    emerge_scene = process_video(f"{INPUT_DIR}/IMG_7082.MOV", 2, 6, slow_factor=0.5)
    txt4 = create_text_clip("FREEDOM!", 6, "center")
    clips.append(CompositeVideoClip([emerge_scene, txt4]))
    
    # Scene 5: "Just a little wet" - Newborn (5s)
    print("Scene 5: Just hatched")
    wet_scene = process_video(f"{INPUT_DIR}/IMG_7083.MOV", 5, 5)
    txt5 = create_text_clip("Just a little wet\nbehind the ears", 5, "top")
    clips.append(CompositeVideoClip([wet_scene, txt5]))
    
    # Scene 6: "Food and water" - Drying (8s)
    print("Scene 6: All they think about")
    dry_scene = process_video(f"{INPUT_DIR}/IMG_7083.MOV", 15, 8)
    txt6 = create_text_clip("All they think about is\nfood and water", 8, "top")
    clips.append(CompositeVideoClip([dry_scene, txt6]))
    
    # Scene 7: "Living their best life" - BROODER CHICKS (12s) - THE FINALE
    print("Scene 7: Living their best life - BROODER FINALE")
    brooder_scene = process_video(f"{INPUT_DIR}/IMG_6118.MOV", 5, 12)
    txt7 = create_text_clip("Living their best life", 12, "center")
    clips.append(CompositeVideoClip([brooder_scene, txt7]))
    
    # Combine all
    print("\nCombining scenes...")
    final = concatenate_videoclips(clips)
    
    new_duration = sum([c.duration for c in clips])
    print(f"New duration: {new_duration:.1f}s")
    
    # Add audio
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final.duration:
        n_loops = int(final.duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, final.duration).volumex(0.4)
    final = final.set_audio(audio)
    
    # Export
    print(f"\nExporting v9 to {OUTPUT}")
    final.write_videofile(
        OUTPUT,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="8000k",
        threads=4,
        preset="medium"
    )
    
    print("\n✅ v9 ready! Better progression with brooder at the end!")
    
    # Cleanup
    final.close()
    egg_vid.close()
    crack_vid.close()
    hatch_vid.close()
    emerge_vid.close()
    dry_vid.close()
    brooder_vid.close()

if __name__ == "__main__":
    build_v9()
