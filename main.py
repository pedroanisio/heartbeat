import time
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import os
from pathlib import Path

home_path: str = str(Path.home())
home_path = f"{home_path}/cron"

if not os.path.exists(home_path):
    os.makedirs(home_path)

os.chdir(home_path)

beats_filename = "beats.txt"
events_filename = "events.txt"
number_of_lines = 60
diff_threshold = 70

def create_files(filename):
    f = open(filename,"a")
    f.close()


def send_email(text):
    sender_email = "pals.1980.dev@gmail.com"
    receiver_email = "pedroanisio@gmail.com"
    password = "wm4g65gh"
    hostname = socket.gethostname()

    message = MIMEMultipart("alternative")
    message["Subject"] = text
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    plain = f"""\
    heartbeat checker
    hostname: {hostname}
    """
    html = f"""\
    <html>
      <body>
        <p>heartbeat checker</p>
        <p>hostname: {hostname}
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def check_if_event_exists(event):
    fh = open(events_filename, 'r')
    for line in fh:
        if re.search(f"^{event}.*", line.rstrip()):
            return True
    fh.close()
    return False


def write_event(event_start, event_end):
    e = open(events_filename, "a")
    e.write(f"{event_start},{event_end}\n")
    e.close()

create_files(beats_filename)
create_files(events_filename)

beats_array = []
f = open(beats_filename, "r")
num_lines = sum(1 for line in f)
f.close()

if num_lines > number_of_lines:
    i = 0
    with open(beats_filename, "r") as f:
        for line in (f.readlines()[-number_of_lines:]):
            beats_array.append(float(line))
            i = i + 1
n = len(beats_array) - 1

while n > 0:
    diff = beats_array[n] - beats_array[n - 1]
    if diff > diff_threshold:

        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(beats_array[n - 1]))
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(beats_array[n]))
        if not check_if_event_exists(str(beats_array[n - 1])):
            text = f"skipped {int(diff / 60)} beats from {start_time} to {end_time}"
            write_event(str(beats_array[n - 1]), str(beats_array[n]))
            send_email(text)
    n = n - 1