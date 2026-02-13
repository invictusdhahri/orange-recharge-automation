# VPS Deployment Guide 🚀

Complete guide to run Orange recharge automation on a VPS (Ubuntu/Debian) without any manual intervention.

---

## 🎯 Quick Deploy (5 minutes)

```bash
# 1. SSH into your VPS
ssh user@your-vps-ip

# 2. Run the auto-installer
curl -sSL https://raw.githubusercontent.com/invictusdhahri/orange-recharge-automation/master/install-vps.sh | bash

# 3. Done! Test it:
cd ~/orange-recharge-automation
python3 test_creditcard.py
```

---

## 📦 Manual Installation (Step by Step)

### 1. Update System

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### 2. Install Python & Dependencies

```bash
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    chromium-browser \
    chromium-chromedriver \
    git \
    ffmpeg
```

### 3. Clone Repository

```bash
cd ~
git clone https://github.com/invictusdhahri/orange-recharge-automation.git
cd orange-recharge-automation
```

### 4. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Packages

```bash
pip install -r requirements.txt
```

### 6. Configure API Key

```bash
# Create .env file
cat > .env << 'EOF'
TWOCAPTCHA_API_KEY=9d1be5cb29642744ec425ab74d909bb5
TEST_PHONE=53028939
TEST_AMOUNT=20
EOF
```

### 7. Test the Automation

```bash
python3 test_creditcard.py
```

Expected output:
```
✅ 2Captcha solved!
💳 Clicking Payer...
⏳ Waiting for GraphQL response...
📍 Payment URL captured!
```

---

## 🐳 Docker Deployment (RECOMMENDED)

Docker ensures consistent environment across all servers.

### 1. Install Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

Log out and back in for group changes to take effect.

### 2. Create Dockerfile

```bash
cd ~/orange-recharge-automation
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set environment to use chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

CMD ["python3", "test_creditcard.py"]
EOF
```

### 3. Build Docker Image

```bash
docker build -t orange-recharge .
```

### 4. Run Container

```bash
docker run --rm \
    -e TWOCAPTCHA_API_KEY=9d1be5cb29642744ec425ab74d909bb5 \
    -e TEST_PHONE=53028939 \
    -e TEST_AMOUNT=20 \
    orange-recharge
```

---

## 🔄 Run as a Service (systemd)

For production deployment that auto-restarts on failure.

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/orange-recharge.service
```

Paste:

```ini
[Unit]
Description=Orange Recharge Automation Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/orange-recharge-automation
Environment="PATH=/home/your-username/orange-recharge-automation/venv/bin"
ExecStart=/home/your-username/orange-recharge-automation/venv/bin/python3 test_creditcard.py
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

**Replace `your-username` with your actual username!**

### 2. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable orange-recharge.service
sudo systemctl start orange-recharge.service
```

### 3. Check Status

```bash
sudo systemctl status orange-recharge.service
```

### 4. View Logs

```bash
sudo journalctl -u orange-recharge.service -f
```

---

## 🌐 API Server (Flask)

Turn the automation into an API that you can call remotely.

### 1. Create API Server

```bash
cat > api_server.py << 'EOF'
from flask import Flask, request, jsonify
from orange_creditcard import OrangeCreditCardRecharge
import os

app = Flask(__name__)

@app.route('/recharge', methods=['POST'])
def recharge():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount', 20)
    
    if not phone:
        return jsonify({'error': 'Phone number required'}), 400
    
    api_key = os.getenv('TWOCAPTCHA_API_KEY')
    recharger = OrangeCreditCardRecharge(twocaptcha_api_key=api_key)
    
    result = recharger.recharge(
        phone_number=phone,
        amount=amount,
        captcha_method='auto'
    )
    
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
```

### 2. Install Flask

```bash
pip install flask
```

### 3. Run API Server

```bash
python3 api_server.py
```

### 4. Test API

```bash
curl -X POST http://your-vps-ip:5000/recharge \
    -H "Content-Type: application/json" \
    -d '{"phone": "53028939", "amount": 20}'
```

---

## 📊 Monitoring & Logging

### 1. Setup Logging

```bash
mkdir -p ~/orange-recharge-automation/logs
```

Update `.env`:
```bash
LOG_FILE=logs/recharge.log
LOG_LEVEL=INFO
```

### 2. View Logs

```bash
tail -f logs/recharge.log
```

### 3. Log Rotation

```bash
sudo nano /etc/logrotate.d/orange-recharge
```

Paste:
```
/home/your-username/orange-recharge-automation/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## 🔐 Security Best Practices

