#!/bin/bash
# Deploy Alexa Skill to AWS Lambda

set -e

SKILL_NAME="enki-assistant"
LAMBDA_FUNCTION_NAME="enki-alexa-handler"
AWS_REGION="us-east-1"  # Change if needed

echo "=== Enki Alexa Skill Deployment ==="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
command -v aws >/dev/null 2>&1 || { echo "AWS CLI required. Install: brew install awscli"; exit 1; }
command -v zip >/dev/null 2>&1 || { echo "zip required. Install: brew install zip"; exit 1; }

# Get OpenClaw Gateway info
echo ""
echo "OpenClaw Gateway Configuration:"
echo "Current gateway config:"
grep -E "(url|token|port)" ~/.openclaw/openclaw.json | head -5

echo ""
echo "⚠️  IMPORTANT: Update these values in lambda_function.py:"
echo "  1. OPENCLAW_GATEWAY_URL - Must be accessible from AWS"
echo "  2. OPENCLAW_AUTH_TOKEN - From your openclaw.json"
echo ""

# For local testing, we need to expose the gateway
# Options:
echo "To make OpenClaw accessible from AWS, you need:"
echo ""
echo "Option 1: Tailscale (Recommended)"
echo "  - Already installed: tailscale status"
echo "  - Your Tailscale IP will be the gateway URL"
echo "  - Example: http://100.x.x.x:18789"
echo ""
echo "Option 2: ngrok (Temporary)"
echo "  - Install: brew install ngrok"
echo "  - Run: ngrok http 18789"
echo "  - Use the https URL for Lambda"
echo ""
echo "Option 3: AWS VPC (Advanced)"
echo "  - Run OpenClaw on EC2 in same VPC"
echo ""

read -p "Press Enter once you've updated lambda_function.py with your gateway URL..."

# Create deployment package
echo ""
echo "Creating Lambda deployment package..."
cd alexa-skill
zip -r ../enki-alexa-skill.zip lambda_function.py

echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Create Lambda function in AWS Console:"
echo "   https://console.aws.amazon.com/lambda"
echo ""
echo "2. Create new function:"
echo "   - Name: enki-alexa-handler"
echo "   - Runtime: Python 3.11"
echo "   - Architecture: x86_64"
echo ""
echo "3. Upload enki-alexa-skill.zip"
echo ""
echo "4. Set Environment Variables:"
echo "   - OPENCLAW_GATEWAY_URL=http://YOUR_IP:18789"
echo "   - OPENCLAW_AUTH_TOKEN=your-token"
echo ""
echo "5. Create Alexa Skill:"
echo "   https://developer.amazon.com/alexa/console/ask"
echo ""
echo "6. Import interaction_model.json"
echo ""
echo "7. Set Lambda ARN as endpoint"
echo ""
echo "For detailed instructions, see:"
echo "https://developer.amazon.com/en-US/docs/alexa/custom-skills/steps-to-build-a-custom-skill.html"
echo ""
