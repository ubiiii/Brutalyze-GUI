import re
import csv
import json
import os
import requests
import time
from collections import defaultdict
from datetime import datetime, timedelta

def get_ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,query", timeout=5)
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

def analyze_log(log_path, threshold, window_minutes, blacklist_path="blacklist.txt"):
    BRUTE_THRESHOLD = threshold
    TIME_WINDOW = timedelta(minutes=window_minutes)

    FAILED_LOGIN_REGEX = re.compile(
        r"(?P<date>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) .*sshd.*Failed password for (invalid user )?(?P<user>\w+) from (?P<ip>[\d\.]+)"
    )

    failed_attempts_by_ip = defaultdict(int)
    failed_attempts_by_user = defaultdict(int)
    attempt_timestamps = defaultdict(list)
    raw_entries = []

    def parse_datetime(date_str):
        return datetime.strptime(date_str + " " + str(datetime.now().year), "%b %d %H:%M:%S %Y")

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = FAILED_LOGIN_REGEX.search(line)
            if match:
                date_str = match.group("date")
                ip = match.group("ip")
                user = match.group("user")
                dt = parse_datetime(date_str)
                failed_attempts_by_ip[ip] += 1
                failed_attempts_by_user[user] += 1
                attempt_timestamps[ip].append(dt)
                raw_entries.append((dt, ip, user))

    brute_force_ips = []
    for ip, times in attempt_timestamps.items():
        times.sort()
        for i in range(len(times) - BRUTE_THRESHOLD + 1):
            if times[i + BRUTE_THRESHOLD - 1] - times[i] <= TIME_WINDOW:
                brute_force_ips.append(ip)
                break

    blacklisted_ips = set()
    flagged_blacklist_matches = []
    if os.path.exists(blacklist_path):
        with open(blacklist_path, "r") as bl_file:
            blacklisted_ips = set(line.strip() for line in bl_file if line.strip())
        flagged_blacklist_matches = [ip for ip in failed_attempts_by_ip if ip in blacklisted_ips]

    ip_geo_data = {}
    for ip in failed_attempts_by_ip:
        ip_geo_data[ip] = get_ip_geolocation(ip)
        time.sleep(1.5)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    export_dir = "reports"
    os.makedirs(export_dir, exist_ok=True)
    csv_file = os.path.join(export_dir, f"report_{timestamp}.csv")
    json_file = os.path.join(export_dir, f"report_{timestamp}.json")
    alert_file = os.path.join(export_dir, f"alerts_{timestamp}.txt")

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["IP Address", "Country", "Region", "City", "Failed Attempts", "Brute Force Suspected", "Blacklisted"])
        for ip, count in failed_attempts_by_ip.items():
            geo = ip_geo_data[ip]
            brute = "YES" if ip in brute_force_ips else "NO"
            blacklisted = "YES" if ip in blacklisted_ips else "NO"
            writer.writerow([ip, geo["country"], geo["region"], geo["city"], count, brute, blacklisted])

    json_data = {
        "summary": {
            "total_failed_ips": len(failed_attempts_by_ip),
            "total_brute_force_ips": len(brute_force_ips)
        },
        "attempts_by_ip": [
            {
                "ip": ip,
                "failed_attempts": count,
                "brute_force": ip in brute_force_ips,
                "location": ip_geo_data[ip]
            }
            for ip, count in failed_attempts_by_ip.items()
        ]
    }

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

    alerts = []
    if len(brute_force_ips) >= 3:
        alerts.append(f"🚨 {len(brute_force_ips)} brute-force IPs detected")
    for ip in flagged_blacklist_matches:
        alerts.append(f"🚫 Blacklisted IP found: {ip}")
    if sum(failed_attempts_by_ip.values()) >= 20:
        alerts.append(f"🔥 High volume of failed logins: {sum(failed_attempts_by_ip.values())} total attempts")

    with open(alert_file, "w", encoding="utf-8") as f:
        for alert in alerts:
            f.write(alert + "\n")

    return {
        "summary": json_data["summary"],
        "alerts": alerts,
        "csv": csv_file,
        "json": json_file,
        "alerts_txt": alert_file
    }
