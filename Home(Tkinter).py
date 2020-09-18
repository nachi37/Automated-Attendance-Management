from tkinter import *
import os
import os
import cv2
import sqlite3
#import faces
def training():
	os.system('python faces-train.py')


def show_attend():
	screen2=Toplevel(screen)
	screen2.geometry("500x500")
	screen2.title("Marked attendance" )
	conn = sqlite3.connect('Automated_attendance.db')
	c = conn.cursor()
	c.execute("SELECT * from attendance_details")
	records=c.fetchall()
	print(records)
	name_label=Label(screen2,text ="Name ",font="Arial 12 bold italic")
	name_label.grid(row=0,column=0)

	year_label=Label(screen2,text ="Status ",font="Arial 12 bold italic")
	year_label.grid(row=0,column=1)

	branch_label=Label(screen2,text ="Date ",font="Arial 12 bold italic")
	branch_label.grid(row=0,column=2)

	course_label = Label(screen2,text="Time ",font="Arial 12 bold italic")
	course_label.grid(row=0,column=3)
	row=1
	print_records=''
	for record in records:
		for i in range(4):
			print_records = str(record[i])+" "
			query_lebel = Label(screen2, text=print_records,font = "Arial 12 normal normal")	
			query_lebel.grid(row=row,column=i)
		row+=1
		  
	 
	# query_lebel = Label(screen2, text=print_records,font = "Arial 12 normal normal")	
	# query_lebel.grid(row="0",column="0")	
	quit = Button(screen2,text="Quit",command=screen2.destroy,font = "Arial 14 bold normal",pady="10")
	quit.grid(row=row,column=3)



def show_regis():
	screen2=Toplevel(screen)
	screen2.geometry("500x500")
	screen2.title("Registered Students" )
	conn = sqlite3.connect('Automated_attendance.db')
	c = conn.cursor()
	c.execute("SELECT * from student_details")
	records=c.fetchall()
	print(records)

	name_label=Label(screen2,text ="Name ",font="Arial 12 bold italic")
	name_label.grid(row=0,column=0)

	year_label=Label(screen2,text ="Year ",font="Arial 12 bold italic")
	year_label.grid(row=0,column=1)

	branch_label=Label(screen2,text ="Branch ",font="Arial 12 bold italic")
	branch_label.grid(row=0,column=2)

	course_label = Label(screen2,text="Course ",font="Arial 12 bold italic")
	course_label.grid(row=0,column=3)

	reg_label=Label(screen2,text ="Registration No.",font="Arial 12 bold italic")
	reg_label.grid(row=0,column=4)
	row=1
	print_records=''
	for record in records:
		for i in range(5):
			print_records = str(record[i])+" "
			query_lebel = Label(screen2, text=print_records,font = "Arial 12 normal normal")	
			query_lebel.grid(row=row,column=i)
		row+=1
		  
	 
	# query_lebel = Label(screen2, text=print_records,font = "Arial 12 normal normal")	
	# query_lebel.grid(row="0",column="0")	
	quit = Button(screen2,text="Quit",command=screen2.destroy,font = "Arial 14 bold normal",pady="10")
	quit.grid(row=row,column=3)

def recognition():
    os.system('python faces.py')

# def dataset():
# 	os.system('python dataset-creator.py')
def capture():
	#Capture student image
	
	Id= name.get()
	cam = cv2.VideoCapture(0)
	detector=cv2.CascadeClassifier('D:\\Project\\src\\cascades\\data\\haarcascade_frontalface_alt2.xml')

	 
	os.mkdir("images/"+Id)
	sampleNum=0
	while(sampleNum!=200):
	    ret, img = cam.read()
	    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	    faces = detector.detectMultiScale(gray,scaleFactor=1.5, minNeighbors=5)
	    for (x,y,w,h) in faces:
	        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	        
	        #incrementing sample number 
	        sampleNum=sampleNum+1
	        #saving the captured face in the dataset folder
	        #cv2.imwrite("images/user/."+Id+'.'+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
	        cv2.imwrite("images/"+Id+"/"+Id+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])

	        cv2.imshow('frame',img)

	    if cv2.waitKey(1) & sampleNum==200:
	        break
	cam.release()
	cv2.destroyAllWindows()

