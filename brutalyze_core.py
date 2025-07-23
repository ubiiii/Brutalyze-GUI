import re
import os
import json
import time
import requests
from datetime import datetime
from collections import defaultdict

def parse_datetime(date_str):
    return datetime.strptime(date_str + " " + str(datetime.now().year), "%b %d %H:%M:%S %Y")

def get_ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return {
                "ip": ip,
                "country": data.get("country", ""),
                "region": data.get("regionName", ""),
                "city": data.get("city", "")
            }
        elif data.get("message") == "private range":
            return {
                "ip": ip,
                "country": "Private IP",
                "region": "-",
                "city": "-"
            }
    except:
        pass
    return {"ip": ip, "country": "", "region": "", "city": ""}

# Regex patterns
FAILED_LOGIN_RE = re.compile(r"Failed password for (invalid user )?(?P<user>\w+) from (?P<ip>[\d\.]+)")
SUCCESS_LOGIN_RE = re.compile(r"Accepted password for (?P<user>\w+) from (?P<ip>[\d\.]+)")
IP_RE = re.compile(r"from (?P<ip>[\d\.]+)")

def analyze_log(filepath):
    classified_logs = {
        "Failed Login": [],
        "Successful Login": [],
        "Suspicious": [],
        "Other": []
    }

    ip_cache = {}
    alerts = []
    failed_count = 0
    success_count = 0

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            timestamp_match = re.match(r"^(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})", line)
            timestamp = timestamp_match.group(1) if timestamp_match else ""

            entry = {
                "timestamp": timestamp,
                "raw": line.strip(),
                "category": "Other",
                "ip": None,
                "user": None,
                "location": None
            }

            if FAILED_LOGIN_RE.search(line):
                m = FAILED_LOGIN_RE.search(line)
                entry["category"] = "Failed Login"
                entry["ip"] = m.group("ip")
                entry["user"] = m.group("user")
                failed_count += 1

            elif SUCCESS_LOGIN_RE.search(line):
                m = SUCCESS_LOGIN_RE.search(line)
                entry["category"] = "Successful Login"
                entry["ip"] = m.group("ip")
                entry["user"] = m.group("user")
                success_count += 1

            elif "invalid user" in line or "Did not receive identification string" in line:
                entry["category"] = "Suspicious"
                m = IP_RE.search(line)
                if m:
                    entry["ip"] = m.group("ip")

            # Add geolocation if IP present
            if entry["ip"]:
                if entry["ip"] not in ip_cache:
                    ip_cache[entry["ip"]] = get_ip_geolocation(entry["ip"])
                    time.sleep(1.5)
                entry["location"] = ip_cache[entry["ip"]]

            classified_logs[entry["category"]].append(entry)

    # Alerts based on volume
    if failed_count >= 20:
        alerts.append(f"🔥 High volume of failed logins: {failed_count} attempts")
    if len(classified_logs["Suspicious"]) > 0:
        alerts.append(f"⚠️ Suspicious activity detected: {len(classified_logs['Suspicious'])} entries")

    return {
        "summary": {
            "failed_logins": failed_count,
            "successful_logins": success_count,
            "suspicious": len(classified_logs["Suspicious"]),
            "other": len(classified_logs["Other"])
        },
        "alerts": alerts,
        "classified": classified_logs
    }
