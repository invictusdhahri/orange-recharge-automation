# Orange Tunisia - Credit Card Recharge Automation 💳

Complete automation for Orange Tunisia credit card recharges with **FREE reCAPTCHA bypass**.

## 🎯 Features

- ✅ **Credit card recharge** - Get payment URL from GraphQL
- 🆓 **FREE reCAPTCHA bypass** - Audio challenge + speech recognition (~60% success)
- 💰 **2Captcha fallback** - Optional paid service (~99% success, $0.001/solve)
- 🔄 **Auto mode** - Try free method first, fallback to paid if fails
- 🚀 **Production-ready** - Error handling and retries

## 📊 CAPTCHA Bypass Comparison

| Method | Success Rate | Cost | Speed |
|--------|--------------|------|-------|
| **Audio + Speech Recognition** | 60-80% | $0 (FREE) | 10-20s |
| **2Captcha Service** | 95-99% | $0.001/solve | 15-30s |
| **Auto (Recommended)** | 95%+ | ~$0.0003/solve | 10-30s |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt

# Install ffmpeg for audio processing
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

### 2. Basic Usage (FREE Audio CAPTCHA)

```bash
python orange_creditcard.py 53028939 20
```

**Arguments:**
- `phone_number`: Orange phone (e.g., 53028939)
- `amount`: Recharge amount (10, 20, 25, 30, 40, 50, 100, 200, or custom)
- `notification_number` (optional): Phone to notify after recharge

### 3. With 2Captcha Fallback (Recommended)

```bash
python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_API_KEY
```

Get 2Captcha API key: https://2captcha.com/?from=6591885

## 📝 Flow

### Step-by-Step Process

1. **Navigate to page**
   ```
   https://www.orange.tn/recharge-en-ligne
   → Select "Recharge par carte bancaire"
   ```

2. **Fill form**
   - Phone number (e.g., `53028939`)
   - Confirmation phone
   - Amount (10-200 DT or custom)
   - Notification number (optional)

3. **Click Valider**
   - Form validates
   - reCAPTCHA appears

4. **Solve reCAPTCHA** (automatic)
   - **Method 1 (Free):** Audio challenge + speech recognition
   - **Method 2 (Paid):** 2Captcha service
   - **Auto mode:** Try free first, fallback to paid

5. **Click Payer**
   - GraphQL mutation: `topupWithCreditCard`
   - Response contains payment URL

6. **Capture Payment URL**
   ```json
   {
     "data": {
       "topupWithCreditCard": "https://ipay.clictopay.com:443/epg/merchants/CLICTOPAY/payment.html?mdOrder=xxx&language=fr"
     }
   }
   ```

## 🔓 reCAPTCHA Bypass Methods

### Method 1: Audio Challenge (FREE) 🎧

**How it works:**
1. Click reCAPTCHA checkbox
2. Click audio button
3. Download audio file
4. Convert to WAV
5. Use Google Speech Recognition API (free)
6. Submit answer

**Pros:**
- ✅ Completely free
- ✅ No external service required
- ✅ 60-80% success rate

**Cons:**
- ❌ Requires audio processing libraries
- ❌ Google Speech API has rate limits
- ❌ May fail on difficult audio

**Code:**
```python
from orange_creditcard import OrangeCreditCardRecharge

recharger = OrangeCreditCardRecharge()
result = recharger.recharge(
    phone_number="53028939",
    amount=20,
    captcha_method='audio'  # Force audio method
)
```

### Method 2: 2Captcha Service (PAID) 💰

**How it works:**
1. Extract reCAPTCHA site key
2. Send to 2Captcha API
3. Human workers solve it
4. Get token back
5. Inject token into page

**Pros:**
- ✅ 95-99% success rate
- ✅ Very reliable
- ✅ Fast (15-30 seconds)

**Cons:**
- ❌ Costs money ($0.001/solve = $1 per 1000 solves)
- ❌ Requires API key

**Pricing:**
- $3 = 3000+ solves
- $10 = 10,000+ solves

**Setup:**
```bash
# 1. Sign up at https://2captcha.com/?from=6591885
# 2. Get API key from dashboard
# 3. Use in script

python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_KEY
```

**Code:**
```python
recharger = OrangeCreditCardRecharge(twocaptcha_api_key='YOUR_KEY')
result = recharger.recharge(
    phone_number="53028939",
    amount=50,
    captcha_method='2captcha'  # Force 2Captcha
)
```

### Method 3: Auto (BEST) 🚀

**Recommended for production!**

Tries free audio method first, falls back to 2Captcha if it fails.

**Benefits:**
- ✅ 95%+ success rate
- ✅ Minimal cost (only ~30% of requests need 2Captcha)
- ✅ Best of both worlds

**Cost estimate:**
- 1000 recharges = ~300 paid solves = $0.30
- 10,000 recharges = ~3000 paid solves = $3

