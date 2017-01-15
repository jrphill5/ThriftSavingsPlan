import smtplib, os, sys
from datetime import datetime

# Read authentication information from auth.py:
# Variables EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_FROM, EMAIL_TO, and EMAIL_SIGNAL should be defined.
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'auth.py')) as f: exec(f.read())

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

msg = MIMEMultipart()

if len(sys.argv) > 1 and sys.argv[1] == '--signal':
	msg['Subject'] = 'TSP Signal Detected on ' + datetime.now().strftime('%m/%d/%Y')
	EMAIL_TO = EMAIL_SIGNAL
else:
	msg['Subject'] = 'TSP Status for ' + datetime.now().strftime('%m/%d/%Y')

msg['From'] = EMAIL_FROM
msg['To'] = ', '.join(EMAIL_TO)

try:
	with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'TSPEmail.txt'), 'r') as fh:
		text = MIMEText('<font face="Courier New, Courier, monospace">' + fh.read().replace(' ', '&nbsp;').replace('\n', '<br />') + '</font>', 'html')
except:
	text = MIMEText('<font face="Courier New, Courier, monospace">Attached are the most recent TSP charts with signals.</font>', 'html')

msg.attach(text)

imgpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

for imgfile in sorted(os.listdir(imgpath)):
	with open(os.path.join(imgpath, imgfile), 'rb') as fp:
		img = MIMEImage(fp.read())
	img.add_header('Content-Disposition', 'attachment', filename=imgfile)
	msg.attach(img)

s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
s.starttls()
s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
s.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
s.quit()
