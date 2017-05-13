from bbio import*
from bbio.libraries.WebCam import WebCam
from bbio.libraries.BBIOServer import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time

def streaming(num):
		if num == 0:
			print "start Streaming"
			server = BBIOServer()
			cam.startStreaming()
			vid = Page("Webcam Video")
			vid.add_video("192.168.0.1","5000")
			server.start(vid)
			bit = 1
		else:
			print "Stop Streaming"
			cam.stopstreaming()
			server.close()
			bit = 0
			

def capture():
	location = "captured"
	cam.takeSnapshot(location)
	print "saving image"

def sendmsg(str):
		print "Sending email notification"
		msg = MIMEMultipart()
		msg['Subject'] = "IMPORTANT : Beaglebone Remote Security Camera"
		msg['From'] = sender
		msg['To'] = receiver
		msg.attach(MIMEText(str,'plain'))

		######
		img = open("captured.jpeg","rb")
		msg.attach(MIMEImage(img.read()))
		img.close()
		######

		server = smtplib.SMTP_SSL("smtp.gmail.com",465)
#		server.set_debuglevel(1)
		server.ehlo()
		server.login(sender,password)
		server.sendmail(sender,receiver,msg.as_string())
		print "sent email"
		server.close()

cam = WebCam()
sender = '@gmail.com'
receiver = '@gmail.com'
password = ""
pir = GPIO1_28
bit = 0

def setup():
	pinMode(pir,INPUT,PULLUP)
	attachInterrupt(pir, motiondetect, RISING)

def loop():
	print "loop!"
	delay(1000)

def motiondetect():
	global bit
	str = "Motion detected"
	print str
	capture()
#	streaming(bit)
	sendmsg(str)

run(setup,loop)
#
