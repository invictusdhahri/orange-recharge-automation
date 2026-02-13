#!/usr/bin/env node
/**
 * Orange Tunisia Credit Card Recharge with 2Captcha
 * Node.js + Puppeteer implementation
 */

const puppeteer = require('puppeteer');
const https = require('https');

const TWOCAPTCHA_API_KEY = '9d1be5cb29642744ec425ab74d909bb5';
const SITE_KEY = '6Leg2IkcAAAAAMh5olydKqPSz0lI7ysYRrIo_9ea';
const PAGE_URL = 'https://www.orange.tn/recharge-en-ligne';

// 2Captcha API helper
function solve2Captcha(sitekey, pageurl) {
    return new Promise((resolve, reject) => {
        // Submit CAPTCHA
        const submitUrl = `http://2captcha.com/in.php?key=${TWOCAPTCHA_API_KEY}&method=userrecaptcha&googlekey=${sitekey}&pageurl=${pageurl}&json=1`;
        
        https.get(submitUrl, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                const result = JSON.parse(data);
                if (result.status !== 1) {
                    reject(new Error('2Captcha submission failed: ' + JSON.stringify(result)));
                    return;
                }
                
                const captchaId = result.request;
                console.log(`✅ CAPTCHA submitted, ID: ${captchaId}`);
                console.log('⏳ Waiting for solution...');
                
                // Poll for result
                let attempts = 0;
                const poll = setInterval(() => {
                    attempts++;
                    const resultUrl = `http://2captcha.com/res.php?key=${TWOCAPTCHA_API_KEY}&action=get&id=${captchaId}&json=1`;
                    
                    https.get(resultUrl, (res) => {
                        let data = '';
                        res.on('data', chunk => data += chunk);
                        res.on('end', () => {
                            const result = JSON.parse(data);
                            
                            if (result.status === 1) {
                                clearInterval(poll);
                                console.log('✅ CAPTCHA solved!');
                                resolve(result.request);
                            } else if (attempts > 30) {
                                clearInterval(poll);
                                reject(new Error('Timeout waiting for CAPTCHA'));
                            } else {
                                console.log(`⏳ Attempt ${attempts}/30...`);
                            }
                        });
                    });
                }, 3000);
            });
        });
    });
}

async function main() {
    console.log('🚀 Starting Orange credit card recharge automation\n');
    
    const browser = await puppeteer.launch({
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // Navigate to page
    console.log('📱 Opening Orange recharge page...');
    await page.goto(PAGE_URL, { waitUntil: 'networkidle2' });
    await page.waitForTimeout(2000);
    
    // Fill phone number (first input)
    console.log('📞 Entering phone number...');
    await page.type('input[placeholder*="55 555 555"]', '53028939');
    
    // Fill confirmation (second input)
    const phoneInputs = await page.$$('input[placeholder*="55 555 555"]');
    if (phoneInputs.length >= 2) {
        await phoneInputs[1].type('53028939');
    }
    
    // Click 20 DT
    console.log('💰 Selecting 20 DT...');
    await page.click('button::-p-text(20)');
    await page.waitForTimeout(1000);
    
    // Click Valider
    console.log('✅ Clicking Valider...');
    await page.click('button::-p-text(Valider)');
    await page.waitForTimeout(2000);
    
    // Solve reCAPTCHA
    console.log('🔓 Solving reCAPTCHA with 2Captcha...');
    const token = await solve2Captcha(SITE_KEY, PAGE_URL);
    
    // Inject token
    console.log('💉 Injecting reCAPTCHA token...');
    await page.evaluate((token) => {
        document.getElementById('g-recaptcha-response').innerHTML = token;
        document.getElementById('g-recaptcha-response').value = token;
        
        // Trigger callback
        if (typeof ___grecaptcha_cfg !== 'undefined') {
            const clients = ___grecaptcha_cfg.clients;
            for (let id in clients) {
                if (clients[id] && clients[id].callback) {
                    clients[id].callback(token);
                }
            }
        }
    }, token);
    
    await page.waitForTimeout(2000);
    
    // Click Payer
    console.log('💳 Clicking Payer...');
    await page.click('button::-p-text(Payer)');
    
    // Wait for response
    console.log('⏳ Waiting for GraphQL response...');
    await page.waitForTimeout(5000);
    
    // Check if redirected
    const currentUrl = page.url();
    console.log(`\n📍 Current URL: ${currentUrl}`);
    
    if (currentUrl.includes('clictopay') || currentUrl.includes('payment')) {
        console.log('✅ SUCCESS! Redirected to payment page');
        console.log(`🔗 Payment URL: ${currentUrl}`);
    } else {
        console.log('⚠️  Not redirected yet, checking page content...');
        const content = await page.content();
        
        // Look for GraphQL response in page
        if (content.includes('clictopay') || content.includes('topupWithCreditCard')) {
            console.log('✅ Found payment URL in page content!');
            // Extract URL
            const match = content.match(/https:\/\/ipay\.clictopay\.com[^"']*/);
            if (match) {
                console.log(`🔗 Payment URL: ${match[0]}`);
            }
        } else {
            console.log('❌ No payment URL found');
        }
    }
    
    // Keep browser open for inspection
    console.log('\n🔍 Browser will stay open for 30 seconds for inspection...');
    await page.waitForTimeout(30000);
    
    await browser.close();
}

main().catch(console.error);
