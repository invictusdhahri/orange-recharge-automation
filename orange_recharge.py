#!/usr/bin/env python3
"""
Orange Tunisia Recharge Automation
Simple, production-ready script with math CAPTCHA solving
"""

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def solve_math_captcha(equation_text):
    """
    Solve simple math equations from CAPTCHA
    Examples: "10 + 7", "5 * 3", "20 - 8", "15 / 3"
    
    Args:
        equation_text (str): Math equation like "10 + 7"
    
    Returns:
        int: Solution to the equation
    """
    # Remove any extra whitespace and special characters except math operators
    clean = equation_text.strip()
    
    # Extract numbers and operator
    match = re.match(r'(\d+)\s*([+\-*/])\s*(\d+)', clean)
    if not match:
        raise ValueError(f"Cannot parse equation: {equation_text}")
    
    num1, operator, num2 = match.groups()
    num1, num2 = int(num1), int(num2)
    
    # Calculate based on operator
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 // num2  # Integer division
    
    raise ValueError(f"Unknown operator: {operator}")


def recharge_orange(phone_number, recharge_code, headless=False):
    """
    Perform Orange Tunisia recharge with math CAPTCHA solving
    
    Args:
        phone_number (str): Orange phone number (e.g., "53028939")
        recharge_code (str): 13-14 digit recharge code
        headless (bool): Run browser in headless mode
    
    Returns:
        dict: Result with status and message
            - status: 'success', 'invalid_code', or 'error'
            - message: Human-readable result
            - response: Raw GraphQL response (if available)
    """
    
    # Setup Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    
    try:
        print("🚀 Starting Orange recharge automation...")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 15)
        
        # Navigate to recharge page
        print("📱 Opening Orange recharge page...")
        driver.get("https://www.orange.tn/recharge-par-carte-de-recharge")
        time.sleep(3)
        
        # Fill phone number (first field)
        print(f"📞 Entering phone number: {phone_number}")
        phone_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][inputmode="numeric"]'))
        )
        phone_input.clear()
        phone_input.send_keys(phone_number)
        
        # Fill confirmation phone number (second field)
        print("📞 Confirming phone number...")
        phone_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"][inputmode="numeric"]')
        if len(phone_inputs) >= 2:
            phone_inputs[1].clear()
            phone_inputs[1].send_keys(phone_number)
        
        # Fill recharge code
        print(f"🎫 Entering recharge code: {recharge_code}")
        code_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Code"]')
        code_input.clear()
        code_input.send_keys(recharge_code)
        
        # Read and solve math CAPTCHA
        print("🧮 Reading math CAPTCHA...")
        captcha_label = driver.find_element(By.XPATH, '//label[contains(text(), "+") or contains(text(), "-") or contains(text(), "*") or contains(text, "/")]')
        captcha_text = captcha_label.text.strip()
        print(f"🧮 CAPTCHA equation: {captcha_text}")
        
        # Solve the equation
        answer = solve_math_captcha(captcha_text)
        print(f"✅ CAPTCHA solution: {answer}")
        
        # Fill CAPTCHA answer
        captcha_input = driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
        captcha_input.clear()
        captcha_input.send_keys(str(answer))
        
        # Enable network monitoring to capture GraphQL response
        driver.execute_cdp_cmd('Network.enable', {})
        
        # Submit form
        print("📤 Submitting recharge...")
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Wait for response
        time.sleep(3)
        
        # Check for success message
        try:
            success_element = driver.find_element(By.XPATH, '//*[contains(text(), "Opération effectuée avec succès")]')
            print("✅ Recharge successful!")
            return {
                'status': 'success',
                'message': 'Opération effectuée avec succès',
                'phone': phone_number,
                'code': recharge_code
            }
        except:
            pass
        
        # Check for error message
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, '.error, .alert-danger, [class*="error"]')
            error_text = error_element.text
            print(f"❌ Error: {error_text}")
            return {
                'status': 'invalid_code',
                'message': error_text
            }
        except:
            pass
        
        # If no clear success or error, check page source
        page_source = driver.page_source.lower()
        if 'succès' in page_source or 'success' in page_source:
            return {
                'status': 'success',
                'message': 'Recharge appears successful (detected in page source)'
            }
        elif 'erreur' in page_source or 'error' in page_source or 'invalide' in page_source:
            return {
                'status': 'invalid_code',
                'message': 'Recharge code appears invalid (detected in page source)'
            }
        
        return {
            'status': 'error',
            'message': 'Unknown response - manual verification needed'
        }
        
    except Exception as e:
        print(f"❌ Error during automation: {str(e)}")
        return {
            'status': 'error',
            'message': f'Automation error: {str(e)}'
        }
    
    finally:
        if driver:
            time.sleep(2)  # Brief pause to see result
            driver.quit()


def main():
    """Main entry point for CLI usage"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python orange_recharge.py <phone_number> <recharge_code> [--headless]")
        print("Example: python orange_recharge.py 53028939 1234567890123")
        sys.exit(1)
    
    phone_number = sys.argv[1]
    recharge_code = sys.argv[2]
    headless = '--headless' in sys.argv
    
    result = recharge_orange(phone_number, recharge_code, headless=headless)
    
    print("\n" + "="*50)
    print("RECHARGE RESULT")
    print("="*50)
    print(f"Status:  {result['status']}")
    print(f"Message: {result['message']}")
    if result.get('phone'):
        print(f"Phone:   {result['phone']}")
    print("="*50)
    
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
