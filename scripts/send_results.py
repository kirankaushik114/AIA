#!/usr/bin/env python3
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from xml.etree import ElementTree as ET
from dotenv import load_dotenv
load_dotenv()


print("🚀 Starting send_results.py ...")

# Read environment variables
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM", SMTP_USER)

print("🔍 Environment variables:")
for key, val in {
    "SMTP_HOST": SMTP_HOST,
    "SMTP_PORT": SMTP_PORT,
    "SMTP_USER": SMTP_USER,
    "SMTP_PASS": "***" if SMTP_PASS else None,
    "EMAIL_TO": EMAIL_TO,
    "EMAIL_FROM": EMAIL_FROM,
}.items():
    print(f"  {key} = {val}")

REPORT_DIR = "reports"
REPORT_HTML = os.path.join(REPORT_DIR, "report.html")
LOG_HTML = os.path.join(REPORT_DIR, "log.html")
OUTPUT_XML = os.path.join(REPORT_DIR, "output.xml")

print("\n📁 Checking for report files:")
for f in [REPORT_HTML, LOG_HTML, OUTPUT_XML]:
    print(f"  {f} -> {'✅ found' if os.path.exists(f) else '❌ missing'}")

if not SMTP_HOST or not SMTP_USER or not SMTP_PASS or not EMAIL_TO:
    print("\n❌ Missing SMTP configuration — exiting early.")
    sys.exit(2)

# Compose email
msg = EmailMessage()
msg["Subject"] = "Robot Framework CI Results"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO
body = "Attached: report.html, log.html, output.xml\n\n"

# Parse output.xml for summary
if os.path.exists(OUTPUT_XML):
    try:
        tree = ET.parse(OUTPUT_XML)
        root = tree.getroot()
        stats = root.find(".//statistics/total")
        if stats is not None:
            total_tests = stats.findtext("total")
            total_pass = stats.findtext("pass")
            total_fail = stats.findtext("fail")
            body += f"🧪 Summary: {total_tests} total, {total_pass} passed, {total_fail} failed\n"
        else:
            body += "⚠️ Could not extract stats from XML.\n"
    except Exception as e:
        body += f"⚠️ XML parsing error: {e}\n"

msg.set_content(body)

# Attach files
for path in (REPORT_HTML, LOG_HTML, OUTPUT_XML):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        msg.add_attachment(
            data,
            maintype="application",
            subtype="octet-stream",
            filename=os.path.basename(path),
        )
        print(f"📎 Attached: {path}")

# Send email
print(f"\n📤 Connecting to {SMTP_HOST}:{SMTP_PORT} as {SMTP_USER} ...")
context = ssl.create_default_context()
try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print(f"✅ Email sent successfully to {EMAIL_TO}")
except Exception as e:
    print(f"❌ Error sending email: {e}")
    sys.exit(1)
