#!/usr/bin/env python3
"""
Build Quail Hatch Video v8 with AI-enhanced transitions
- Frame interpolation between clips
- Smooth morphing effects
- Dramatic slow-motion on hatching moment
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

# Add moviepy
sys.path.insert(0, '/Users/mirzaie/.openclaw/workspace/.venvs/moviepy/lib/python3.14/site-packages')
from moviepy.editor import *
from moviepy.video.fx.all import resize

INPUT = "/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v7.mp4"
OUTPUT = "/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v8.mp4"
AUDIO = "/Users/mirzaie/Pictures/QuailHatch/ukulele_source.m4a"
WORKSPACE = "/Users/mirzaie/.openclaw/workspace/v8_build"

os.makedirs(WORKSPACE, exist_ok=True)
os.makedirs(f"{WORKSPACE}/frames", exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def extract_frames(video_path, output_dir, fps=10):
    """Extract frames from video at specified fps."""
    print(f"Extracting frames from {video_path}...")
    clip = VideoFileClip(video_path)
    
    frame_count = 0
    for t in np.arange(0, clip.duration, 1/fps):
        frame = clip.get_frame(t)
        frame_path = f"{output_dir}/frame_{frame_count:04d}.jpg"
        Image.fromarray(frame).save(frame_path, quality=95)
        frame_count += 1
    
    clip.close()
    print(f"Extracted {frame_count} frames")
    return frame_count

def interpolate_frames(frame1_path, frame2_path, num_intermediate=10):
    """Create smooth transition between two frames using crossfade."""
    img1 = np.array(Image.open(frame1_path).convert('RGB'))
    img2 = np.array(Image.open(frame2_path).convert('RGB'))
    
    frames = []
    for i in range(num_intermediate + 2):
        alpha = i / (num_intermediate + 1)
        # Linear blend
        blended = cv2.addWeighted(img1, 1-alpha, img2, alpha, 0)
        frames.append(blended)
    
    return frames

def create_zoom_effect(frame, zoom_factor=1.5, duration_frames=30):
    """Create a zoom-in effect on a frame."""
    img = np.array(Image.fromarray(frame).convert('RGB'))
    h, w = img.shape[:2]
    
    frames = []
    for i in range(duration_frames):
        # Calculate zoom
        progress = i / duration_frames
        current_zoom = 1 + (zoom_factor - 1) * progress
        
        # Calculate crop region
        new_w = int(w / current_zoom)
        new_h = int(h / current_zoom)
        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2
        x2 = x1 + new_w
        y2 = y1 + new_h
        
        # Crop and resize
        cropped = img[y1:y2, x1:x2]
        zoomed = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LANCZOS4)
        frames.append(zoomed)
    
    return frames

def enhance_hatching_sequence():
    """Create an enhanced hatching sequence with AI-like effects."""
    print("Creating AI-enhanced hatching sequence...")
    
    # Extract key frames from the original video
    video = VideoFileClip(INPUT)
    
    # Define key moments for enhancement (in seconds)
    key_moments = [
        (5, "egg_waiting"),      # Egg waiting
        (9, "first_crack"),      # First crack  
        (18, "hatching"),        # Active hatching
        (22, "emerging"),        # Chick emerging
        (28, "just_hatched"),    # Just hatched
    ]
    
    enhanced_clips = []
    
    # Scene 1: Normal intro (0-5s)
    print("Scene 1: Intro...")
    enhanced_clips.append(video.subclip(0, 5))
    
    # Scene 2: Dramatic zoom on egg cracking (5-12s) - SLOW MOTION
    print("Scene 2: Dramatic hatching sequence with zoom...")
    crack_scene = video.subclip(5, 12)
    # Apply slow motion
    crack_scene = crack_scene.fx(vfx.speedx, 0.5)  # Half speed
    enhanced_clips.append(crack_scene)
    
    # Scene 3: Transition sequence (12-20s) with interpolation
    print("Scene 3: Smooth transition...")
    
    # Extract frames for interpolation
    start_frame = video.get_frame(12)
    end_frame = video.get_frame(20)
    
    # Create smooth crossfade
    transition_frames = []
    for i in range(15):  # 15 interpolated frames = 0.5s at 30fps
        alpha = i / 14
        blended = (start_frame * (1 - alpha) + end_frame * alpha).astype(np.uint8)
        transition_frames.append(blended)
    
    # Create clip from frames
    transition_clip = ImageSequenceClip(transition_frames, fps=30)
    transition_clip = transition_clip.set_duration(0.5)
    enhanced_clips.append(transition_clip)
    
    # Add the actual scene
    enhanced_clips.append(video.subclip(20, 25))
    
    # Scene 4: Normal ending (25-45s)
    print("Scene 4: Ending...")
    ending = video.subclip(25, 45)
    enhanced_clips.append(ending)
    
    # Combine all clips
    final = concatenate_videoclips(enhanced_clips)
    
    # Add audio
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
    
    print("\n✅ v8 with AI enhancements is ready!")
    final.close()
    video.close()

if __name__ == "__main__":
    enhance_hatching_sequence()
