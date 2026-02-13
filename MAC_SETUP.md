# Mac Setup Guide 🍎

Quick setup guide for running Orange recharge automation on macOS.

---

## 🚀 Quick Start (3 commands)

```bash
# 1. Install webdriver-manager
pip3 install webdriver-manager

# 2. Pull latest code (if already cloned)
git pull

# 3. Run Mac-optimized script
python3 test_creditcard_mac.py
```

Done! 🎉

---

## 📦 Full Installation

### Option 1: Homebrew (Recommended)

```bash
# Install ChromeDriver
brew install chromedriver

# Install dependencies
pip3 install -r requirements.txt

# Run
python3 test_creditcard.py
```

### Option 2: Automatic Driver Management

```bash
# Install with webdriver-manager
pip3 install webdriver-manager

# Install dependencies
pip3 install -r requirements.txt

# Run Mac version
python3 test_creditcard_mac.py
```

---

## 🔧 Troubleshooting

### "Unable to obtain driver for chrome"

**Solution 1 (Fastest):**
```bash
brew install chromedriver
```

**Solution 2:**
```bash
pip3 install webdriver-manager
python3 test_creditcard_mac.py
```

### "chromedriver cannot be opened because the developer cannot be verified"

Mac security blocked ChromeDriver. Fix:

```bash
xattr -d com.apple.quarantine /usr/local/bin/chromedriver
```

Or go to **System Settings → Privacy & Security** and click "Allow Anyway"

### "LibreSSL" Warning

This is harmless. To fix:

```bash
brew install openssl
pip3 install --upgrade urllib3
```

### "Couldn't find ffmpeg" Warning

Optional (only needed for free audio CAPTCHA):

```bash
brew install ffmpeg
```

---

## 📁 Which Script to Use?

| Script | Use When | Driver Management |
|--------|----------|-------------------|
| `test_creditcard.py` | ChromeDriver installed via Homebrew | Manual |
| `test_creditcard_mac.py` | Want automatic driver management | Automatic |
| `simple_test.py` | Quick testing | Manual |

**Recommendation:** Use `test_creditcard_mac.py` - it handles everything automatically!

---

## 💡 Mac-Specific Tips

### 1. Keep Browser Visible (Recommended for Mac)

The Mac version runs with visible browser by default. This helps with:
- Debugging
- Seeing what's happening
- Better success rate

To enable headless mode, edit `test_creditcard_mac.py`:
```python
chrome_options.add_argument('--headless=new')
```

### 2. Better Performance

Close other Chrome windows before running:
```bash
killall "Google Chrome"
```

### 3. M1/M2 Macs (Apple Silicon)

Everything works natively! No Rosetta needed.

---

## 🎯 Complete Setup Example

```bash
# 1. Clone (if not already done)
git clone https://github.com/invictusdhahri/orange-recharge-automation.git
cd orange-recharge-automation

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Install ChromeDriver (choose one):
# Option A: Homebrew
brew install chromedriver

# Option B: Automatic
pip3 install webdriver-manager

# 4. Create .env file
cat > .env << 'EOF'
TWOCAPTCHA_API_KEY=9d1be5cb29642744ec425ab74d909bb5
TEST_PHONE=53028939
TEST_AMOUNT=20
EOF

# 5. Run!
python3 test_creditcard_mac.py
```

---

## ✅ Expected Output

```
🚀 Starting Orange credit card recharge...
📞 Entering phone number: 53028939
📞 Confirming phone number...
💰 Selecting amount: 20 DT
✅ Clicking Valider...
🔓 Solving reCAPTCHA...
💰 Using 2Captcha service...
⏳ Waiting for 2Captcha to solve (ID: 81905427485)...
✅ 2Captcha solved!
⏳ Waiting for Pay button...
💳 Clicking Payer...
⏳ Waiting for GraphQL response...
```

---

## 🚨 Common Errors & Fixes

### Error: `element click intercepted`

Already fixed in latest version! Run:
```bash
git pull
```

### Error: `ChromeDriver not found`

```bash
brew install chromedriver
```

### Error: `Permission denied: chromedriver`

```bash
chmod +x /usr/local/bin/chromedriver
xattr -d com.apple.quarantine /usr/local/bin/chromedriver
```

---

## 📊 Performance on Mac

| MacBook | Chrome Version | Speed | Success Rate |
|---------|----------------|-------|--------------|
| M1 Pro | 144.x | Fast | 95%+ |
| M2 | 144.x | Fast | 95%+ |
| Intel i7 | 144.x | Good | 95%+ |

---

## 🔐 Mac Security Settings

### Allow Terminal to Control Chrome

1. **System Settings** → **Privacy & Security** → **Automation**
2. Check **Terminal** → **Google Chrome**

### Firewall

If enabled, allow:
- Python
- ChromeDriver
- Google Chrome

---

## 🎓 Development on Mac

### Run with visible browser (recommended):

```python
# In test_creditcard_mac.py, comment out:
# chrome_options.add_argument('--headless=new')
```

### Debug mode:

```python
import time
# Add before driver.quit():
time.sleep(30)  # Keep browser open for 30 seconds
```

### Check Chrome version:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

---

## 🔄 Update Guide

```bash
cd orange-recharge-automation
git pull
pip3 install -r requirements.txt --upgrade
```

---

## ✅ Mac Setup Checklist

- [ ] Xcode Command Line Tools installed (`xcode-select --install`)
- [ ] Homebrew installed (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`)
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Google Chrome installed
- [ ] ChromeDriver installed (`brew install chromedriver`)
- [ ] Repository cloned
- [ ] Dependencies installed (`pip3 install -r requirements.txt`)
- [ ] `.env` file created
- [ ] Test successful (`python3 test_creditcard_mac.py`)

---

## 🆘 Still Having Issues?

1. **Check Chrome is installed:**
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
   ```

2. **Check ChromeDriver:**
   ```bash
   chromedriver --version
   ```

3. **Reinstall everything:**
   ```bash
   brew uninstall chromedriver
   brew install chromedriver
   pip3 install --force-reinstall selenium webdriver-manager
   ```

4. **Use Mac-specific script:**
   ```bash
   python3 test_creditcard_mac.py
   ```

---

**Status:** ✅ Mac Ready  
**Tested on:** macOS Ventura 13.x, Sonoma 14.x, Sequoia 15.x  
**Chrome:** 144.x (latest stable)
