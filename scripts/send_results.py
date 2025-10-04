#!/usr/bin/env python3
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage

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

# Check required environment variables
if not SMTP_HOST or not SMTP_USER or not SMTP_PASS or not EMAIL_TO:
    print('Missing SMTP configuration in environment variables', file=sys.stderr)
    sys.exit(2)

msg = EmailMessage()
msg['Subject'] = 'Robot Framework CI Results'
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO

body = 'Attached: report.html, log.html, output.xml\n'

if os.path.exists(OUTPUT_XML):
    # Try to extract simple pass/fail summary from output.xml
    try:
        from xml.etree import ElementTree as ET
        tree = ET.parse(OUTPUT_XML)
        root = tree.getroot()
        totals = root.find('statistics')
        if totals is not None:
            body += 'Output XML parsed. See attachments for full details.\n'
    except Exception:
        body += 'Could not parse output.xml for summary.\n'

msg.set_content(body)

# Attach files if present
for path in (REPORT_HTML, LOG_HTML, OUTPUT_XML):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
        maintype = 'application'
        subtype = 'octet-stream'
        if path.endswith('.html'):
            maintype = 'text'
            subtype = 'html'
        elif path.endswith('.xml'):
            maintype = 'application'
            subtype = 'xml'
        msg.add_attachmen_
