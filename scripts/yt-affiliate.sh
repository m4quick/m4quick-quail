#!/bin/bash
# YouTube Affiliate Link Generator
# Usage: ./yt-affiliate.sh "video title" "product1:ASIN" "product2:ASIN" ...

ASSOCIATE_ID="m4quickquail-20"
VIDEO_TITLE="${1:-Quail Video}"
shift

echo "=========================================="
echo "  YouTube Description for: $VIDEO_TITLE"
echo "=========================================="
echo ""
echo "🐣 M4Quick Quail Farm"
echo ""
echo "📺 Subscribe: https://www.youtube.com/@m4quick"
echo "🐣 Starter Kit: https://m4quick.github.io/m4quick-quail/starter-kit.html"
echo ""

if [ $# -gt 0 ]; then
    echo "🛒 Products mentioned (Amazon Affiliate):"
    for product in "$@"; do
        name="${product%%:*}"
        asin="${product##*:}"
        echo "• $name: https://www.amazon.com/dp/$asin?tag=$ASSOCIATE_ID"
    done
    echo ""
fi

echo "📧 Questions? michael@mirzaie.com"
echo ""
echo "---"
echo "*As an Amazon Associate, I earn from qualifying purchases.*"
echo ""
echo "=========================================="
echo ""
echo "Copy the above into your YouTube description!"
