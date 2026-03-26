#!/usr/bin/env python3
"""
Build Quail Hatch Video v8 with enhanced transitions
- Smooth crossfades between scenes
- Slow-motion on hatching moment
- Zoom effects using PIL
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Add moviepy
sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *
from moviepy.video.fx.all import resize

INPUT = "/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v7.mp4"
OUTPUT = "/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v8.mp4"
AUDIO = "/Users/mirzaie/Pictures/QuailHatch/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v8_build"

os.makedirs(WORKSPACE, exist_ok=True)

def zoom_frame(frame_array, zoom_factor):
    """Zoom into center of frame."""
    h, w = frame_array.shape[:2]
    pil_img = Image.fromarray(frame_array)
    
    # Calculate new size
    new_w = int(w / zoom_factor)
    new_h = int(h / zoom_factor)
    
    # Crop center
    left = (w - new_w) // 2
    top = (h - new_h) // 2
    right = left + new_w
    bottom = top + new_h
    
    cropped = pil_img.crop((left, top, right, bottom))
    zoomed = cropped.resize((w, h), Image.Resampling.LANCZOS)
    
    return np.array(zoomed)

def create_zoom_clip(video_clip, start_time, duration, final_zoom=1.3):
    """Create a clip with progressive zoom effect."""
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

def create_crossfade(clip1, clip2, duration=0.5):
    """Create smooth crossfade between two clips."""
    # Get frames from end of clip1 and start of clip2
    fps = 30
    num_frames = int(duration * fps)
    
    frames = []
    frame1 = clip1.get_frame(clip1.duration - 0.05)
    frame2 = clip2.get_frame(0)
    
    for i in range(num_frames):
        alpha = i / (num_frames - 1)
        blended = (frame1 * (1 - alpha) + frame2 * alpha).astype(np.uint8)
        frames.append(blended)
    
    return ImageSequenceClip(frames, fps=fps)

def enhance_video():
    """Create enhanced v8 with AI-like effects."""
    print("Loading v7...")
    video = VideoFileClip(INPUT)
    
    enhanced_clips = []
    
    # Scene 1: Normal intro (0-6s)
    print("Scene 1: Intro with zoom on eggs...")
    intro = video.subclip(0, 6)
    # Create zoom effect on egg scene
    intro_zoomed = create_zoom_clip(video, 0, 6, final_zoom=1.2)
    enhanced_clips.append(intro_zoomed)
    
    # Scene 2: DRAMATIC SLOW MOTION - The Crack (6-14s)
    print("Scene 2: Dramatic slow-motion hatching...")
    crack_scene = video.subclip(6, 14)
    # Slow it down for drama
    crack_slow = crack_scene.fx(vfx.speedx, 0.4)  # 40% speed = 2.5x slower
    enhanced_clips.append(crack_slow)
    
    # Scene 3: EMERGENCE - Slow motion (14-22s)
    print("Scene 3: Chick emergence...")
    emerge_scene = video.subclip(14, 22)
    # Slow this down too
    emerge_slow = emerge_scene.fx(vfx.speedx, 0.5)  # Half speed
    enhanced_clips.append(emerge_slow)
    
    # Scene 4: Recovery - normal speed (22-45s)
    print("Scene 4: Fluffy ending...")
    ending = video.subclip(22, 45)
    enhanced_clips.append(ending)
    
    # Combine all
    print("\nCombining scenes...")
    final = concatenate_videoclips(enhanced_clips)
    
    # Calculate new duration
    new_duration = sum([c.duration for c in enhanced_clips])
    print(f"New duration: {new_duration:.1f}s (was {video.duration:.1f}s)")
    
    # Add audio
    print("Adding audio...")
    audio = AudioFileClip(AUDIO)
    if audio.duration < final.duration:
        n_loops = int(final.duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * n_loops)
    audio = audio.subclip(0, final.duration).volumex(0.4)
    final = final.set_audio(audio)
    
    # Export
    print(f"\nExporting v8 to {OUTPUT}")
    final.write_videofile(
        OUTPUT,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="8000k",
        threads=4,
        preset="medium"
    )
    
    print("\n✅ v8 with slow-motion hatching is ready!")
    final.close()
    video.close()

if __name__ == "__main__":
    enhance_video()
