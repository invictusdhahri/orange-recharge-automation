#!/usr/bin/env python3
"""
Quick test script for Orange credit card recharge with 2Captcha
Loads API key from .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from orange_creditcard import OrangeCreditCardRecharge

# Load .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Get credentials
api_key = os.getenv('TWOCAPTCHA_API_KEY')
phone = os.getenv('TEST_PHONE', '53028939')
amount = int(os.getenv('TEST_AMOUNT', '20'))

if not api_key:
    print("❌ No API key found in .env file!")
    print("Create .env file with: TWOCAPTCHA_API_KEY=your_key")
    exit(1)

print("="*60)
print("Orange Credit Card Recharge Test")
print("="*60)
print(f"Phone:  {phone}")
print(f"Amount: {amount} DT")
print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
print("="*60)
print()

# Initialize recharger
recharger = OrangeCreditCardRecharge(
    twocaptcha_api_key=api_key,
    headless=False  # Keep browser visible for testing
)

# Perform recharge
print("🚀 Starting recharge with auto CAPTCHA solving...")
print("   (will try free audio first, fallback to 2Captcha)")
print()

result = recharger.recharge(
    phone_number=phone,
    amount=amount,
    captcha_method='auto'
)

# Show result
print()
print("="*60)
print("RESULT")
print("="*60)
print(f"Status: {result['status']}")

if result.get('payment_url'):
    print(f"✅ Payment URL obtained!")
    print(f"   {result['payment_url']}")
elif result.get('message'):
    print(f"Message: {result['message']}")

if result.get('current_url'):
    print(f"Current URL: {result['current_url']}")

print("="*60)
