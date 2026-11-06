#!/usr/bin/env python3
"""WiFi actions for the eww WiFi panel (NetworkManager, via nmcli).

  wifi.py list           print the network list as JSON
  wifi.py select BSSID   disconnect if that network is active, else connect
  wifi.py toggle         WiFi radio on/off
  wifi.py watch          keep the list fresh while the panel is open

Every action pushes the new list to eww when it finishes.
"""
import html
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

LOG = Path.home() / ".cache/wifi.log"
ROFI_THEME = Path.home() / ".config/rofi/wifi-password.rasi"
SIGNAL_ICON = " "
LOCK_ICON = ""


def nmcli(*args):
    return subprocess.run(["nmcli", *args], capture_output=True, text=True)


def fields(line):
    """Split one `nmcli -t` line on unescaped colons."""
    parts = re.split(r"(?<!\\):", line)
    return [p.replace("\\:", ":").replace("\\\\", "\\") for p in parts]


def say(message):
    """Show a desktop notification (replacing the previous one) and log it."""
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"{datetime.now():%F %T} {message}\n")
    subprocess.run(["notify-send", "-h", "string:x-dunst-stack-tag:wifi",
                    "WiFi", html.escape(message)])


# --- reading state ----------------------------------------------------------

def scan():
    """All visible access points (from NetworkManager's cache, no rescan)."""
    out = nmcli("-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY,BSSID",
                "device", "wifi", "list", "--rescan", "no").stdout
    aps = []
    for line in out.splitlines():
        in_use, ssid, signal, security, bssid = fields(line)
        if ssid:
            aps.append({"ssid": ssid, "signal": int(signal or 0),
                        "security": security, "bssid": bssid,
                        "connected": in_use == "*"})
    return aps


def is_secured(security):
    return security not in ("", "--")


def networks():
    """One entry per SSID (active or strongest AP), active first, as eww expects."""
    best = {}
    for ap in scan():
        old = best.get(ap["ssid"])
        if not old or (ap["connected"], ap["signal"]) > (old["connected"], old["signal"]):
            best[ap["ssid"]] = ap
    ordered = sorted(best.values(), key=lambda a: (not a["connected"], -a["signal"]))
    return [{**ap, "secured": is_secured(ap["security"]),
             "sig_icon": SIGNAL_ICON, "sec_icon": LOCK_ICON} for ap in ordered]


def wifi_device():
    for line in nmcli("-t", "-f", "DEVICE,TYPE", "device").stdout.splitlines():
        device, kind = fields(line)
        if kind == "wifi":
            return device


def saved_profile(ssid):
    """UUID of the saved WiFi profile for this SSID (profile names can differ)."""
    for line in nmcli("-t", "-f", "UUID,TYPE", "connection", "show").stdout.splitlines():
        uuid, kind = fields(line)
        if kind == "802-11-wireless":
            saved = nmcli("-g", "802-11-wireless.ssid", "connection", "show", "uuid", uuid)
            if saved.stdout.strip() == ssid:
                return uuid


# --- eww --------------------------------------------------------------------

def refresh():
    data = json.dumps(networks(), separators=(",", ":"), ensure_ascii=False)
    subprocess.run(["eww", "update", f"wifi_networks={data}"], capture_output=True)


def panel_open():
    return "wifi_window" in subprocess.run(
        ["eww", "active-windows"], capture_output=True, text=True).stdout


# --- actions ----------------------------------------------------------------

def ask_password(ssid):
    out = subprocess.run(
        ["rofi", "-dmenu", "-password", "-p", "", "-mesg", ssid,
         "-theme", str(ROFI_THEME)],
        input="", capture_output=True, text=True).stdout
    return out.strip()


def connect(ap):
    ssid = ap["ssid"]
    say(f"Connecting to {ssid}...")
    uuid = saved_profile(ssid)

    if uuid:
        result = nmcli("--wait", "20", "connection", "up", "uuid", uuid)
        # Saved password missing or rejected: ask once, keep the profile.
        if result.returncode and "secret" in result.stderr.lower():
            password = ask_password(ssid)
            if password:
                nmcli("connection", "modify", "uuid", uuid, "wifi-sec.psk", password)
                result = nmcli("--wait", "20", "connection", "up", "uuid", uuid)
    else:
        args = ["--wait", "20", "device", "wifi", "connect", ssid, "bssid", ap["bssid"]]
        if is_secured(ap["security"]):
            password = ask_password(ssid)
            if not password:
                say("Cancelled")
                return
            args += ["password", password]
        result = nmcli(*args)
        if result.returncode:  # don't leave a half-made profile behind
            created = saved_profile(ssid)
            if created:
                nmcli("connection", "delete", "uuid", created)

    if result.returncode:
        say(f"Could not connect to {ssid}: {result.stderr.strip() or 'failed'}")
    else:
        say(f"Connected to {ssid}")


def select(bssid):
    aps = scan()
    ap = next((a for a in aps if a["bssid"] == bssid), None)
    if not ap:
        say("Network is no longer in range")
    elif any(a["connected"] and a["ssid"] == ap["ssid"] for a in aps):
        # `device disconnect` also stops NetworkManager from auto-reconnecting.
        nmcli("device", "disconnect", wifi_device())
        say(f"Disconnected from {ap['ssid']}")
    else:
        connect(ap)
    refresh()


def toggle():
    on = nmcli("radio", "wifi").stdout.strip() == "enabled"
    nmcli("radio", "wifi", "off" if on else "on")
    time.sleep(1)
    refresh()


def watch():
    """Refresh now, then rescan every ~8s for as long as the panel is open."""
    refresh()
    while True:
        nmcli("device", "wifi", "rescan")  # may be refused if too soon; harmless
        time.sleep(2)
        refresh()
        if not panel_open():
            return
        time.sleep(6)


if __name__ == "__main__":
    action, *rest = sys.argv[1:] or ["list"]
    if action == "list":
        print(json.dumps(networks(), separators=(",", ":"), ensure_ascii=False))
    elif action == "select" and rest:
        select(rest[0])
    elif action == "toggle":
        toggle()
    elif action == "watch":
        watch()
    else:
        sys.exit(__doc__)
