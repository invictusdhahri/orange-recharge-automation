# Testing Guide 🧪

Quick guide to test Orange credit card recharge automation with 2Captcha.

## 🚀 Quick Test (5 minutes)

### 1. Clone & Setup

```bash
git clone https://github.com/invictusdhahri/orange-recharge-automation.git
cd orange-recharge-automation

# Install dependencies
pip install -r requirements.txt

# For audio CAPTCHA (optional)
# Linux:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg
```

### 2. Configure API Key

```bash
# Copy .env template
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use any text editor
```

Your `.env` should look like:
```env
TWOCAPTCHA_API_KEY=9d1be5cb29642744ec425ab74d909bb5
TEST_PHONE=53028939
TEST_AMOUNT=20
```

### 3. Run Test

**Easy way (using test script):**
```bash
python test_creditcard.py
```

**Or run directly:**
```bash
python orange_creditcard.py 53028939 20 --2captcha-key=9d1be5cb29642744ec425ab74d909bb5
```

### 4. What to Expect

The script will:
1. ✅ Open Orange recharge page
2. ✅ Fill phone number (53028939)
3. ✅ Select amount (20 DT)
4. ✅ Click "Valider"
5. 🎧 Try FREE audio CAPTCHA first (~15 seconds)
6. 💰 If audio fails → Use 2Captcha (~20 seconds)
7. ✅ Click "Payer"
8. ✅ Capture payment URL from GraphQL

**Expected output:**
```
🚀 Starting Orange credit card recharge...
📞 Entering phone number: 53028939
📞 Confirming phone number...
💰 Selecting amount: 20 DT
✅ Clicking Valider...
🔓 Solving reCAPTCHA...
🎧 Attempting audio CAPTCHA challenge...
📥 Downloading audio challenge...
🎤 Recognizing speech...
✅ Recognized: [text]
✅ Audio CAPTCHA solved!
⏳ Waiting for Pay button...
💳 Clicking Payer...
✅ Payment URL obtained!

===========================================================
RESULT
===========================================================
Status: success
✅ Payment URL obtained!
   https://ipay.clictopay.com:443/epg/merchants/CLICTOPAY/payment.html?mdOrder=xxx&language=fr
===========================================================
```

### 5. Check 2Captcha Balance

```bash
curl "http://2captcha.com/res.php?key=9d1be5cb29642744ec425ab74d909bb5&action=getbalance"
```

---

## 🧪 Test Scenarios

### Test 1: Audio CAPTCHA (Free)

```bash
# Force audio method only
python orange_creditcard.py 53028939 20 --captcha-method=audio
```

**Expected:** 60-80% success rate

### Test 2: 2Captcha Only

```bash
# Force 2Captcha method
python orange_creditcard.py 53028939 20 --2captcha-key=YOUR_KEY
```

**Expected:** 95-99% success rate  
**Cost:** $0.001 (0.1 cents)

### Test 3: Auto Mode (Recommended)

```bash
# Try audio first, fallback to 2Captcha
python test_creditcard.py
```

**Expected:** 95%+ success rate  
**Cost:** ~$0.0003 average

---

## 📊 What Gets Tested

| Component | Status |
|-----------|--------|
| ✅ Form filling | Automated |
| ✅ Math CAPTCHA (scratch card) | 100% success |
| ✅ reCAPTCHA audio bypass | 60-80% success |
| ✅ 2Captcha integration | 95-99% success |
| ✅ GraphQL response capture | Working |
| ✅ Payment URL extraction | Working |

---

## 🔍 Debugging

### Enable verbose logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Keep browser open longer

Edit `orange_creditcard.py`:
```python
finally:
    if self.driver:
        time.sleep(30)  # Keep open for 30 seconds
        # self.driver.quit()  # Comment this out to keep browser open
```

### Check 2Captcha errors

```bash
# Check API key
curl "http://2captcha.com/res.php?key=YOUR_KEY&action=getbalance"

# Check recent solves
curl "http://2captcha.com/res.php?key=YOUR_KEY&action=get&id=CAPTCHA_ID"
```

### Browser not opening?

```bash
# Install Chrome
sudo apt-get install chromium-browser

# Or use Firefox (modify script to use Firefox driver)
```

---

## ✅ Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] ffmpeg installed (for audio CAPTCHA)
- [ ] .env file configured with API key
- [ ] 2Captcha balance > $0.50
- [ ] Chrome/Chromium browser installed
- [ ] Script runs without errors
- [ ] Browser opens Orange page
- [ ] Form gets filled automatically
- [ ] CAPTCHA gets solved
- [ ] Payment URL is captured

---

## 🆘 Common Issues

### "No module named 'selenium'"

```bash
pip install -r requirements.txt
```

### "No module named 'dotenv'"

```bash
pip install python-dotenv
```

### "ffmpeg not found"

```bash
# Linux:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

### "2Captcha error: ERROR_WRONG_USER_KEY"

Check your API key in .env file. Get it from: https://2captcha.com/enterpage

### "CAPTCHA_NOT_READY"

This is normal! 2Captcha needs 15-30 seconds to solve. The script waits automatically.

### "Failed to solve CAPTCHA"

Try again or check your 2Captcha balance:
```bash
curl "http://2captcha.com/res.php?key=YOUR_KEY&action=getbalance"
```

---

## 📈 Expected Costs

### For This Test (20 DT recharge)

- **Audio method:** $0 (free)
- **2Captcha fallback:** $0.001 if audio fails
- **Total:** ~$0.0003 on average

### For 100 Tests

- **Audio only:** $0
- **Auto mode:** ~$0.03
- **2Captcha only:** $0.10

---

## 🎯 Next Steps After Testing

1. ✅ Verify payment URL format
2. ✅ Test with different amounts (10, 50, 100 DT)
3. ✅ Test notification phone number feature
4. ✅ Implement GraphQL response parsing
5. ✅ Add payment URL to database/queue
6. ✅ Integrate with your application

---

## 📞 Support

- **GitHub Issues:** https://github.com/invictusdhahri/orange-recharge-automation/issues
- **2Captcha Support:** https://2captcha.com/support
- **Documentation:** Check CREDITCARD_RECHARGE.md and CAPTCHA_BYPASS.md

---

**Ready to test?** Just run:
```bash
python test_creditcard.py
```

Good luck! 🚀
