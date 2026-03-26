#!/bin/bash
# Build Quail Hatch Video v7 with humorous captions

INPUT="/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v6.mp4"
OUTPUT="/Users/mirzaie/Pictures/QuailHatch/QuailHatchVideo_v7.mp4"
AUDIO="/Users/mirzaie/Pictures/QuailHatch/ukulele_source.m4a"
WORKSPACE="/Users/mirzaie/.openclaw/workspace/v7_build"

mkdir -p "$WORKSPACE"

# Extract video duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT" | cut -d. -f1)
echo "Video duration: ${DURATION}s"

# Create captioned version using multiple drawtext filters
# Each caption appears at specific time ranges
ffmpeg -y -i "$INPUT" -vf "
drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='Day 17...':fontsize=72:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=150:enable='between(t\\,0\\,7)',
drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='This is a tuff egg to crack':fontsize=64:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=150:enable='between(t\\,7\\,12)',
drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='Almost there...':fontsize=64:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=150:enable='between(t\\,12\\,20)',
drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='FREEDOM!':fontsize=72:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=150:enable='between(t\\,20\\,26)',
drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='Just a little wet behind the ears':fontsize=56:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=150:enable='between(t\\,26\\,31)',
drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='All they think about is food and water':fontsize=52:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=150:enable='between(t\\,31\\,39)',
drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='Living their best life':fontsize=64:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=150:enable='between(t\\,39\\,45)'
" -c:v libx264 -preset medium -crf 23 -an -r 30 "$WORKSPACE/captioned.mp4"

echo "Adding audio..."
ffmpeg -y -i "$WORKSPACE/captioned.mp4" -stream_loop -1 -i "$AUDIO" -t $DURATION \
    -c:v copy -c:a aac -b:a 128k -shortest "$OUTPUT"

echo "Done!"
ls -lh "$OUTPUT"
