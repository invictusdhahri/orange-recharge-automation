# Orange Tunisia Recharge Automation 🍊

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automated recharge system for Orange Tunisia with **multiple methods**:
- 🎫 **Scratch card recharge** - Math CAPTCHA (super easy!)
- 💳 **Credit card recharge** - reCAPTCHA with FREE audio bypass (~60% success) + 2Captcha fallback

## ✨ Features

### Scratch Card Recharge
- ✅ **No login required** - Direct recharge submission
- 🧮 **Math CAPTCHA solving** - Automatic equation solving (e.g., "10 + 7")
- 🚀 **Fast & reliable** - Clean GraphQL API
- 📊 **Clear responses** - Simple success/error detection

### Credit Card Recharge
- 💳 **Get payment URL** - Automated form filling + CAPTCHA bypass
- 🆓 **FREE reCAPTCHA bypass** - Audio challenge + speech recognition (~60-80% success)
- 💰 **2Captcha fallback** - Optional paid service (~99% success, $0.001/solve)
- 🔄 **Auto mode** - Try free first, fallback to paid ($0.30 per 1000 recharges)
- 🔧 **Production-ready** - Error handling and validation

## 🆚 Orange vs Ooredoo

| Feature | Orange | Ooredoo |
|---------|--------|---------|
| **Login** | ❌ Not needed | ✅ Required |
| **CAPTCHA Type** | Math equation | Text OCR |
| **Difficulty** | ⭐ Easy | ⭐⭐⭐ Medium |
| **API** | GraphQL | HTML forms |
| **Automation** | ⭐⭐⭐ Easy | ⭐⭐ Medium |

## 📋 Requirements

- Python 3.8+
- Chrome browser
- ChromeDriver (automatically managed by selenium)

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/invictusdhahri/orange-recharge-automation.git
cd orange-recharge-automation
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 💡 Usage

### Method 1: Scratch Card Recharge

**Basic:**
```bash
python orange_recharge.py <phone_number> <recharge_code>
```

**Example:**
```bash
python orange_recharge.py 53028939 1234567890123
```

**Headless mode:**
```bash
python orange_recharge.py 53028939 1234567890123 --headless
```

### Method 2: Credit Card Recharge 💳

**FREE (audio CAPTCHA):**
```bash
python orange_creditcard.py 53028939 20
```

**With 2Captcha fallback (recommended):**
```bash
python orange_creditcard.py 53028939 50 --2captcha-key=YOUR_KEY
```

**Full documentation:** [CREDITCARD_RECHARGE.md](CREDITCARD_RECHARGE.md)

### Programmatic Usage

```python
from orange_recharge import recharge_orange

result = recharge_orange(
    phone_number="53028939",
    recharge_code="1234567890123",
    headless=True
)

if result['status'] == 'success':
    print(f"✅ Recharge successful!")
    print(f"Phone: {result['phone']}")
else:
    print(f"❌ Failed: {result['message']}")
```

## 📊 Response Format

### Success Response

```json
{
  "status": "success",
  "message": "Opération effectuée avec succès",
  "phone": "53028939",
  "code": "1234567890123"
}
```

**GraphQL Backend:**
```json
{
  "data": {
    "topupWithScratchCard": true
  }
}
```

### Error Response (Invalid Code)

```json
{
  "status": "invalid_code",
  "message": "Code de recharge invalide"
}
```

**GraphQL Backend:**
```json
{
  "errors": [
    {
      "message": "errors.topupWithScratch.invalidScratch",
      "extensions": {
        "code": "BAD_USER_INPUT"
      }
    }
  ]
}
```

## 🧮 Math CAPTCHA Solver

The script automatically solves simple math equations:

| Equation | Answer | Operators |
|----------|--------|-----------|
| `10 + 7` | `17` | Addition |
| `20 - 8` | `12` | Subtraction |
| `5 * 3` | `15` | Multiplication |
| `15 / 3` | `5` | Division |

**Code:**
```python
def solve_math_captcha(equation_text):
    """
    Solve: "10 + 7" → 17
    """
    match = re.match(r'(\d+)\s*([+\-*/])\s*(\d+)', equation_text)
    num1, operator, num2 = match.groups()
    num1, num2 = int(num1), int(num2)
    
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 // num2
```

## 🔧 How It Works

1. **Open recharge page:** `https://www.orange.tn/recharge-par-carte-de-recharge`
2. **Fill form:**
   - Phone number (e.g., `53028939`)
   - Confirmation phone number
   - Recharge code (13-14 digits)
3. **Read math CAPTCHA:** Extract equation from page (e.g., "10 + 7")
4. **Solve equation:** Calculate answer (`17`)
5. **Submit form:** Send to GraphQL API
6. **Parse response:** Check for success or error

## 🎯 Why Orange is Easier

### Orange
- **CAPTCHA:** Simple math equation → 100% accuracy
- **API:** Clean GraphQL responses
- **Login:** Not required
- **Automation:** Straightforward

### Ooredoo
- **CAPTCHA:** Distorted text → needs OCR (80-90% accuracy)
- **API:** HTML form parsing
- **Login:** Session management required
- **Automation:** More complex

## 🆚 Method Comparison

| Feature | Scratch Card | Credit Card |
|---------|--------------|-------------|
| **CAPTCHA** | Math equation (easy) | reCAPTCHA v2 (hard) |
| **CAPTCHA Bypass** | 100% success (simple math) | 60-99% (audio/2Captcha) |
| **Cost** | $0 (completely free) | $0-0.001/recharge |
| **Use Case** | Have recharge codes | Need to generate payment URL |
| **Speed** | ⚡ Fast (~5-10s) | ⏱️ Medium (~15-30s) |
| **Complexity** | ⭐ Easy | ⭐⭐ Medium |

## 📁 Project Structure

```
orange-recharge-automation/
├── orange_recharge.py           # Scratch card automation
├── orange_creditcard.py         # Credit card automation
├── requirements.txt              # Python dependencies
├── README.md                    # This file
├── CREDITCARD_RECHARGE.md       # Credit card detailed docs
├── RESPONSES.md                 # API response formats
├── LICENSE                      # MIT License
└── .gitignore                  # Git ignore rules
```

## 🔒 Security

- **No credentials stored** - No login required
- **No API keys needed** - Direct browser automation
- **Local execution** - Runs on your machine
- **Open source** - Full code transparency

## ⚠️ Disclaimer

This tool is for **educational purposes** and personal use. Use responsibly:

- Only recharge your own phone numbers
- Respect Orange Tunisia's terms of service
- Don't use for bulk/commercial operations
- Not affiliated with Orange Tunisia

## 🛠️ Troubleshooting

### "ChromeDriver not found"
```bash
# Selenium 4.x+ manages drivers automatically
# If issues persist, install manually:
pip install webdriver-manager
```

### "Element not found"
- Orange's website might have changed
- Check if the site is accessible
- Try running without `--headless` to see what's happening

### CAPTCHA solving fails
- The math CAPTCHA format changed
- Check the equation format in browser
- Open an issue with the new format

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🔗 Related Projects

- [Ooredoo Recharge Automation](https://github.com/invictusdhahri/ooredoo-recharge-automation) - Text CAPTCHA (harder)

## 📧 Contact

- GitHub: [@invictusdhahri](https://github.com/invictusdhahri)
- Issues: [GitHub Issues](https://github.com/invictusdhahri/orange-recharge-automation/issues)

---

**Made with ❤️ by Amen Dhahri**
