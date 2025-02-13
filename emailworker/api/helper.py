class EmailBodyJson:
    def __init__(self,bodydata):
        self.bodydata = bodydata #json format

class EmailRequestBody:
    def __init__(self, email,template,subject,EmailBodyJson):
        self.email = email #sender email
        self.template = template #template name
        self.subject = subject #subject
        self.EmailBody = EmailBodyJson #body of email

