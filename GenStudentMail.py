import pymongo
import smtplib
import datetime
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
for x in mycol.find():
    out = "Absent"
    if(x["present"]):
        out= "present"
    msg = MIMEMultipart() # create a message 
    message = message_template.substitute(student_roll=x["roll"], present=out, date=datetime.date.today())
    msg['From']='attendancemailcssea@gmail.com'
    msg['To']=x['email']
    msg['Subject']='Attendance'
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
print("Mails Sent succusfully!!")