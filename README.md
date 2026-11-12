# Android SMS Bugbounty

> A lightweight, menu-driven **SMS & voice call toolkit** for security engineers, built on the **Twilio REST API** using **Python standard library only** (no `pip install` needed).

**Coded by Mr Sabaz Ali Khan - Cyber Security Engineer**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-lightgrey)
![Use](https://img.shields.io/badge/use-authorized%20only-red)

---

## Overview

`sms_call_tools.py` is a single-file command-line tool for sending SMS, placing text-to-speech voice calls, and reviewing delivery logs through a Twilio account. It is useful for security professionals who need to test SMS/voice delivery flows (for example 2FA/OTP delivery, notification pipelines, alerting, and awareness exercises) **on systems and numbers they are authorized to test**.

Because it uses only the Python standard library, it runs anywhere Python 3 runs, including **Android via Termux**.

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Send SMS | Send a single text message to an E.164 number |
| 2 | Make Call | Voice call with a spoken (text-to-speech) message or your own TwiML URL |
| 3 | Bulk SMS | Send from a CSV file, opt-in recipients only, with confirmation and rate limiting |
| 4 | View Logs | Recent SMS and call history from your Twilio account |
| 5 | Check Status | Look up a message or call by its SID |
| 6 | Account Balance | Show your Twilio balance and currency |

Additional behavior:

- E.164 number validation (e.g. `+923001234567`)
- Local activity log in `sms_call_log.jsonl` (one JSON record per event)
- Credentials read from environment variables, never hard-coded
- Colored terminal output with a banner

## Requirements

- Python 3.8 or newer
- A [Twilio](https://www.twilio.com/) account
- A Twilio phone number (or verified caller ID) that **you own**
- Internet access

No third-party Python packages are required.

## Installation

```bash
git clone https://github.com/<your-username>/Android-SMS-Bugbounty.git
cd Android-SMS-Bugbounty
```

### Termux (Android)

```bash
pkg update && pkg install python git -y
git clone https://github.com/whoami592/Android-SMS-Bugbounty.git
cd Android-SMS-Bugbounty
```

## Configuration

Set your credentials as environment variables:

**Linux / macOS / Termux**

```bash
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=your_auth_token
export TWILIO_FROM=+1XXXXXXXXXX
```

**Windows (PowerShell)**

```powershell
$env:TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:TWILIO_AUTH_TOKEN="your_auth_token"
$env:TWILIO_FROM="+1XXXXXXXXXX"
```

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_FROM` | Your Twilio number in E.164 format |

> Never commit your Account SID or Auth Token to GitHub. Add any `.env` files to `.gitignore`.

## Usage

```bash
python3 sms_call_tools.py
```

You will see a menu:

```
  [1] Send SMS
  [2] Make Call
  [3] Bulk SMS (opt-in CSV)
  [4] View SMS / Call logs
  [5] Check status by SID
  [6] Account balance
  [0] Exit
```

### Send an SMS

Choose `1`, enter the destination number in E.164 format and your message.

### Make a call

Choose `2`, then either type a message to be spoken, or provide a TwiML URL.

### Bulk SMS from CSV

Create a CSV file with two columns, `number` and `message`:

```csv
number,message
+923001234567,Your appointment is confirmed.
+923007654321,Your verification code is 123456.
```

Choose `3`, enter the file path, confirm that **every recipient has opted in**, and set a delay (minimum 1 second) between messages.

### Check status / logs

- `4` shows recent SMS and call history.
- `5` shows the status of a specific message (`SM...` / `MM...`) or call (`CA...`) SID.

## Log File

Every send, call, and bulk result is appended to `sms_call_log.jsonl`:

```json
{"time": "2026-11-11T10:00:00Z", "type": "sms", "to": "+923001234567", "sid": "SMxxxxxxxx", "status": "queued"}
```

## Legal & Ethical Use

This tool is intended for **authorized security testing and legitimate messaging only**.

- Only message people who have **consented** to receive it.
- Only send from numbers **you own or have verified** in Twilio.
- No caller-ID spoofing, harassment, spam, or flooding.
- Follow Twilio's Acceptable Use Policy and the telecom/anti-spam laws of your country and the recipient's country.
- For bug bounty work, stay strictly inside the program's scope and rules.

The author is not responsible for misuse of this software.

## Project Structure

```
Android-SMS-Bugbounty/
├── sms_call_tools.py    # main tool
├── sms_call_log.jsonl   # auto-generated activity log
└── README.md
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN first` | Export the environment variables in the same terminal session |
| `Set TWILIO_FROM ...` | Use your Twilio number in E.164 format, e.g. `+1XXXXXXXXXX` |
| Twilio error code `21608` | Trial accounts can only message verified numbers |
| `Network error` | Check your internet connection / DNS |

## Author

**Mr Sabaz Ali Khan** - Cyber Security Engineer

## License

Released under the MIT License. Add a `LICENSE` file to your repository to apply it.
