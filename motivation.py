#!/usr/bin/env python3
"""Generate a random motivational quote."""

import random

QUOTES = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Your time is limited, don't waste it living someone else's life. – Steve Jobs",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "It does not matter how slowly you go as long as you do not stop. – Confucius",
    "Everything you've ever wanted is on the other side of fear. – George Addair",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
    "The best way to predict the future is to create it. – Peter Drucker",
]

def get_random_quote():
    """Return a random motivational quote."""
    return random.choice(QUOTES)

if __name__ == "__main__":
    quote = get_random_quote()
    print(quote)
