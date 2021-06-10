import pymongo
import smtplib
import datetime
import os 
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Students"]

mycol = mydb["StudentDetails"]

# set up the SMTP server
s = smtplib.SMTP(host ='smtp.gmail.com', port=587)
s.starttls()
s.login('attendancemailcssea@gmail.com','Csse@123')

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


message_template = read_template('Message.txt')
with open("present.txt", 'r+') as f:
    f.truncate(0)
with open("absent.txt", 'r+') as f:
    f.truncate(0)
for x in mycol.find().sort("roll"):
    out = "Absent"
    if(x["present"]):
        out= "present"
        with open("present.txt", 'a+') as f:
            f.write(x["roll"]+"\n")
    else:
        with open("absent.txt", 'a+') as f:
            f.write(x["roll"]+"\n")
    
msg = EmailMessage()
msg["From"] = "attendancemailcssea@gmail.com"
msg["Subject"] = "Attendance"
teacher_mail = input("Enter Teachers Mail: ")
msg["To"] = teacher_mail
msg.set_content(f"present's and abset's on {datetime.date.today()}")
msg.add_attachment(open('present.txt', "r").read(), filename="present.txt")
msg.add_attachment(open('absent.txt', "r").read(), filename="absent.txt")
# send the message via the server set up earlier.
s.send_message(msg)
del msg
print("Mails Sent succusfully!!")