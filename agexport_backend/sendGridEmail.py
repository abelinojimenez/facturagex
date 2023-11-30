# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from pydoc import resolve
from dotenv import load_dotenv
load_dotenv()
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
class SendEmail:

    def __init__(self):
        self.SENDGRID_API_KEY=os.getenv("SENDGRID_API_KEY")
    def sendRecovery(self,subject="Recuperacion de contraseña",to_emails=[],text_content="",from_email="noreplay@efectup.com"):
        try:
            self.message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content='<strong>'+text_content+'</strong>')

            sg = SendGridAPIClient(self.SENDGRID_API_KEY)
            response = sg.send(self.message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return response
        except Exception as e:
            print(e.message)