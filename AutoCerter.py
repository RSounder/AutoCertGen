#Sounder Rajendran; auto cert gen and mailer
#sounderajendran@gmail.com
#make sure you have configured your csv file with headers 'name' and 'mail'

import os
import cv2
import pandas
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

if not os.path.exists('Output'):
    os.makedirs('Output')
    
data = pandas.read_csv('namestxt.csv')
nametxt = data['name'].tolist()

fromaddr = "your_gmail@gmail.com"
passwordStr = "your_password"
toaddrList = data['mail'].tolist()

#path to the certificate template
imgPath = r'template.jpg'
destPath = r'Output/' #dont forget to add / at the end. 

img = cv2.imread(imgPath)

#height, width and channels of img
h, imgWidth, c = img.shape

font = cv2.FONT_HERSHEY_SIMPLEX

#black colour font, with 3px thickness, and size 3
colour = (0,0,0)
thickness = 7
fontscale = 3

def mailer(name, toaddr, filename):
  # instance of MIMEMultipart 
  msg = MIMEMultipart() 

  # storing the senders email address   
  msg['From'] = fromaddr 

  # storing the receivers email address  
  msg['To'] = toaddr 

  # storing the subject  
  msg['Subject'] = "SEED Certs"

  # string to store the body of the mail 
  body = 'Hi ' + name + '''

  Wonderful first line
  Cute second line
  Warm Stuff


  Thanks!!
  '''

  # attach the body with the msg instance 
  msg.attach(MIMEText(body, 'plain')) 
    
  # open the file to be sent  
  attachment = open(filename, "rb")
  # instance of MIMEBase and named as p 
  p = MIMEBase('application', 'octet-stream') 
    
  # To change the payload into encoded form 
  p.set_payload((attachment).read()) 
    
  # encode into base64 
  encoders.encode_base64(p) 
     
  p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    
  # attach the instance 'p' to instance 'msg' 
  msg.attach(p) 
    
  # creates SMTP session 
  s = smtplib.SMTP('smtp.gmail.com', 587) 
    
  # start TLS for security 
  s.starttls() 
    
  # Authentication 
  s.login(fromaddr, passwordStr)

  # Converts the Multipart msg into a string 
  text = msg.as_string() 
  
  # sending the mail 
  s.sendmail(fromaddr, toaddr, text) 
    
  # terminating the session 
  s.quit()


for i in range(0, len(nametxt)):
  #coordinates for placing text. left aligned is simple.
  #but for center aligning, find the width of image and text size to center
  #55px is the width of each text character for the given font specs
  
  xcor = int(imgWidth/2) - (round(len(nametxt[i])/2)*55)

  #ycor 1490 is chosen by trial and error to fit the template.
  #note that h/2 is almost similar to ycor (1490) 
  cor = (xcor, 1490)
  
  img1 = cv2.putText(img, nametxt[i], cor,font , fontscale, colour, thickness, cv2.LINE_AA)
  cv2.imwrite( destPath + str(nametxt[i])+'.jpg',img1)
  print(str(nametxt[i]) + '.jpg created')
  mailer(nametxt[i], toaddrList[i], destPath + str(nametxt[i])+'.jpg' )
  print('Mailed to ' + nametxt[i])
  print('-----End of '+ str(i+1) +'-----')
  img = cv2.imread(imgPath)

####
