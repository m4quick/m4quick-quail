"""
AWS Lambda function for Alexa -> OpenClaw integration
Receives Alexa requests and forwards to OpenClaw Gateway
"""

import json
import urllib.request
import urllib.error
import os

# Configuration
OPENCLAW_GATEWAY_URL = os.environ.get('OPENCLAW_GATEWAY_URL', 'http://YOUR_TAILSCALE_IP:18789')
OPENCLAW_AUTH_TOKEN = os.environ.get('OPENCLAW_AUTH_TOKEN', 'your-auth-token-here')


def lambda_handler(event, context):
    """
    Main Lambda handler for Alexa requests
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Get request type
    request_type = event.get('request', {}).get('type')
    
    if request_type == 'LaunchRequest':
        return handle_launch()
    elif request_type == 'IntentRequest':
        return handle_intent(event)
    elif request_type == 'SessionEndedRequest':
        return handle_session_end()
    else:
        return build_response("I'm not sure how to help with that.")


def handle_launch():
    """Handle skill launch"""
    speech_text = "Hello Sir, Enki is ready. What would you like me to do?"
    return build_response(speech_text, should_end_session=False)


def handle_intent(event):
    """Handle Alexa intents"""
    intent_name = event['request']['intent']['name']
    slots = event['request']['intent'].get('slots', {})
    
    if intent_name == 'AskEnkiIntent':
        query = slots.get('Query', {}).get('value', '')
        if query:
            return forward_to_openclaw(query)
        else:
            return build_response("What would you like me to do?", should_end_session=False)
    
    elif intent_name == 'AMAZON.HelpIntent':
        return build_response(
            "You can ask me anything. For example, 'Ask Enki what's on my calendar' or 'Ask Enki to summarize this video'.",
            should_end_session=False
        )
    
    elif intent_name in ['AMAZON.CancelIntent', 'AMAZON.StopIntent']:
        return build_response("Goodbye Sir.", should_end_session=True)
    
    else:
        return build_response("I'm not sure how to help with that. Try asking me a question.")


def forward_to_openclaw(query):
    """Forward the query to OpenClaw Gateway"""
    try:
        # Prepare request
        url = f"{OPENCLAW_GATEWAY_URL}/api/message"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENCLAW_AUTH_TOKEN}'
        }
        data = {
            'message': query,
            'source': 'alexa',
            'channel': 'alexa-voice'
        }
        
        # Send request to OpenClaw
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            response_text = result.get('response', "I'm working on that.")
            return build_response(response_text, should_end_session=True)
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return build_response("I'm having trouble connecting. Please try again.")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return build_response("I can't reach the gateway right now.")
    except Exception as e:
        print(f"Error: {str(e)}")
        return build_response("Something went wrong. Please try again.")


def handle_session_end():
    """Handle session end"""
    return build_response("Goodbye Sir.", should_end_session=True)


def build_response(speech_text, should_end_session=True):
    """Build Alexa response"""
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech_text
            },
            'shouldEndSession': should_end_session
        }
    }
