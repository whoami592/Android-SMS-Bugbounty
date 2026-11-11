#!/usr/bin/env python3
"""
ADB Call Tool
Coded by: Cyber Security Engineer Mr. Sabaz Ali Khan

Place, answer and end phone calls on YOUR OWN Android device over ADB.

Requirements:
  - Python 3.7+
  - Android platform-tools (adb) installed and on PATH
  - USB debugging enabled on the phone, and the computer authorized

Usage examples:
  python adb_call_tool.py                    # interactive menu
  python adb_call_tool.py call 03001234567   # place a call
  python adb_call_tool.py end                # hang up
  python adb_call_tool.py answer             # answer incoming call
  python adb_call_tool.py devices            # list connected devices
  python adb_call_tool.py -s SERIAL call 03001234567   # pick a device
"""

import argparse
import re
import shutil
import subprocess
import sys
from urllib.parse import quote

BANNER = r"""
⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀⠀⠀⣴⣶⣶⣶⣶⣤⣤⣤⣴⣦⣄⣛⣿⣿⣦⡀
⠀⠀⠀⢀⣾⣿⠏⠀⠀⠀⠀⠀⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣧
⠀⠀⠀⢻⠋⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠛
⠀⠀⠀⣼⡷⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⠁⠀
⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠘⠛⠛⠛⠛⠛⠻⣽⢟⣇⡟⡿⠿⣿⣿⣿⣿⠀⠀
⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⢀⡀⠀⠀⠀⣰⣿⠁⠀⠀⠈⠙⣿⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢓⣶⣾⣿⣟⡃⣀⠀⢻⣿⡀⠤⢤⣄⠑⢿⡇⠀⠀
⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⠟⠙⠁⣼⣿⣿⣿⣶⣶⣿⣿⡇⠀⠀
⠀⠀⠀⡿⣦⠀⠀⢠⠀⠀⠀⢿⣿⣿⡿⠁⠈⠛⠀⢿⣿⣿⡌⢿⣿⣿⣿⡇⣠⣤
⠀⠀⠀⣇⠁⠀⠀⠸⠀⠀⠀⢸⡿⠿⠇⠀⠀⠀⠀⢀⣥⣾⣷⠀⠹⣿⡿⢰⣿⣿
⠀⠀⠀⢻⠀⠀⠀⡇⠀⠀⢠⢿⠀⡀⠀⢀⣐⣛⣳⠿⠿⠿⢿⡷⠀⣿⡅⣾⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠘⡀⠀⠘⣎⠀⠉⠲⢬⣉⣛⣛⣛⣛⣠⣶⡖⣰⣿⠁⠉⠉⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⠀⠀⢠⣤⣭⣿⣯⣽⣿⣟⡐⠁⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣄⣽⣿⣿⣿⣿⣿⣿⡿⢰⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡆⠀⠀⠀⠀⠀⠈⠙⠿⢿⣿⣿⣿⣿⠛⣵⣿⡀⠀⠀⠀⠀⠀
"""

CREDIT = """
        ADB CALL TOOL
        Coded by: Cyber Security Engineer
                  Mr. Sabaz Ali Khan
"""

KEYCODE_CALL = 5      # answer / dial
KEYCODE_ENDCALL = 6   # hang up

PHONE_RE = re.compile(r"^\+?[0-9*#\-\s()]{3,20}$")


def show_banner():
    print(BANNER)
    print(CREDIT)


class AdbError(Exception):
    pass


