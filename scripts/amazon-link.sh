#!/bin/bash
# Amazon Affiliate Link Generator
# Usage: ./amazon-link.sh "product-name" "ASIN"

ASSOCIATE_ID="m4quickquail-20"

if [ $# -lt 2 ]; then
    echo "Usage: $0 \"Product Name\" ASIN"
    echo "Example: $0 \"Brinsea Mini II\" B01N7V536G"
    exit 1
fi

PRODUCT_NAME="$1"
ASIN="$2"

LINK="https://www.amazon.com/dp/${ASIN}?tag=${ASSOCIATE_ID}"

echo "✅ Affiliate Link: $LINK"
echo ""
echo "HTML: <a href=\"$LINK\" target=\"_blank\">$PRODUCT_NAME</a>"
echo "Markdown: [$PRODUCT_NAME]($LINK)"