def data():
	#create database or connect to existing database
	conn = sqlite3.connect('Automated_attendance.db')
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS student_details (
			name text,
			year text,
			branch text,
			course text,
			reg_no text,
			password text
		)""")

	c.execute("Insert into student_details values(:name, :year, :branch, :course, :reg_no, :password)",
		{
			'name':name.get(),
			'year':year.get(),
			'branch':branch.get(),
			'course':course.get(),
			'reg_no':reg_no.get(),
			'password':password.get()
		})

	c.execute("SELECT *,oid from student_details")
	records = c.fetchall()
	print(records)

	conn.commit()
	conn.close()
	#register user to database	


	name.delete(0,END)
	year.delete(0,END)
	branch.delete(0,END)
	course.delete(0,END)
	reg_no.delete(0,END)
	password.delete(0,END)


def register():
	screen1=Toplevel(screen)
	screen1.geometry("500x500")
	screen1.title("Register" )
	 

	global name,year,branch,course,reg_no,password
	name=Entry(screen1,width="20")
	name.grid(row=0,column=1,padx=30)

	year=Entry(screen1,width="20")
	year.grid(row=1,column=1 )

	# branch_var = StringVar()
	# branch_var.set("CSE")
	branch=Entry(screen1,width="20")
	branch.grid(row=2,column=1 )

	course = Entry(screen1,width="20")
	course.grid(row=3,column=1)

	reg_no=Entry(screen1,width="20")
	reg_no.grid(row=4,column=1,padx=30)

	password = Entry(screen1,width=20)
	password.grid(row=5,column=1,padx=30)

	name_label=Label(screen1,text ="Name",font="Arial 12 bold italic")
	name_label.grid(row=0,column=0)

	year_label=Label(screen1,text ="Year",font="Arial 12 bold italic")
	year_label.grid(row=1,column=0)

	branch_label=Label(screen1,text ="Branch",font="Arial 12 bold italic")
	branch_label.grid(row=2,column=0)

	course_label = Label(screen1,text="Course",font="Arial 12 bold italic")
	course_label.grid(row=3,column=0)

	reg_label=Label(screen1,text ="Registration No.",font="Arial 12 bold italic")
	reg_label.grid(row=4,column=0)
	
	password_label=Label(screen1,text="Password",font="Arial 12 bold italic")
	password_label.grid(row=5,column=0)
 
	image=Button(screen1,text="Take Image",command=capture ,font="Arial 14 bold italic")
	image.grid(row=6,column=1)

	regis=Button(screen1,text="Submit data",command=data ,font="Arial 14 bold italic")
	regis.grid(row=7,column=1)

	quit = Button(screen1,text="Quit",command=screen1.destroy,font="Arial 14 bold italic")
	quit.grid(row=8,column=1)
	 

def Home():
	global screen
	screen=Tk()
	screen.geometry("400x400")
	screen.title("Home" )
	register_button=Button(text= "Register User", height= "2", command = register,font="Arial 12 bold italic") 
	register_button.grid(row="0",column="0",ipadx="40",padx="90")
	train_button=Button(text="Train images",height= "2", command=training,font="Arial 12 bold italic")
	train_button.grid(row="1",column="0",ipadx="40")
	recognize_button=Button(text= "Take attendance", height= "2", command = recognition,font="Arial 12 bold italic") 
	recognize_button.grid(row="2",column="0",ipadx="30")
	show_registered=Button(text="Show registered student",height= "2",command=show_regis,font="Arial 12 bold italic")
	show_registered.grid(row="3",column="0",ipadx="10")
	show_attendance=Button(text="Show attendance",height="2",command=show_attend,font="Arial 12 bold italic")
	show_attendance.grid(row="4",column="0",ipadx="20")
	quit_button=Button(text="Quit",height= "2",command=screen.destroy,font="Arial 14 bold italic")
	quit_button.grid(row="5",column="0",ipadx="20")
	


	screen.mainloop()

Home()
