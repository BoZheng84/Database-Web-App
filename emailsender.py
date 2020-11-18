from email.mime.text import MIMEText
import smtplib


def send_mail(email, height, average_height, count):
    from_email = "working.hard.bo@gmail.com"
    from_password = "Aoyu082313!"
    to_email = email

    subject = "Height data"
    message = "Hey there, your height is <strong>%s</strong>. Averag height of all is <strong>%s</strong> and that is calculated out <strong>%s</strong> of people." % (height, average_height, count)  # height value will be in bold.

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
