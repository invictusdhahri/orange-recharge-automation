#!/bin/bash
#
# Orange Tunisia Recharge Automation - VPS Auto-Installer
# Usage: curl -sSL https://raw.githubusercontent.com/invictusdhahri/orange-recharge-automation/master/install-vps.sh | bash
#

set -e

echo "🚀 Orange Recharge Automation - VPS Installer"
echo "=============================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "⚠️  Please don't run as root. Run as your normal user."
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -qq

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-venv \
    chromium-browser \
    chromium-chromedriver \
    git \
    ffmpeg \
    curl

# Clone repository
echo "📥 Cloning repository..."
cd ~
if [ -d "orange-recharge-automation" ]; then
    echo "   Repository already exists, pulling latest..."
    cd orange-recharge-automation
    git pull
else
    git clone https://github.com/invictusdhahri/orange-recharge-automation.git
    cd orange-recharge-automation
fi

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env configuration..."
    cat > .env << 'EOF'
# 2Captcha API Key
TWOCAPTCHA_API_KEY=9d1be5cb29642744ec425ab74d909bb5

# Test phone number
TEST_PHONE=53028939

# Test amount
TEST_AMOUNT=20
EOF
    echo "   Created .env file with default configuration"
else
    echo "   .env file already exists, keeping current configuration"
fi

# Test installation
echo ""
echo "✅ Installation complete!"
echo ""
echo "📍 Installation directory: ~/orange-recharge-automation"
echo ""
echo "🧪 To test the automation:"
echo "   cd ~/orange-recharge-automation"
echo "   source venv/bin/activate"
echo "   python3 test_creditcard.py"
echo ""
echo "📚 For more options, see VPS_DEPLOYMENT.md"
echo ""
