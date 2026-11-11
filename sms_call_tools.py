#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMS & Call Tools  (Twilio REST API, Python stdlib only)
Coded by Mr Sabaz Ali Khan - Cyber Security Engineer

Features
  1. Send SMS
  2. Make voice call (text-to-speech message or TwiML URL)
  3. Bulk SMS from CSV (opt-in recipients only, rate limited)
  4. View recent SMS / call logs
  5. Check status of a message or call
  6. Account balance / info

Setup (environment variables, never hard-code credentials):
  export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  export TWILIO_AUTH_TOKEN=your_auth_token
  export TWILIO_FROM=+1XXXXXXXXXX      # a number YOU own/verified in Twilio

Legal use only: send to people who consented, from numbers you own.
No caller-ID spoofing, no flooding. A log is kept in sms_call_log.jsonl.
"""

import base64
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from xml.sax.saxutils import escape

BANNER = r"""
⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣷⣷⣶⣶⣷⣷⣷⣶⣶⣶⣶⣶⣶⣶⣶⣦⣄⠻⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⠻⣿⣿⡿⣿⡿⠿⠛⣻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⠶⠖⠛⣋⣉⣉⣭⣤⣤⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠋⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⣛⣉⣭⣥⣴⣶⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠁⢲⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠔⠒⠈⣉⡉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣉⣉⣩⣥⣤⣤⠆⣰⣿⣿⣿⣿⣿⣿⣿⣿⣋⣤⣤⣶⢾⣿⣿⣦⣄⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⢈⣈⡀⠙⠛⠷⢦⡀⠀⡹⠋⠛⢻⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠟⠛⢿⠇⢻⣿⣿⣿⣿⣿⣿⣿⡿⠛⠀⠀⠠⠖⠛⠋⠛⠳⠀⠀⠀⠙⠆⠀⡾⠀⠀⠻⠿⢿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡟⠀⣴⣄⡀⢾⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⣀⣤⡙⠂⠀⠀⡄⠀⠀⠀⠀⣴⣾⣧⠀⠀⠀⠀⠀⠀⠃⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡇⠀⣾⣿⣿⣦⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣀⠀⠐⠃⠀⢀⣠⣼⣿⣿⣿⠀⠀⠀⠀⠀⢤⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡇⠘⠋⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠅⣠⣼⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⡾⠿⠿⠿⠿⠿⠟⠿⠿⡿⡿⡿
⣿⣿⡀⣀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣦⣤⣤⣦⡄⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣧⣼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⡀⠀⠹⣿⠇⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⢃⣾⡿⠿⢿⣿⣿⣿⠙⠻⣿⠟⢻⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠓⡄⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⠏⠀⢀⣀⣙⡛⠋⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣭⠀⠀⠀⢀⣠⣆⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢩⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⠁⠀⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠹⠿⠿⠛⠋⠉⠉⠁⠀⠈⠙⠋⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⠀⠀⢤⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡁⢠⣤⣤⣄⣤⣤⣤⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣬⡾⠓⠀⣸⣿⣿⣿⣿⣿⡟⢿⣿⣿⣿⣿⣿⡏⢀⠄⣸⣿⣿⣿⣿⣿⠟⠉⠉⠉⠉⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡯⠐⣡⣾⣿⣿⣿⣿⣿⣿⠻⣎⠻⣿⣿⣿⣿⣇⢘⣠⣹⣿⣿⣿⣿⣧⣀⡀⣀⣀⠀⢀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧⡙⢷⣽⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡟⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣭⢻⣿⣿⣮⣻⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠙⠙⠃⢰⣌⠣⡀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⡟⠈⠙⠛⠿⠿⠿⠋⠀⠀⠀⠀⠀⢀⣄⣹⣇⠱⠘⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠟⢻⣿⠀⡆⢸⡇⢿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀
"""

CREDIT = "Coded by Mr Sabaz Ali Khan - Cyber Security Engineer"
LOG_FILE = "sms_call_log.jsonl"
API = "https://api.twilio.com/2010-04-01"
E164 = re.compile(r"^\+[1-9]\d{6,14}$")


# ----------------------------------------------------------------- helpers
def cprint(text, color="0"):
    if sys.stdout.isatty():
        print(f"\033[{color}m{text}\033[0m")
    else:
        print(text)


def show_banner():
    cprint(BANNER, "32")
    cprint("   ╔══════════════════════════════════════════════╗", "36")
    cprint("   ║            SMS  &  CALL  TOOLS               ║", "36")
    cprint(f"   ║  {CREDIT}  ║", "36")
    cprint("   ╚══════════════════════════════════════════════╝\n", "36")


def log_event(kind, **data):
    rec = {"time": datetime.utcnow().isoformat() + "Z", "type": kind, **data}
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def valid_number(num):
    return bool(E164.match(num.strip()))


class Twilio:
    def __init__(self):
        self.sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
        self.token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
        self.sender = os.getenv("TWILIO_FROM", "").strip()
        if not (self.sid and self.token):
            cprint("[!] Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN first.", "31")
            sys.exit(1)

    def _request(self, method, path, data=None):
        url = f"{API}/Accounts/{self.sid}/{path}"
        body = urllib.parse.urlencode(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method)
        auth = base64.b64encode(f"{self.sid}:{self.token}".encode()).decode()
        req.add_header("Authorization", f"Basic {auth}")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            try:
                err = json.loads(e.read().decode())
                raise RuntimeError(f"{err.get('code')}: {err.get('message')}")
            except ValueError:
                raise RuntimeError(f"HTTP {e.code}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error: {e.reason}")

    def send_sms(self, to, body):
        return self._request("POST", "Messages.json",
                             {"To": to, "From": self.sender, "Body": body})

    def make_call(self, to, message=None, url=None):
        data = {"To": to, "From": self.sender}
        if url:
            data["Url"] = url
        else:
            data["Twiml"] = (f"<Response><Say>{escape(message)}</Say></Response>")
        return self._request("POST", "Calls.json", data)

    def list_messages(self, limit=10):
        return self._request("GET", f"Messages.json?PageSize={limit}")["messages"]

    def list_calls(self, limit=10):
        return self._request("GET", f"Calls.json?PageSize={limit}")["calls"]

    def get_message(self, sid):
        return self._request("GET", f"Messages/{sid}.json")

    def get_call(self, sid):
        return self._request("GET", f"Calls/{sid}.json")

    def balance(self):
        return self._request("GET", "Balance.json")


# ----------------------------------------------------------------- actions
def ask_number(prompt):
    num = input(prompt).strip()
    if not valid_number(num):
        cprint("[!] Use international E.164 format, e.g. +923001234567", "31")
        return None
    return num


def do_send_sms(tw):
    to = ask_number("To (+countrycode...): ")
    if not to:
        return
    body = input("Message: ").strip()
    if not body:
        return
    r = tw.send_sms(to, body)
    cprint(f"[+] Queued. SID: {r['sid']}  Status: {r['status']}", "32")
    log_event("sms", to=to, sid=r["sid"], status=r["status"])


def do_call(tw):
    to = ask_number("To (+countrycode...): ")
    if not to:
        return
    mode = input("1) Speak a message  2) Use TwiML URL : ").strip()
    if mode == "2":
        r = tw.make_call(to, url=input("TwiML URL: ").strip())
    else:
        msg = input("Message to speak: ").strip()
        if not msg:
            return
        r = tw.make_call(to, message=msg)
    cprint(f"[+] Call started. SID: {r['sid']}  Status: {r['status']}", "32")
    log_event("call", to=to, sid=r["sid"], status=r["status"])


def do_bulk(tw):
    path = input("CSV file (columns: number,message): ").strip()
    if not os.path.isfile(path):
        cprint("[!] File not found.", "31")
        return
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            num, msg = (row.get("number") or "").strip(), (row.get("message") or "").strip()
            if valid_number(num) and msg:
                rows.append((num, msg))
    if not rows:
        cprint("[!] No valid rows.", "31")
        return
    cprint(f"[i] {len(rows)} valid recipients.", "33")
    if input("Confirm every recipient has opted in to receive SMS (yes/no): ").lower() != "yes":
        cprint("[!] Cancelled.", "31")
        return
    delay = max(1.0, float(input("Delay between messages in seconds [min 1]: ") or 1))
    ok = 0
    for i, (num, msg) in enumerate(rows, 1):
        try:
            r = tw.send_sms(num, msg)
            ok += 1
            cprint(f"[{i}/{len(rows)}] {num} -> {r['status']}", "32")
            log_event("bulk_sms", to=num, sid=r["sid"], status=r["status"])
        except RuntimeError as e:
            cprint(f"[{i}/{len(rows)}] {num} FAILED: {e}", "31")
            log_event("bulk_sms_fail", to=num, error=str(e))
        time.sleep(delay)
    cprint(f"[+] Done. {ok}/{len(rows)} queued.", "36")


def do_logs(tw):
    n = int(input("How many entries [10]: ") or 10)
    cprint("\n--- Recent SMS ---", "33")
    for m in tw.list_messages(n):
        print(f"{m['date_sent'] or m['date_created']} | {m['direction']:<14} | "
              f"{m['from']} -> {m['to']} | {m['status']}")
    cprint("\n--- Recent Calls ---", "33")
    for c in tw.list_calls(n):
        print(f"{c['start_time']} | {c['direction']:<14} | "
              f"{c['from']} -> {c['to']} | {c['status']} | {c['duration']}s")


def do_status(tw):
    sid = input("Message or Call SID: ").strip()
    try:
        r = tw.get_message(sid) if sid.startswith("SM") or sid.startswith("MM") else tw.get_call(sid)
    except RuntimeError as e:
        cprint(f"[!] {e}", "31")
        return
    for k in ("sid", "status", "to", "from", "date_created", "error_code", "error_message", "duration"):
        if k in r:
            print(f"{k:<14}: {r[k]}")


def do_balance(tw):
    r = tw.balance()
    cprint(f"[i] Balance: {r['balance']} {r['currency']}", "32")


MENU = """
  [1] Send SMS
  [2] Make Call
  [3] Bulk SMS (opt-in CSV)
  [4] View SMS / Call logs
  [5] Check status by SID
  [6] Account balance
  [0] Exit
"""


def main():
    show_banner()
    tw = Twilio()
    if not valid_number(tw.sender):
        cprint("[!] Set TWILIO_FROM to your Twilio number in E.164 format.", "31")
        sys.exit(1)
    actions = {"1": do_send_sms, "2": do_call, "3": do_bulk,
               "4": do_logs, "5": do_status, "6": do_balance}
    while True:
        print(MENU)
        choice = input("Select > ").strip()
        if choice == "0":
            cprint(f"\n{CREDIT}", "36")
            break
        fn = actions.get(choice)
        if not fn:
            continue
        try:
            fn(tw)
        except (RuntimeError, ValueError) as e:
            cprint(f"[!] {e}", "31")
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()
