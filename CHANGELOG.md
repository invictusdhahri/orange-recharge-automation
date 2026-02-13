# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-02-13

### Fixed
- **CAPTCHA verification logic**: Both audio and 2Captcha methods now properly verify the checkbox state after solving
  - Audio method: Checks `aria-checked="true"` on reCAPTCHA checkbox after submitting audio answer
  - 2Captcha method: Verifies checkbox state after token injection
  - Eliminates false positives where script reported success but checkbox wasn't actually checked
  - Eliminates false negatives where script reported failure but checkbox was checked
  - Improves auto mode reliability by correctly detecting which method succeeded

### Details
Previously, the script would:
- Return `True` from audio method without checking if the answer was correct
- Return `True` from 2Captcha method without verifying the token was accepted
- Sometimes report "failed" when CAPTCHA was actually solved
- Sometimes report "success" when CAPTCHA wasn't solved

Now, both methods:
1. Submit the CAPTCHA solution (audio answer or token)
2. Wait for processing
3. Switch to checkbox iframe
4. Check `aria-checked` attribute on `#recaptcha-anchor`
5. Return `True` only if `aria-checked="true"`
6. Return `False` if checkbox not checked or verification fails

This ensures accurate reporting and proper fallback behavior in auto mode.

## [1.0.0] - 2026-02-13

### Added
- Initial release of Orange Tunisia recharge automation
- Scratch card recharge with math CAPTCHA solver
- Credit card recharge with reCAPTCHA bypass
- FREE audio challenge method (60-80% success)
- 2Captcha service integration (95-99% success)
- Auto mode (free + paid fallback, best of both worlds)
- Comprehensive documentation (10 files, 40KB+)
- Test infrastructure and deployment guides
- Server environment support (OpenClaw/VPS)
- JavaScript click workarounds for element interception errors