### 1. Use Environment Variables

Never commit API keys! Always use `.env`:

```bash
# .gitignore should include:
.env
.env.*
!.env.example
```

### 2. Firewall Configuration

```bash
# Allow only SSH and your API port
sudo ufw allow 22/tcp
sudo ufw allow 5000/tcp
sudo ufw enable
```

### 3. Reverse Proxy (Nginx)

For production API:

```bash
sudo apt-get install nginx

sudo nano /etc/nginx/sites-available/orange-recharge
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/orange-recharge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🚨 Troubleshooting

### Chrome Not Found

```bash
# Install Chromium
sudo apt-get install chromium-browser chromium-chromedriver

# Or use Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```

### Element Click Intercepted

Already fixed in latest version! Update:
```bash
git pull origin master
```

### 2Captcha Timeout

Increase timeout in `orange_creditcard.py`:
```python
for _ in range(60):  # Increase from 60 to 90
    time.sleep(2)
    # ...
```

### Memory Issues on Small VPS

Use swap file:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 💰 VPS Recommendations

### Minimum Requirements
- **RAM:** 1GB
- **CPU:** 1 core
- **Storage:** 10GB
- **OS:** Ubuntu 20.04+

### Recommended Providers

| Provider | Price/Month | RAM | Notes |
|----------|-------------|-----|-------|
| **DigitalOcean** | $6 | 1GB | Easy setup, reliable |
| **Hetzner** | €4 | 2GB | Best value, EU location |
| **Linode** | $5 | 1GB | Good performance |
| **Vultr** | $5 | 1GB | Many locations |

### Setup Times
- DigitalOcean: ~5 minutes
- Hetzner: ~10 minutes (pending verification)
- Linode: ~5 minutes
- Vultr: ~5 minutes

---

## 🔄 Auto-Update Script

Keep the automation updated:

```bash
cat > ~/update-orange-recharge.sh << 'EOF'
#!/bin/bash
cd ~/orange-recharge-automation
git pull origin master
source venv/bin/activate
pip install -r requirements.txt --upgrade
echo "Updated successfully!"
EOF

chmod +x ~/update-orange-recharge.sh
```

Run weekly with cron:
```bash
crontab -e
```

Add:
```
0 2 * * 0 /home/your-username/update-orange-recharge.sh
```

---

## 📈 Performance Monitoring

### Track Success Rate

```python
# Add to test_creditcard.py
import json
from datetime import datetime

def log_result(result):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'status': result['status'],
        'duration': time.time() - start_time
    }
    
    with open('performance.log', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
```

### Generate Report

```bash
cat performance.log | jq -s 'group_by(.status) | map({status: .[0].status, count: length})'
```

---

## 🎯 Quick Commands Cheat Sheet

```bash
# Start service
sudo systemctl start orange-recharge

# Stop service
sudo systemctl stop orange-recharge

# Restart service
sudo systemctl restart orange-recharge

# View logs
sudo journalctl -u orange-recharge -f

# Test manually
cd ~/orange-recharge-automation && source venv/bin/activate && python3 test_creditcard.py

# Update code
cd ~/orange-recharge-automation && git pull

# Check 2Captcha balance
curl "http://2captcha.com/res.php?key=9d1be5cb29642744ec425ab74d909bb5&action=getbalance"
```

---

## ✅ Deployment Checklist

- [ ] VPS created and accessible via SSH
- [ ] System updated (`apt-get update && upgrade`)
- [ ] Python 3.9+ installed
- [ ] Chromium browser installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured with API key
- [ ] Test successful (`python3 test_creditcard.py`)
- [ ] Service configured (optional)
- [ ] API server setup (optional)
- [ ] Monitoring enabled (optional)
- [ ] Firewall configured
- [ ] Auto-update scheduled (optional)

---

## 🆘 Support

- **GitHub Issues:** https://github.com/invictusdhahri/orange-recharge-automation/issues
- **Documentation:** Check other .md files in repo
- **2Captcha Support:** https://2captcha.com/support

---

**Status:** ✅ Production Ready  
**Last Updated:** February 13, 2026  
**Tested On:** Ubuntu 20.04, Ubuntu 22.04, Debian 11
