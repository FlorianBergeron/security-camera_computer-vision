
# Import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Send Email :
class MailNotification:
    def __init__(self, from_gmail, mdp_gmail, user_mail):
        self.from_gmail = from_gmail
        self.mdp_gmail = mdp_gmail
        self.user_mail = user_mail

    def init_mail(self, subject_mail, body_mail):
        msg = MIMEMultipart()
        msg['From'] = self.from_gmail
        msg['To'] = self.user_mail
        msg['Subject'] = subject_mail
        msg.attach(MIMEText(body_mail, 'plain'))
        return msg

    def init_attachement(self, file_name):
        attachment = open(file_name, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
        return part

    def send_mail(self, subject_mail, body_mail, file_path):
        msg = self.init_mail(subject_mail, body_mail)
        msg.attach(self.init_attachement(file_path))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.from_gmail, self.mdp_gmail)
        text = msg.as_string()
        server.sendmail(self.from_gmail, self.user_mail, text)
        server.quit()
