# Orange Tunisia Recharge - Response Formats

Complete documentation of all possible responses from the Orange recharge system.

## ✅ Success Response

### What You See

**Browser Display:**
- ✅ Green background
- ✅ Checkmark icon
- ✅ Text: **"Opération effectuée avec succès"**
- ✅ Phone number displayed: `53 028 939`

**Python Response:**
```json
{
  "status": "success",
  "message": "Opération effectuée avec succès",
  "phone": "53028939",
  "code": "1234567890123"
}
```

### Backend (GraphQL)

**Endpoint:** `POST https://www.orange.tn/graphql`

**Response:**
```json
{
  "data": {
    "topupWithScratchCard": true
  }
}
```

**Status Code:** `200 OK`

---

## ❌ Error Responses

### 1. Invalid Recharge Code

**What You See:**
- Red error message
- Text about invalid code

**Python Response:**
```json
{
  "status": "invalid_code",
  "message": "Code de recharge invalide"
}
```

**Backend (GraphQL):**
```json
{
  "errors": [
    {
      "message": "errors.topupWithScratch.invalidScratch",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": [
        "topupWithScratchCard"
      ],
      "extensions": {
        "code": "BAD_USER_INPUT",
        "exception": {
          "stacktrace": [
            "UserInputError: errors.topupWithScratch.invalidScratch",
            "    at /opt/app/dist/index.js:1:916637",
            "    ..."
          ]
        }
      }
    }
  ],
  "data": null
}
```

**Status Code:** `200 OK` (GraphQL always returns 200, errors in body)

### 2. Wrong CAPTCHA Answer

**What You See:**
- Error message about incorrect CAPTCHA

**Python Response:**
```json
{
  "status": "error",
  "message": "CAPTCHA incorrect"
}
```

### 3. Invalid Phone Number

**What You See:**
- Form validation error
- Red border on phone input

**Python Response:**
```json
{
  "status": "error",
  "message": "Numéro de téléphone invalide"
}
```

### 4. Network/Connection Error

**Python Response:**
```json
{
  "status": "error",
  "message": "Automation error: <error details>"
}
```

---

## 🔍 Detection Logic

### Success Detection (Priority Order)

1. **Look for success message:**
   ```python
   success_element = driver.find_element(
       By.XPATH, 
       '//*[contains(text(), "Opération effectuée avec succès")]'
   )
   ```

2. **Check page source:**
   ```python
   page_source = driver.page_source.lower()
   if 'succès' in page_source or 'success' in page_source:
       return {'status': 'success', ...}
   ```

3. **Parse GraphQL response (if captured):**
   ```python
   if response.get('data', {}).get('topupWithScratchCard'):
       return {'status': 'success', ...}
   ```

### Error Detection (Priority Order)

1. **Look for error elements:**
   ```python
   error_element = driver.find_element(
       By.CSS_SELECTOR, 
       '.error, .alert-danger, [class*="error"]'
   )
   ```

2. **Check GraphQL errors:**
   ```python
   if response.get('errors'):
       error_msg = response['errors'][0]['message']
       if 'invalidScratch' in error_msg:
           return {'status': 'invalid_code', ...}
   ```

3. **Check page source:**
   ```python
   if 'erreur' in page_source or 'invalide' in page_source:
       return {'status': 'invalid_code', ...}
   ```

---

## 📊 Response Comparison

| Response | Status Code | Data | Errors | UI Message |
|----------|-------------|------|--------|------------|
| **Success** | 200 | `{"topupWithScratchCard": true}` | `null` | Green "Opération effectuée avec succès" |
| **Invalid Code** | 200 | `null` | `[{"message": "errors.topupWithScratch.invalidScratch", ...}]` | Red error text |
| **Wrong CAPTCHA** | 200 | varies | varies | Red "CAPTCHA incorrect" |
| **Network Error** | varies | N/A | N/A | Python exception |

---

## 🧪 Testing

### Test Invalid Code

```bash
python orange_recharge.py 53028939 0000000000000
```

**Expected Output:**
```
❌ Error: Code de recharge invalide
Status:  invalid_code
Message: Code de recharge invalide
```

### Test Valid Code

```bash
python orange_recharge.py 53028939 <valid-13-14-digit-code>
```

**Expected Output:**
```
✅ Recharge successful!
Status:  success
Message: Opération effectuée avec succès
Phone:   53028939
```

---

## 🔧 Response Parsing Code

```python
def parse_response(driver, timeout=5):
    """
    Parse Orange recharge response from page
    
    Returns:
        dict: Structured response
    """
    time.sleep(timeout)
    
    # Check for success
    try:
        success_el = driver.find_element(
            By.XPATH, 
            '//*[contains(text(), "Opération effectuée avec succès")]'
        )
        return {
            'status': 'success',
            'message': 'Opération effectuée avec succès'
        }
    except:
        pass
    
    # Check for error
    try:
        error_el = driver.find_element(
            By.CSS_SELECTOR, 
            '.error, .alert-danger'
        )
        return {
            'status': 'invalid_code',
            'message': error_el.text
        }
    except:
        pass
    
    # Fallback: check page source
    source = driver.page_source.lower()
    if 'succès' in source:
        return {'status': 'success', 'message': 'Success detected'}
    elif 'erreur' in source or 'invalide' in source:
        return {'status': 'invalid_code', 'message': 'Error detected'}
    
    return {
        'status': 'error',
        'message': 'Unknown response'
    }
```

---

## 📝 Notes

1. **GraphQL always returns 200** - Even for errors, check the body
2. **UI detection is reliable** - Green background + success text = success
3. **Multiple detection methods** - Script tries 3 different ways to detect success/error
4. **Clear error messages** - GraphQL errors are well-structured
5. **No ambiguity** - Either success or clear error reason

---

**Last Updated:** February 13, 2026  
**Tested With:** Orange Tunisia recharge system (2026)
