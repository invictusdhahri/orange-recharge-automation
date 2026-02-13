#!/usr/bin/env python3
"""
Orange Tunisia Credit Card Recharge Automation
With FREE reCAPTCHA bypass (audio challenge + speech recognition)
+ 2Captcha fallback option
"""

import os
import re
import time
import base64
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Optional: for audio CAPTCHA bypass
try:
    import speech_recognition as sr
    from pydub import AudioSegment
    HAS_SPEECH_RECOGNITION = True
except ImportError:
    HAS_SPEECH_RECOGNITION = False


class OrangeCreditCardRecharge:
    """
    Orange Tunisia credit card recharge with reCAPTCHA bypass
    """
    
    def __init__(self, twocaptcha_api_key=None, headless=False):
        """
        Args:
            twocaptcha_api_key (str): 2Captcha API key (optional, for fallback)
            headless (bool): Run browser in headless mode
        """
        self.twocaptcha_api_key = twocaptcha_api_key
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def _setup_driver(self):
        """Setup Chrome driver with options"""
        import sys
        chrome_options = Options()
        
        # Use headless mode on Linux servers, visible on Mac/Windows for better compatibility
        if self.headless or sys.platform.startswith('linux'):
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Use Chromium if available (Linux only)
        import sys
        if sys.platform.startswith('linux'):
            chrome_options.binary_location = '/usr/bin/chromium'
        # On Mac, let Selenium find Chrome automatically
        
        # Anti-detection measures
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_cdp_cmd('Network.enable', {})
        
        # Hide webdriver property
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        self.wait = WebDriverWait(self.driver, 20)
        
    def solve_recaptcha_audio(self):
        """
        FREE method: Solve reCAPTCHA using audio challenge + speech recognition
        Returns: True if solved, False if failed
        """
        if not HAS_SPEECH_RECOGNITION:
            print("⚠️  speech_recognition not installed. Install with:")
            print("   pip install SpeechRecognition pydub")
            return False
        
        # Check if ffmpeg is available
        import shutil
        if not shutil.which('ffmpeg') and not shutil.which('ffprobe'):
            print("⚠️  ffmpeg not installed. Install with:")
            print("   brew install ffmpeg  (Mac)")
            print("   Skipping audio method, using 2Captcha instead...")
            return False
        
        try:
            print("🎧 Attempting audio CAPTCHA challenge...")
            
            # Switch to reCAPTCHA iframe
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"]'))
            )
            self.driver.switch_to.frame(iframe)
            
            # Click the checkbox first
            checkbox = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'recaptcha-checkbox-border'))
            )
            checkbox.click()
            time.sleep(2)
            
            # Switch back to main content
            self.driver.switch_to.default_content()
            
            # Switch to challenge iframe
            challenge_iframe = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="bframe"]'))
            )
            self.driver.switch_to.frame(challenge_iframe)
            
            # Click audio button
            audio_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'recaptcha-audio-button'))
            )
            audio_button.click()
            time.sleep(2)
            
            # Get audio source URL
            audio_source = self.wait.until(
                EC.presence_of_element_located((By.ID, 'audio-source'))
            )
            audio_url = audio_source.get_attribute('src')
            
            # Download audio file
            print("📥 Downloading audio challenge...")
            response = requests.get(audio_url)
            audio_path = Path('/tmp/recaptcha_audio.mp3')
            audio_path.write_bytes(response.content)
            
            # Convert to WAV for speech recognition
            audio = AudioSegment.from_mp3(str(audio_path))
            wav_path = Path('/tmp/recaptcha_audio.wav')
            audio.export(str(wav_path), format='wav')
            
            # Recognize speech
            print("🎤 Recognizing speech...")
            recognizer = sr.Recognizer()
            with sr.AudioFile(str(wav_path)) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
            
            print(f"✅ Recognized: {text}")
            
            # Enter the answer
            audio_input = self.driver.find_element(By.ID, 'audio-response')
            audio_input.send_keys(text.lower())
            audio_input.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # Switch back to main content
            self.driver.switch_to.default_content()
            
            # Verify CAPTCHA was actually solved by checking checkbox state
            # Poll for up to 10 seconds to see if checkbox gets checked
            print("🔍 Verifying checkbox state...")
            checkbox_checked = False
            
            for verify_attempt in range(10):  # 10 attempts x 1 second = 10 seconds max
                time.sleep(1)
                
                try:
                    # Switch to checkbox iframe to verify
                    checkbox_iframe = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"][src*="anchor"]'))
                    )
                    self.driver.switch_to.frame(checkbox_iframe)
                    
                    # Look for the checkmark (aria-checked="true")
                    checkbox = self.driver.find_element(By.ID, 'recaptcha-anchor')
                    is_checked = checkbox.get_attribute('aria-checked')
                    
                    self.driver.switch_to.default_content()
                    
                    if is_checked == 'true':
                        print(f"✅ Checkbox verified as checked (after {verify_attempt + 1}s)")
                        checkbox_checked = True
                        break
                    else:
                        # Still not checked, keep polling
                        if verify_attempt % 3 == 0 and verify_attempt > 0:
                            print(f"⏳ Still waiting for checkbox... ({verify_attempt + 1}s)")
                            
                except Exception as verify_error:
                    # If we can't find iframe/checkbox, break out
                    print(f"⚠️  Verification error: {verify_error}")
                    self.driver.switch_to.default_content()
                    break
            
            if checkbox_checked:
                print("✅ Audio CAPTCHA solved successfully!")
                return True
            else:
                print("❌ Audio CAPTCHA not verified (checkbox not checked after 10s)")
                return False
            
        except Exception as e:
            print(f"❌ Audio CAPTCHA failed: {str(e)}")
            self.driver.switch_to.default_content()
            return False
    
    def solve_recaptcha_2captcha(self, sitekey):
        """
        PAID method: Solve reCAPTCHA using 2Captcha service
        Args:
            sitekey (str): reCAPTCHA site key
        Returns: True if solved, False if failed
        """
        if not self.twocaptcha_api_key:
            print("⚠️  2Captcha API key not provided")
            return False
        
        try:
            print("💰 Using 2Captcha service...")
            
            # Quick balance check to validate API key
            success, balance, message = self.check_2captcha_balance()
            if not success:
                print(f"❌ 2Captcha API key validation failed: {message}")
                return False
            print(f"   💵 Account balance: ${balance:.2f}")
            
            # Click the checkbox first to initialize reCAPTCHA
            print("   🖱️  Clicking reCAPTCHA checkbox to initialize...")
            try:
                # Switch to reCAPTCHA iframe
                iframe = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"][src*="anchor"]'))
                )
                self.driver.switch_to.frame(iframe)
                
                # Click the checkbox
                checkbox = self.wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'recaptcha-checkbox-border'))
                )
                self.driver.execute_script("arguments[0].click();", checkbox)
                
                # Poll checkbox state for up to 8 seconds to see if it auto-solves
                print("   ⏳ Checking if reCAPTCHA auto-solved...")
                auto_solved = False
                
                for check_attempt in range(8):  # 8 attempts x 1 second = 8 seconds
                    time.sleep(1)
                    
                    # Re-find the checkbox element and check state
                    checkbox_elem = self.driver.find_element(By.ID, 'recaptcha-anchor')
                    is_checked = checkbox_elem.get_attribute('aria-checked')
                    
                    if is_checked == 'true':
                        print(f"   🎉 reCAPTCHA auto-solved after {check_attempt + 1}s! No 2Captcha needed!")
                        auto_solved = True
                        break
                    elif check_attempt > 0 and check_attempt % 3 == 0:
                        print(f"   ⏱️  Still checking... ({check_attempt + 1}s)")
                
                # Switch back to main content
                self.driver.switch_to.default_content()
                
                if auto_solved:
                    return True
                else:
                    print("   ✅ Challenge appeared - using 2Captcha...")
                    
            except Exception as click_error:
                print(f"   ⚠️  Could not click checkbox: {click_error}")
                print("   Continuing with direct token injection...")
                self.driver.switch_to.default_content()
            
            # Submit CAPTCHA to 2Captcha
            url = self.driver.current_url
            submit_url = f"http://2captcha.com/in.php?key={self.twocaptcha_api_key}&method=userrecaptcha&googlekey={sitekey}&pageurl={url}&json=1"
            
            print(f"   📤 Submitting to 2Captcha API...")
            response = requests.get(submit_url, timeout=10)
            result = response.json()
            
            if result['status'] != 1:
                error_msg = result.get('request', 'Unknown error')
                print(f"❌ 2Captcha submission failed: {error_msg}")
                print(f"   Full response: {result}")
                
                # Common errors with helpful messages
                if error_msg == 'ERROR_WRONG_USER_KEY':
                    print("   💡 Check your API key - it appears to be invalid")
                elif error_msg == 'ERROR_ZERO_BALANCE':
                    print("   💡 Your 2Captcha balance is $0 - add funds at https://2captcha.com")
                elif error_msg == 'ERROR_NO_SLOT_AVAILABLE':
                    print("   💡 2Captcha is busy - try again in a few minutes")
                
                return False
            
            captcha_id = result['request']
            print(f"⏳ Waiting for 2Captcha to solve (ID: {captcha_id})...")
            
            # Poll for result (usually takes 10-30 seconds)
            for attempt in range(60):
                time.sleep(2)
                result_url = f"http://2captcha.com/res.php?key={self.twocaptcha_api_key}&action=get&id={captcha_id}&json=1"
                
                try:
                    response = requests.get(result_url, timeout=10)
                    result = response.json()
                except requests.exceptions.Timeout:
                    print(f"   ⚠️  Request timeout, retrying...")
                    continue
                except Exception as poll_error:
                    print(f"   ⚠️  Polling error: {poll_error}")
                    continue
                
                # Print progress every 10 seconds
                if attempt > 0 and attempt % 5 == 0:
                    elapsed = attempt * 2
                    print(f"   ⏱️  Still waiting... ({elapsed}s elapsed)")
                
                # Check if solved
                if result['status'] == 1:
                    token = result['request']
                    print("✅ 2Captcha token received!")
                    
                    # Inject token into page
                    self.driver.execute_script(f"""
                        document.getElementById('g-recaptcha-response').innerHTML = '{token}';
                        document.getElementById('g-recaptcha-response').value = '{token}';
                        
                        // Try multiple callback methods
                        if (typeof ___grecaptcha_cfg !== 'undefined') {{
                            for (var id in ___grecaptcha_cfg.clients) {{
                                var client = ___grecaptcha_cfg.clients[id];
                                if (client && typeof client.callback === 'function') {{
                                    try {{
                                        client.callback('{token}');
                                    }} catch (e) {{ }}
                                }}
                            }}
                        }}
                        
                        // Alternative: trigger change event
                        var event = new Event('change');
                        document.getElementById('g-recaptcha-response').dispatchEvent(event);
                        
                        // Remove disabled attribute from button
                        var buttons = document.querySelectorAll('button[disabled]');
                        buttons.forEach(function(btn) {{
                            btn.removeAttribute('disabled');
                            btn.disabled = false;
                        }});
                    """)
                    
                    # Verify CAPTCHA was actually solved by checking checkbox state
                    # Poll for up to 10 seconds to see if checkbox gets checked
                    print("   🔍 Verifying checkbox state...")
                    checkbox_checked = False
                    
                    for verify_attempt in range(10):  # 10 attempts x 1 second = 10 seconds max
                        time.sleep(1)
                        
                        try:
                            # Switch to checkbox iframe to verify
                            checkbox_iframe = self.wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"][src*="anchor"]'))
                            )
                            self.driver.switch_to.frame(checkbox_iframe)
                            
                            # Look for the checkmark (aria-checked="true")
                            checkbox = self.driver.find_element(By.ID, 'recaptcha-anchor')
                            is_checked = checkbox.get_attribute('aria-checked')
                            
                            self.driver.switch_to.default_content()
                            
                            if is_checked == 'true':
                                print(f"   ✅ Checkbox verified as checked (after {verify_attempt + 1}s)")
                                checkbox_checked = True
                                break
                            else:
                                # Still not checked, keep polling
                                if verify_attempt % 3 == 0 and verify_attempt > 0:
                                    print(f"   ⏳ Still waiting for checkbox... ({verify_attempt + 1}s)")
                                
                        except Exception as verify_error:
                            # If we can't find iframe/checkbox, break out
                            print(f"   ⚠️  Verification error: {verify_error}")
                            self.driver.switch_to.default_content()
                            break
                    
                    if checkbox_checked:
                        print("✅ 2Captcha token accepted!")
                        return True
                    else:
                        print("❌ 2Captcha token not accepted (checkbox not checked after 10s)")
                        return False
                
                # Check for errors (status == 0)
                elif result['status'] == 0:
                    error_msg = result.get('request', 'Unknown error')
                    # CAPCHA_NOT_READY is normal, keep waiting
                    if error_msg == 'CAPCHA_NOT_READY':
                        continue
                    # Other errors are actual failures
                    else:
                        print(f"❌ 2Captcha error: {error_msg}")
                        print(f"   Full response: {result}")
                        return False
            
            # If we get here, we timed out
            print("❌ 2Captcha timeout after 120 seconds")
            print(f"   Last response: {result}")
            return False
            
        except Exception as e:
            print(f"❌ 2Captcha error: {str(e)}")
            return False
    
    def check_2captcha_balance(self):
        """
        Check 2Captcha account balance
        Returns: (success: bool, balance: float, message: str)
        """
        if not self.twocaptcha_api_key:
            return (False, 0.0, "No API key provided")
        
        try:
            url = f"http://2captcha.com/res.php?key={self.twocaptcha_api_key}&action=getbalance&json=1"
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if result['status'] == 1:
                balance = float(result['request'])
                return (True, balance, f"Balance: ${balance:.2f}")
            else:
                error = result.get('request', 'Unknown error')
                return (False, 0.0, f"Error: {error}")
        except Exception as e:
            return (False, 0.0, f"Exception: {str(e)}")
    
    def get_recaptcha_sitekey(self):
        """Extract reCAPTCHA site key from page"""
        # Hardcoded site key for Orange Tunisia (tested and confirmed)
        ORANGE_SITEKEY = "6Leg2IkcAAAAAMh5olydKqPSz0lI7ysYRrIo_9ea"
        
        # Try to extract dynamically as backup
        try:
            iframe = self.driver.find_element(By.CSS_SELECTOR, 'iframe[src*="recaptcha"]')
            src = iframe.get_attribute('src')
            match = re.search(r'k=([^&]+)', src)
            if match:
                extracted_key = match.group(1)
                # Verify it matches our known key
                if extracted_key == ORANGE_SITEKEY:
                    return extracted_key
                else:
                    print(f"⚠️  Site key changed! Old: {ORANGE_SITEKEY}, New: {extracted_key}")
                    return extracted_key
        except:
            pass
        
        # Fallback to known key
        return ORANGE_SITEKEY
    
    def recharge(self, phone_number, amount, notification_number=None, captcha_method='auto'):
        """
        Perform credit card recharge
        
        Args:
            phone_number (str): Orange phone number (e.g., "53028939")
            amount (int): Recharge amount (10, 20, 25, 30, 40, 50, 100, 200, or custom)
            notification_number (str): Optional phone to notify after recharge
            captcha_method (str): 'audio' (free), '2captcha' (paid), or 'auto' (try audio first, fallback to 2captcha)
        
        Returns:
            dict: Result with payment URL
        """
        try:
            self._setup_driver()
            
            print("🚀 Starting Orange credit card recharge...")
            self.driver.get("https://www.orange.tn/recharge-en-ligne")
            time.sleep(3)
            
            # Select "Recharge par carte bancaire" if needed
            # (page loads with this option by default based on screenshot)
            
            # Fill phone number
            print(f"📞 Entering phone number: {phone_number}")
            phone_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="55 555 555"]'))
            )
            phone_input.clear()
            phone_input.send_keys(phone_number)
            
            # Fill confirmation phone number
            print("📞 Confirming phone number...")
            phone_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[placeholder*="55 555 555"]')
            if len(phone_inputs) >= 2:
                phone_inputs[1].clear()
                phone_inputs[1].send_keys(phone_number)
            
            # Select amount (use JavaScript to avoid click interception)
            print(f"💰 Selecting amount: {amount} DT")
            if amount in [10, 20, 25, 30, 40, 50, 100, 200]:
                # Click predefined amount button
                buttons = self.driver.find_elements(By.TAG_NAME, 'button')
                # Find the button with the amount text
                for btn in buttons:
                    if str(amount) == btn.text.strip():
                        self.driver.execute_script("arguments[0].click();", btn)
                        break
            else:
                # Enter custom amount
                custom_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
                custom_input.clear()
                custom_input.send_keys(str(amount))
            
            # Fill notification number if provided
            if notification_number:
                print(f"📱 Setting notification number: {notification_number}")
                notif_input = self.driver.find_elements(By.CSS_SELECTOR, 'input[placeholder*="55 555 555"]')
                if len(notif_input) >= 3:
                    notif_input[2].clear()
                    notif_input[2].send_keys(notification_number)
            
            # Click Valider (use JavaScript to avoid click interception)
            print("✅ Clicking Valider...")
            valider_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Valider")]')
            self.driver.execute_script("arguments[0].click();", valider_button)
            time.sleep(3)  # Wait for reCAPTCHA to load
            
            # Wait for reCAPTCHA iframe to be visible
            print("⏳ Waiting for reCAPTCHA to load...")
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"]'))
                )
                print("✅ reCAPTCHA loaded!")
            except:
                print("⚠️  reCAPTCHA iframe not found, continuing anyway...")
            
            # Solve reCAPTCHA
            print("🔓 Solving reCAPTCHA...")
            captcha_solved = False
            
            if captcha_method in ['audio', 'auto']:
                captcha_solved = self.solve_recaptcha_audio()
            
            if not captcha_solved and captcha_method in ['2captcha', 'auto']:
                sitekey = self.get_recaptcha_sitekey()
                if sitekey:
                    captcha_solved = self.solve_recaptcha_2captcha(sitekey)
            
            if not captcha_solved:
                return {
                    'status': 'error',
                    'message': 'Failed to solve CAPTCHA'
                }
            
            # Set up network interception BEFORE clicking Payer
            print("🔍 Setting up GraphQL response interceptor...")
            self.driver.execute_script("""
                window.capturedPaymentUrl = null;
                
                // Intercept fetch
                const originalFetch = window.fetch;
                window.fetch = function(...args) {
                    return originalFetch(...args).then(response => {
                        const clonedResponse = response.clone();
                        
                        if (args[0].includes('graphql') || args[0].includes('topup')) {
                            clonedResponse.json().then(data => {
                                if (data.data && data.data.topupWithCreditCard) {
                                    window.capturedPaymentUrl = data.data.topupWithCreditCard;
                                    console.log('✅ Payment URL captured:', window.capturedPaymentUrl);
                                }
                            }).catch(() => {});
                        }
                        
                        return response;
                    });
                };
                
                // Intercept XHR
                const originalOpen = XMLHttpRequest.prototype.open;
                const originalSend = XMLHttpRequest.prototype.send;
                
                XMLHttpRequest.prototype.open = function(method, url) {
                    this._url = url;
                    return originalOpen.apply(this, arguments);
                };
                
                XMLHttpRequest.prototype.send = function() {
                    this.addEventListener('load', function() {
                        if ((this._url.includes('graphql') || this._url.includes('topup')) && this.status === 200) {
                            try {
                                const data = JSON.parse(this.responseText);
                                if (data.data && data.data.topupWithCreditCard) {
                                    window.capturedPaymentUrl = data.data.topupWithCreditCard;
                                    console.log('✅ Payment URL captured:', window.capturedPaymentUrl);
                                }
                            } catch (e) {}
                        }
                    });
                    return originalSend.apply(this, arguments);
                };
            """)
            
            # Wait for Pay button to become enabled
            print("⏳ Waiting for Pay button...")
            time.sleep(3)  # Give page time to process token
            
            # Force enable the button
            self.driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                buttons.forEach(function(btn) {
                    if (btn.textContent.includes('Payer')) {
                        btn.removeAttribute('disabled');
                        btn.disabled = false;
                    }
                });
            """)
            
            pay_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Payer")]'))
            )
            
            # Click Pay (use JavaScript to avoid click interception)
            print("💳 Clicking Payer...")
            self.driver.execute_script("arguments[0].click();", pay_button)
            
            # Wait for GraphQL response and check intercepted URL
            print("⏳ Waiting for GraphQL response...")
            payment_url = None
            
            # Poll for captured payment URL (from our JavaScript interceptor)
            for i in range(20):  # 10 seconds total (20 x 0.5s)
                time.sleep(0.5)
                captured_url = self.driver.execute_script("return window.capturedPaymentUrl;")
                
                if captured_url:
                    payment_url = captured_url
                    print(f"✅ Payment URL captured from interceptor!")
                    break
            
            # If interceptor didn't catch it, check if redirected
            if not payment_url:
                time.sleep(2)
                current_url = self.driver.current_url
                if 'clictopay' in current_url or 'payment' in current_url:
                    print("✅ Payment URL obtained from redirect!")
                    payment_url = current_url
            
            # If we got the payment URL, return success
            if payment_url:
                return {
                    'status': 'success',
                    'payment_url': payment_url,
                    'phone': phone_number,
                    'amount': amount
                }
            
            # Fallback: try to find URL in page source
            page_source = self.driver.page_source
            if 'clictopay' in page_source:
                import re
                match = re.search(r'https://ipay\.clictopay\.com[^"\'<>\s]*', page_source)
                if match:
                    payment_url = match.group(0)
                    print(f"✅ Payment URL found in page source!")
                    return {
                        'status': 'success',
                        'payment_url': payment_url,
                        'phone': phone_number,
                        'amount': amount
                    }
            
            print("⚠️  Payment initiated but URL not captured automatically")
            current_url = self.driver.current_url
            return {
                'status': 'partial_success',
                'message': 'Reached payment step - check browser for payment URL',
                'current_url': current_url
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
        
        finally:
            if self.driver:
                time.sleep(5)  # Keep browser open to see result
                # self.driver.quit()  # Uncomment in production


def main():
    """CLI entry point"""
    import sys
    
    # Check for special commands
    if len(sys.argv) >= 2 and sys.argv[1] == 'check-balance':
        # Extract 2captcha key from args
        twocaptcha_key = None
        for arg in sys.argv:
            if arg.startswith('--2captcha-key='):
                twocaptcha_key = arg.split('=')[1]
        
        if not twocaptcha_key:
            print("Usage: python orange_creditcard.py check-balance --2captcha-key=YOUR_KEY")
            sys.exit(1)
        
        recharger = OrangeCreditCardRecharge(twocaptcha_api_key=twocaptcha_key)
        success, balance, message = recharger.check_2captcha_balance()
        
        print("\n" + "="*60)
        print("2CAPTCHA ACCOUNT STATUS")
        print("="*60)
        if success:
            print(f"✅ API Key Valid")
            print(f"💵 Balance: ${balance:.2f}")
            if balance < 0.50:
                print(f"⚠️  Low balance! Add funds at https://2captcha.com")
        else:
            print(f"❌ {message}")
        print("="*60)
        sys.exit(0)
    
    if len(sys.argv) < 3:
        print("Usage: python orange_creditcard.py <phone_number> <amount> [notification_number] [--2captcha-key=XXX]")
        print("       python orange_creditcard.py check-balance --2captcha-key=XXX")
        print()
        print("Examples:")
        print("  python orange_creditcard.py 53028939 20")
        print("  python orange_creditcard.py 53028939 50 27865121 --2captcha-key=your_api_key")
        print("  python orange_creditcard.py check-balance --2captcha-key=your_api_key")
        sys.exit(1)
    
    phone_number = sys.argv[1]
    amount = int(sys.argv[2])
    notification_number = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else None
    
    # Extract 2captcha key from args
    twocaptcha_key = None
    for arg in sys.argv:
        if arg.startswith('--2captcha-key='):
            twocaptcha_key = arg.split('=')[1]
    
    recharger = OrangeCreditCardRecharge(twocaptcha_api_key=twocaptcha_key)
    result = recharger.recharge(
        phone_number=phone_number,
        amount=amount,
        notification_number=notification_number,
        captcha_method='auto'  # Try free audio first, fallback to 2captcha
    )
    
    print("\n" + "="*60)
    print("RECHARGE RESULT")
    print("="*60)
    print(f"Status:  {result['status']}")
    if result.get('payment_url'):
        print(f"Payment URL: {result['payment_url']}")
    if result.get('message'):
        print(f"Message: {result['message']}")
    print("="*60)


if __name__ == '__main__':
    main()
