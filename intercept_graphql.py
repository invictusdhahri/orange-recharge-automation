#!/usr/bin/env python3
"""
Alternative approach: Intercept GraphQL request directly
Uses Chrome DevTools Protocol for reliable network interception
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def intercept_graphql_response(driver, timeout=10):
    """
    Wait for and capture the GraphQL response containing payment URL
    """
    print("🔍 Intercepting GraphQL response...")
    
    # JavaScript to capture fetch/XHR responses
    driver.execute_script("""
        window.capturedPaymentUrl = null;
        
        // Intercept fetch
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            return originalFetch(...args).then(response => {
                // Clone to read body without consuming it
                const clonedResponse = response.clone();
                
                // Check if this is our GraphQL response
                if (args[0].includes('graphql') || args[0].includes('topup')) {
                    clonedResponse.json().then(data => {
                        if (data.data && data.data.topupWithCreditCard) {
                            window.capturedPaymentUrl = data.data.topupWithCreditCard;
                            console.log('Payment URL captured:', window.capturedPaymentUrl);
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
                            console.log('Payment URL captured:', window.capturedPaymentUrl);
                        }
                    } catch (e) {}
                }
            });
            return originalSend.apply(this, arguments);
        };
    """)
    
    # Poll for captured URL
    start_time = time.time()
    while time.time() - start_time < timeout:
        payment_url = driver.execute_script("return window.capturedPaymentUrl;")
        if payment_url:
            print(f"✅ Payment URL captured: {payment_url}")
            return payment_url
        time.sleep(0.5)
    
    print("⏳ Timeout waiting for payment URL")
    return None


# Example usage
if __name__ == "__main__":
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    # Your automation code here...
    # After clicking Payer:
    payment_url = intercept_graphql_response(driver, timeout=10)
    
    if payment_url:
        print(f"Success! Payment URL: {payment_url}")
    else:
        print("Failed to capture payment URL")
    
    driver.quit()