**Code:**
```python
recharger = OrangeCreditCardRecharge(twocaptcha_api_key='YOUR_KEY')
result = recharger.recharge(
    phone_number="53028939",
    amount=20,
    captcha_method='auto'  # Default, best option
)
```

## 📱 Programmatic Usage

### Python Script

```python
from orange_creditcard import OrangeCreditCardRecharge

# Initialize (with optional 2Captcha key)
recharger = OrangeCreditCardRecharge(
    twocaptcha_api_key='YOUR_KEY',  # Optional
    headless=False  # Set to True for server
)

# Perform recharge
result = recharger.recharge(
    phone_number="53028939",
    amount=50,
    notification_number="27865121",  # Optional
    captcha_method='auto'  # 'audio', '2captcha', or 'auto'
)

# Check result
if result['status'] == 'success':
    print(f"Payment URL: {result['payment_url']}")
    # Open payment URL or send to user
else:
    print(f"Error: {result['message']}")
```

### Response Format

**Success:**
```python
{
    'status': 'success',
    'payment_url': 'https://ipay.clictopay.com:443/epg/merchants/CLICTOPAY/payment.html?mdOrder=xxx',
    'phone': '53028939',
    'amount': 50
}
```

**Error:**
```python
{
    'status': 'error',
    'message': 'Failed to solve CAPTCHA'
}
```

## 🔧 Advanced Configuration

### Headless Mode (Servers)

```python
recharger = OrangeCreditCardRecharge(headless=True)
```

### Custom Timeout

```python
from selenium.webdriver.support.ui import WebDriverWait

recharger = OrangeCreditCardRecharge()
recharger._setup_driver()
recharger.wait = WebDriverWait(recharger.driver, 30)  # 30 seconds
```

### Network Monitoring (Capture GraphQL)

```python
# Enable network logging
recharger.driver.execute_cdp_cmd('Network.enable', {})

# After clicking Pay, check logs
logs = recharger.driver.get_log('performance')
for log in logs:
    # Parse logs for GraphQL response
    pass
```

## 🛠️ Troubleshooting

### Audio CAPTCHA Not Working

**Problem:** `speech_recognition` not installed

**Solution:**
```bash
pip install SpeechRecognition pydub
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
```

**Problem:** Google Speech API rate limit

**Solution:** Use 2Captcha fallback
```bash
python orange_creditcard.py 53028939 20 --2captcha-key=YOUR_KEY
```

### 2Captcha Errors

**Problem:** Invalid API key

**Solution:**
1. Check key at https://2captcha.com/enterpage
2. Verify balance ($0.50+ minimum)

**Problem:** Timeout

**Solution:** Increase timeout in code
```python
# In solve_recaptcha_2captcha method
for _ in range(120):  # Increase from 60
    time.sleep(2)
    # ...
```

### Payment URL Not Captured

**Problem:** Script says "partial_success"

**Solution:** 
- Check browser (it stays open for 5 seconds)
- Look at Network tab for GraphQL response
- Copy payment URL manually

**Better solution:** Implement proper network interception
```python
# Monitor all network requests
logs = driver.execute_script("return window.performance.getEntries()")
# Filter for GraphQL requests
# Parse response
```

## 💡 Tips

### For Personal Use (1-100 recharges/month)
→ Use **audio method only** (free)
```bash
python orange_creditcard.py 53028939 20
```

### For Regular Use (100-1000 recharges/month)
→ Use **auto mode** with small 2Captcha balance
```bash
python orange_creditcard.py 53028939 20 --2captcha-key=YOUR_KEY
```

### For High Volume (1000+ recharges/month)
→ Use **2Captcha only** (most reliable)
```python
captcha_method='2captcha'
```

## 📊 Cost Analysis

### Free Audio Method
- **Cost:** $0
- **Success rate:** 70% (average)
- **For 1000 recharges:** $0 ✅

### 2Captcha Only
- **Cost:** $0.001/solve
- **Success rate:** 99%
- **For 1000 recharges:** ~$1 💰

### Auto Mode (Recommended)
- **Cost:** ~$0.0003/solve average
- **Success rate:** 95%+
- **For 1000 recharges:** ~$0.30 🎯
- **For 10,000 recharges:** ~$3

## 🔒 Security Notes

- Never commit API keys to git
- Use environment variables for keys
- 2Captcha API key is safe to use (no card details exposed)
- Payment URL is temporary and expires quickly

## 📁 Related Files

- `orange_creditcard.py` - Main automation script
- `requirements.txt` - Python dependencies
- `README.md` - General project info
- `RESPONSES.md` - API response formats

---

**Need help?** Open an issue on GitHub or check the main README.

**Want to save money?** Start with free audio method, add 2Captcha only if needed.

**Pro tip:** For testing, use audio method. For production, use auto mode with a small 2Captcha balance ($3-5).
