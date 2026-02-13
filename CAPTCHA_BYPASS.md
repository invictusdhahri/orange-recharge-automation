# reCAPTCHA Bypass Guide 🔓

Complete guide to bypassing Orange Tunisia's reCAPTCHA for credit card recharges.

## 🎯 Quick Decision Guide

**Just testing?** → Use **FREE audio method**
```bash
pip install SpeechRecognition pydub
sudo apt-get install ffmpeg
python orange_creditcard.py 53028939 20
```

**Production use?** → Use **Auto mode** (free + paid fallback)
```bash
python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_KEY
```

**High volume?** → Use **2Captcha only**
```python
captcha_method='2captcha'
```

---

## Method 1: FREE Audio Challenge 🎧

### How It Works

1. **Click reCAPTCHA** → Triggers challenge
2. **Click audio button** → Get audio CAPTCHA
3. **Download audio** → Save .mp3 file
4. **Convert to WAV** → Process audio
5. **Speech recognition** → Google Speech API (free)
6. **Submit answer** → Solve CAPTCHA

### Setup

```bash
# 1. Install Python dependencies
pip install SpeechRecognition pydub

# 2. Install ffmpeg (audio processing)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

### Usage

```bash
python orange_creditcard.py 53028939 20
```

Or in code:
```python
from orange_creditcard import OrangeCreditCardRecharge

recharger = OrangeCreditCardRecharge()
result = recharger.recharge(
    phone_number="53028939",
    amount=20,
    captcha_method='audio'  # Force audio method
)
```

### Pros & Cons

**Pros ✅**
- Completely FREE ($0)
- No external service
- No API keys needed
- 60-80% success rate
- Privacy-friendly (runs locally)

**Cons ❌**
- Requires audio processing setup (ffmpeg)
- Google Speech API has rate limits (~50 requests/day from same IP)
- Fails on difficult/noisy audio
- Slower than 2Captcha (15-25 seconds)

### Success Rate by Scenario

| Scenario | Success Rate |
|----------|--------------|
| **First 10 attempts** | ~80% |
| **After 50 attempts/day** | ~60% (rate limiting) |
| **With VPN rotation** | ~75% |
| **Clean audio** | ~90% |
| **Noisy audio** | ~50% |

### Troubleshooting

**Problem:** `No module named 'speech_recognition'`
```bash
pip install SpeechRecognition pydub
```

**Problem:** `ffmpeg not found`
```bash
# Linux:
sudo apt-get install ffmpeg

# Mac:
brew install ffmpeg
```

**Problem:** Rate limit exceeded
```
Solution: Wait a few hours, or use 2Captcha fallback
```

**Problem:** Recognition accuracy low
```
Solution: Audio might be too noisy, try again or use 2Captcha
```

**Problem:** "Audio CAPTCHA failed" but checkbox is actually checked
```
Fixed in latest version! Script now verifies checkbox state after solving.
If you still see this, update to latest version:
git pull origin main
```

**Problem:** 2Captcha token received but checkbox not checked
```
This is a server-side validation issue with Orange Tunisia.
The checkbox verification was added to catch this correctly.
Solution: Use auto mode - will retry with different method.
```

---

## Method 2: 2Captcha Service 💰

### How It Works

1. **Extract site key** → Get reCAPTCHA key from page
2. **Send to 2Captcha** → API request with site key + page URL
3. **Human workers solve** → Real people solve the CAPTCHA
4. **Get token** → Receive solution token
5. **Inject token** → Insert into page
6. **Submit** → CAPTCHA bypassed!

### Setup

1. **Sign up at 2Captcha**
   - Go to: https://2captcha.com/?from=6591885
   - Create account
   - Add funds ($3-10 recommended)

2. **Get API key**
   - Dashboard → Settings → API Key
   - Copy the key (starts with uppercase letters)

3. **Use in script**
   ```bash
   python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_API_KEY
   ```

### Pricing

| Package | Solves | Cost per Solve | Total |
|---------|--------|----------------|-------|
| **Starter** | 3,000 | $0.001 | $3 |
| **Basic** | 10,000 | $0.001 | $10 |
| **Pro** | 50,000 | $0.0008 | $40 |
| **Enterprise** | 100,000+ | $0.0006 | Custom |

**Real-world cost:**
- 100 recharges = $0.10
- 1,000 recharges = $1.00
- 10,000 recharges = $10.00

### Usage

```bash
python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_KEY
```

Or in code:
```python
from orange_creditcard import OrangeCreditCardRecharge

recharger = OrangeCreditCardRecharge(twocaptcha_api_key='YOUR_KEY')
result = recharger.recharge(
    phone_number="53028939",
    amount=50,
    captcha_method='2captcha'  # Force 2Captcha
)
```

### Pros & Cons

**Pros ✅**
- Very high success rate (95-99%)
- Fast (15-30 seconds)
- Reliable and consistent
- No setup complexity
- Works for all reCAPTCHA types

**Cons ❌**
- Costs money ($0.001/solve)
- Requires API key
- Depends on external service
- Rate limited (but high limits)

### Success Rate

| Metric | Value |
|--------|-------|
| **Success rate** | 95-99% |
| **Average time** | 20 seconds |
| **Max time** | 120 seconds |
| **Timeout rate** | <1% |

---

## Method 3: Auto Mode (RECOMMENDED) 🚀

### How It Works

1. **Try audio first** → Attempt free audio challenge
2. **If fails** → Fallback to 2Captcha
3. **Return result** → Success from either method

### Setup

```bash
# 1. Install audio dependencies
pip install SpeechRecognition pydub
sudo apt-get install ffmpeg