class Adb:
    def __init__(self, serial=None):
        self.serial = serial
        if shutil.which("adb") is None:
            raise AdbError(
                "adb not found. Install Android platform-tools and add it to PATH."
            )

    def _base(self):
        cmd = ["adb"]
        if self.serial:
            cmd += ["-s", self.serial]
        return cmd

    def run(self, *args, timeout=20):
        cmd = self._base() + list(args)
        try:
            res = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            raise AdbError("adb command timed out.")
        out = (res.stdout or "").strip()
        err = (res.stderr or "").strip()
        if res.returncode != 0:
            raise AdbError(err or out or "adb command failed.")
        return out

    def shell(self, *args, timeout=20):
        return self.run("shell", *args, timeout=timeout)

    # ---- device management ----
    def devices(self):
        out = subprocess.run(
            ["adb", "devices", "-l"], capture_output=True, text=True
        ).stdout
        lines = [l for l in out.splitlines()[1:] if l.strip()]
        return lines

    def check_device(self):
        state = self.run("get-state")
        if state != "device":
            raise AdbError(f"Device state is '{state}', expected 'device'.")

    # ---- call actions ----
    def call(self, number):
        number = number.strip()
        if not PHONE_RE.match(number):
            raise AdbError("Invalid phone number format.")
        clean = re.sub(r"[\s\-()]", "", number)
        uri = "tel:" + quote(clean, safe="+")
        out = self.shell(
            "am", "start", "-a", "android.intent.action.CALL", "-d", uri
        )
        if "Error" in out or "Exception" in out:
            raise AdbError(out)
        return f"Calling {clean} ..."

    def dial(self, number):
        """Open the dialer with the number filled in (no auto call)."""
        clean = re.sub(r"[\s\-()]", "", number.strip())
        uri = "tel:" + quote(clean, safe="+")
        self.shell("am", "start", "-a", "android.intent.action.DIAL", "-d", uri)
        return f"Dialer opened with {clean}"

    def end(self):
        self.shell("input", "keyevent", str(KEYCODE_ENDCALL))
        return "Call ended."

    def answer(self):
        self.shell("input", "keyevent", str(KEYCODE_CALL))
        return "Answer key sent."

    def call_state(self):
        out = self.shell("dumpsys", "telephony.registry")
        m = re.search(r"mCallState=(\d)", out)
        states = {"0": "IDLE", "1": "RINGING", "2": "OFFHOOK (in call)"}
        return states.get(m.group(1), "UNKNOWN") if m else "UNKNOWN"

    def device_info(self):
        model = self.shell("getprop", "ro.product.model")
        brand = self.shell("getprop", "ro.product.brand")
        android = self.shell("getprop", "ro.build.version.release")
        return f"{brand} {model} | Android {android}"


def interactive(adb):
    menu = """
 [1] Make a call
 [2] Open dialer with number
 [3] End call
 [4] Answer incoming call
 [5] Show call state
 [6] Device info
 [7] List devices
 [0] Exit
"""
    while True:
        print(menu)
        choice = input("Select > ").strip()
        try:
            if choice == "1":
                num = input("Phone number: ")
                print(adb.call(num))
            elif choice == "2":
                num = input("Phone number: ")
                print(adb.dial(num))
            elif choice == "3":
                print(adb.end())
            elif choice == "4":
                print(adb.answer())
            elif choice == "5":
                print("Call state:", adb.call_state())
            elif choice == "6":
                print(adb.device_info())
            elif choice == "7":
                for line in adb.devices() or ["No devices found."]:
                    print(line)
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
        except AdbError as e:
            print(f"[!] {e}")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break


def main():
    parser = argparse.ArgumentParser(description="ADB Call Tool")
    parser.add_argument("-s", "--serial", help="device serial (if several connected)")
    sub = parser.add_subparsers(dest="cmd")

    p_call = sub.add_parser("call", help="place a call")
    p_call.add_argument("number")
    p_dial = sub.add_parser("dial", help="open dialer with number")
    p_dial.add_argument("number")
    sub.add_parser("end", help="end current call")
    sub.add_parser("answer", help="answer incoming call")
    sub.add_parser("state", help="show call state")
    sub.add_parser("info", help="show device info")
    sub.add_parser("devices", help="list devices")

    args = parser.parse_args()
    show_banner()

    try:
        adb = Adb(args.serial)
        if args.cmd == "devices":
            for line in adb.devices() or ["No devices found."]:
                print(line)
            return
        adb.check_device()
        if args.cmd is None:
            print("Connected:", adb.device_info())
            interactive(adb)
        elif args.cmd == "call":
            print(adb.call(args.number))
        elif args.cmd == "dial":
            print(adb.dial(args.number))
        elif args.cmd == "end":
            print(adb.end())
        elif args.cmd == "answer":
            print(adb.answer())
        elif args.cmd == "state":
            print("Call state:", adb.call_state())
        elif args.cmd == "info":
            print(adb.device_info())
    except AdbError as e:
        print(f"[!] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
