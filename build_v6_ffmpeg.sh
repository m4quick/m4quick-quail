#!/bin/bash
# Build Quail Hatch Video v6 using ffmpeg directly
# Story: "The Miracle of Hatching" - 7 scenes, ~45 seconds

INPUT_DIR="/Users/mirzaie/Pictures/QuailHatch"
OUTPUT="$INPUT_DIR/QuailHatchVideo_v6.mp4"
WORKSPACE="/Users/mirzaie/.openclaw/workspace/v6_build"
TARGET_W=1080
TARGET_H=1920
FPS=30

mkdir -p "$WORKSPACE"

# Function to process video to vertical 9:16
process_clip() {
    local input=$1
    local start=$2
    local duration=$3
    local output=$4
    
    ffmpeg -y -ss $start -t $duration -i "$input" -vf \
        "scale=-1:$TARGET_H:flags=lanczos,crop=$TARGET_W:$TARGET_H:(in_w-$TARGET_W)/2:(in_h-$TARGET_H)/2" \
        -c:v libx264 -preset medium -crf 23 -an -r $FPS "$output"
}

echo "Processing scenes..."

# Scene 1: The Wait (Eggs) - horizontal source
process_clip "$INPUT_DIR/IMG_6093.MOV" 10 7 "$WORKSPACE/scene1.mp4"

# Scene 2: The First Sign (Pipping) - vertical
ffmpeg -y -ss 5 -t 5 -i "$INPUT_DIR/IMG_6138.MOV" -vf \
    "scale=${TARGET_W}:${TARGET_H}:force_original_aspect_ratio=decrease,pad=$TARGET_W:$TARGET_H:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 -an -r $FPS "$WORKSPACE/scene2.mp4"

# Scene 3: The Struggle - vertical
ffmpeg -y -ss 30 -t 8 -i "$INPUT_DIR/IMG_7081.MOV" -vf \
    "scale=${TARGET_W}:${TARGET_H}:force_original_aspect_ratio=decrease,pad=$TARGET_W:$TARGET_H:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 -an -r $FPS "$WORKSPACE/scene3.mp4"

# Scene 4: The Breakthrough - vertical
ffmpeg -y -ss 60 -t 6 -i "$INPUT_DIR/IMG_7081.MOV" -vf \
    "scale=${TARGET_W}:${TARGET_H}:force_original_aspect_ratio=decrease,pad=$TARGET_W:$TARGET_H:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 -an -r $FPS "$WORKSPACE/scene4.mp4"

# Scene 5: Wet and New - vertical
ffmpeg -y -ss 2 -t 5 -i "$INPUT_DIR/IMG_7082.MOV" -vf \
    "scale=${TARGET_W}:${TARGET_H}:force_original_aspect_ratio=decrease,pad=$TARGET_W:$TARGET_H:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 -an -r $FPS "$WORKSPACE/scene5.mp4"

# Scene 6: The Brooder - vertical
ffmpeg -y -ss 5 -t 8 -i "$INPUT_DIR/IMG_6118.MOV" -vf \
    "scale=${TARGET_W}:${TARGET_H}:force_original_aspect_ratio=decrease,pad=$TARGET_W:$TARGET_H:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 -an -r $FPS "$WORKSPACE/scene6.mp4"

# Scene 7: Final - vertical
ffmpeg -y -ss 5 -t 6 -i "$INPUT_DIR/IMG_7083.MOV" -vf \
    "scale=${TARGET_W}:${TARGET_H}:force_original_aspect_ratio=decrease,pad=$TARGET_W:$TARGET_H:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 -an -r $FPS "$WORKSPACE/scene7.mp4"

echo "Creating concat file..."
cat > "$WORKSPACE/concat.txt" << EOF
file 'scene1.mp4'
file 'scene2.mp4'
file 'scene3.mp4'
file 'scene4.mp4'
file 'scene5.mp4'
file 'scene6.mp4'
file 'scene7.mp4'
EOF

echo "Combining scenes..."
ffmpeg -y -f concat -safe 0 -i "$WORKSPACE/concat.txt" -c copy "$WORKSPACE/nosound.mp4"

echo "Adding audio..."
# Get video duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$WORKSPACE/nosound.mp4" | cut -d. -f1)
echo "Video duration: ${DURATION}s"

# Loop audio to match duration
ffmpeg -y -stream_loop -1 -i "$INPUT_DIR/ukulele_source.m4a" -i "$WORKSPACE/nosound.mp4" \
    -t $DURATION -c:v copy -c:a aac -b:a 128k -shortest "$OUTPUT"

echo "Done! Output: $OUTPUT"
ls -lh "$OUTPUT"