# 2. Get 2Captcha API key (optional but recommended)
# Sign up at https://2captcha.com/?from=6591885

# 3. Run with both methods available
python orange_creditcard.py 53028939 20 --2captcha-key=YOUR_KEY
```

### Usage

```bash
# Auto mode (default)
python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_KEY
```

Or in code:
```python
recharger = OrangeCreditCardRecharge(twocaptcha_api_key='YOUR_KEY')
result = recharger.recharge(
    phone_number="53028939",
    amount=50,
    captcha_method='auto'  # Default, best option!
)
```

### Cost Analysis

**Scenario:** 1000 recharges

| Method | Success Rate | Paid Solves | Cost |
|--------|--------------|-------------|------|
| Audio only | 70% | 0 | $0 |
| 2Captcha only | 99% | 1000 | $1.00 |
| **Auto mode** | **95%+** | **~300** | **$0.30** |

**Why auto mode is best:**
- 70% of requests succeed with free audio
- 30% fallback to paid 2Captcha
- Total cost: ~$0.30 per 1000 recharges
- Best reliability + minimal cost

### Pros & Cons

**Pros ✅**
- Best of both worlds
- High success rate (95%+)
- Very low cost (~$0.0003/solve average)
- Automatic fallback
- No manual intervention

**Cons ❌**
- Requires both setups (audio + 2Captcha)
- Slightly more complex
- Still has small cost

---

## 📊 Complete Comparison

| Feature | Audio (Free) | 2Captcha (Paid) | Auto (Hybrid) |
|---------|-------------|-----------------|---------------|
| **Success Rate** | 60-80% | 95-99% | 95%+ |
| **Cost/1000** | $0 | $1.00 | $0.30 |
| **Speed** | 15-25s | 15-30s | 15-30s |
| **Setup** | Medium | Easy | Medium |
| **Reliability** | Medium | High | High |
| **Best For** | Testing | High volume | Production |

---

## 💡 Recommendations

### For Different Use Cases

**Personal testing (1-10 recharges)**
→ **Audio only** (free)
```bash
python orange_creditcard.py 53028939 20
```

**Small business (10-100/month)**
→ **Auto mode** with $3 2Captcha balance
```bash
python orange_creditcard.py 53028939 20 --2captcha-key=YOUR_KEY
```

**Medium business (100-1000/month)**
→ **Auto mode** with $10 2Captcha balance
- Cost: ~$3-5/month
- Success rate: 95%+

**Large business (1000+/month)**
→ **2Captcha only** for maximum reliability
```python
captcha_method='2captcha'
```
- Cost: ~$10-30/month
- Success rate: 99%

---

## 🔧 Advanced Tips

### Improve Audio Success Rate

1. **Rotate IPs** → Avoid rate limiting
   ```python
   # Use VPN or proxy rotation
   chrome_options.add_argument('--proxy-server=your_proxy')
   ```

2. **Add delays** → Look more human
   ```python
   time.sleep(random.uniform(2, 5))  # Random delays
   ```

3. **Better audio processing**
   ```python
   # Denoise audio before recognition
   from scipy.signal import wiener
   denoised = wiener(audio_data)
   ```

### Reduce 2Captcha Cost

1. **Cache solved CAPTCHAs** → Reuse for same session
2. **Batch requests** → Process multiple in parallel
3. **Use worker pool** → Optimize API calls

### Monitor Success Rates

```python
import json

stats = {
    'audio_attempts': 0,
    'audio_success': 0,
    'captcha_attempts': 0,
    'captcha_success': 0
}

# After each attempt
stats['audio_attempts'] += 1
if audio_solved:
    stats['audio_success'] += 1

# Calculate rates
audio_rate = stats['audio_success'] / stats['audio_attempts']
print(f"Audio success rate: {audio_rate:.1%}")
```

---

## ❓ FAQ

### Q: Is audio bypass legal?
**A:** Yes, you're using reCAPTCHA's official accessibility feature (audio challenge). It's intended for users who can't see images.

### Q: Will Google ban my IP?
**A:** Unlikely for personal use (<50/day). For high volume, rotate IPs or use 2Captcha.

### Q: Can I use only free method?
**A:** Yes! Just install audio dependencies and run without 2Captcha key. Success rate ~70%.

### Q: Is 2Captcha safe?
**A:** Yes, it's a legitimate service used by thousands of developers. No payment card details are exposed.

### Q: What if both methods fail?
**A:** Very rare (<1%). Script will return error. You can retry or solve manually.

### Q: Can I contribute to 2Captcha costs?
**A:** Script logs which method was used. You can track costs and adjust strategy.

---

## 🎯 Quick Start Commands

**Test audio (free):**
```bash
pip install SpeechRecognition pydub
sudo apt-get install ffmpeg
python orange_creditcard.py 53028939 20
```

**Production (auto mode):**
```bash
# 1. Get 2Captcha key from https://2captcha.com/?from=6591885
# 2. Add $3-5 balance
# 3. Run:
python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_KEY
```

**Check balance:**
```bash
curl "http://2captcha.com/res.php?key=YOUR_KEY&action=getbalance"
```

---

**Need help?** Check [CREDITCARD_RECHARGE.md](CREDITCARD_RECHARGE.md) or open a GitHub issue!
