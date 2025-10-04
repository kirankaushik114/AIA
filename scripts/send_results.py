#!/usr/bin/env python3
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from xml.etree import ElementTree as ET

# --------------------------------------------------------------------
# Read environment variables
# --------------------------------------------------------------------
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
EMAIL_TO = os.environ.get('EMAIL_TO')
EMAIL_FROM = os.environ.get('EMAIL_FROM', SMTP_USER)

REPORT_DIR = 'reports'
REPORT_HTML = os.path.join(REPORT_DIR, 'report.html')
LOG_HTML = os.path.join(REPORT_DIR, 'log.html')
OUTPUT_XML = os.path.join(REPORT_DIR, 'output.xml')

# --------------------------------------------------------------------
# Validate environment variables
# --------------------------------------------------------------------
if not SMTP_HOST or not SMTP_USER or not SMTP_PASS or not EMAIL_TO:
    print('❌ Missing SMTP configuration in environment variables', file=sys.stderr)
    sys.exit(2)

# --------------------------------------------------------------------
# Compose Email
# --------------------------------------------------------------------
msg = EmailMessage()
msg['Subject'] = 'Robot Framework CI Results'
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO

body = "Attached: report.html, log.html, output.xml\n\n"

# --------------------------------------------------------------------
# Parse output.xml for summary (if available)
# --------------------------------------------------------------------
if os.path.exists(OUTPUT_XML):
    try:
        tree = ET.parse(OUTPUT_XML)
        root = tree.getroot()
        total = root.find(".//total/stat")
        stats = root.find(".//statistics/total")
        if stats is not None:
            total_tests = stats.findtext("total")
            total_pass = stats.findtext("pass")
            total_fail = stats.findtext("fail")
            body += f"Summary:\nTotal: {total_tests}, Passed: {total_pass}, Failed: {total_fail}\n"
        else:
            body += "Output XML parsed but no summary found.\n"
    except Exception as e:
        body += f"⚠️ Could not parse output.xml for summary: {e}\n"
else:
    body += "⚠️ No output.xml found. Only report and log will be attached.\n"

msg.set_content(body)

# --------------------------------------------------------------------
# Attach result files (HTML, XML)
# --------------------------------------------------------------------
for path in (REPORT_HTML, LOG_HTML, OUTPUT_XML):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        maintype, subtype = "application", "octet-stream"
        if path.endswith(".html"):
            maintype, subtype = "text", "html"
        elif path.endswith(".xml"):
            maintype, subtype = "application", "xml"
        msg.add_attachment(data, maintype=maintype, subtype=subtype,
                           filename=os.path.basename(path))

# --------------------------------------------------------------------
# Send email via SMTP (TLS)
# --------------------------------------------------------------------
context = ssl.create_default_context()
try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print(f"✅ Email sent successfully to {EMAIL_TO}")
except Exception as e:
    print(f"❌ Failed to send email: {e}", file=sys.stderr)
    sys.exit(1)
