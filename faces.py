import numpy as np
import cv2 
import pickle
import sqlite3
import datetime
# from flask import Flask,render_template

# app=Flask(__name__)

# @app.route("/")
# def home():
# 	return render_template("index.php")



# if __name__=="__main__":
# 	app.run()

conn = sqlite3.connect('Automated_attendance.db')
c = conn.cursor()
# c.execute("""DROP TABLE attendance_details""")
face_cascade = cv2.CascadeClassifier('D:\\Project\\src\\cascades\\data\\haarcascade_frontalface_alt2.xml')

labels = {"person-name":0}

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

with open("lables.pickle",'rb') as f:
	og_labels =pickle.load(f)
	labels={v:k for k,v in og_labels.items()}

attendance_list=[]
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

while(True):

	ret,frame=cap.read()
	# print(ret)
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	
	faces = face_cascade.detectMultiScale(gray,scaleFactor=1.5, minNeighbors=5)
	for(x,y,w,h) in faces:
		# print(x,y,w,h)
		roi_gray = gray[y:y+h,x:x+h]
		roi_color = frame[y:y+h,x:x+h]

#recognition

		id_ ,conf = recognizer.predict(roi_gray)
		if(conf > 100):
			name="unknown"
			break
		else:
			name= labels[id_]

		font=cv2.FONT_HERSHEY_SIMPLEX
		  
		color = (255,255,0)
		stroke =2
		cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)	

		today = datetime.datetime.now()
		# dd/mm/YY
		 
		date = today.strftime("%d/%m/%Y")
		time = today.strftime("%H:%M:%S")
		print(date)
		print(time)
		
		c.execute("""CREATE TABLE IF NOT EXISTS attendance_details (
				reg_no text,
				status text,
				day text,
				timing text	 	 
			)""")
		reg_no=name
		status="present"
		new_student=1
		size=len(attendance_list)
		print(size)
		for i in range(size):

			if reg_no==str(attendance_list[i]):
				new_student=0
		if new_student==1:
			attendance_list.append(reg_no)
						 
		print(new_student)
		# print(type(reg_no))
		# print(type(attendance_list[0]))
		print(attendance_list)
		if(reg_no!="unknown" and new_student==1):
			c.execute("Insert into attendance_details values(:reg_no,:status,:today,:time)",{
				'reg_no':reg_no,
				'status':status,
				'today' :date,
				'time' :time
				})

			conn.commit()
		c.execute("SELECT * from attendance_details")
		records=c.fetchall()

		print(attendance_list)
		color = (255,0,0)
		stroke = 5
		end_cord_x = x + w
		end_cord_y = y + h
		cv2.rectangle(frame ,(x,y) ,(end_cord_x, end_cord_y),color,stroke)

	cv2.imshow('frame',frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break
c.execute("SELECT * from attendance_details")
records = c.fetchall()
print(records)
conn.close() 
cap.release()
cv2.destroyAllWindows()


