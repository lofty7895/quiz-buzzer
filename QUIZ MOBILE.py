from tkinter import *
import pymysql


win=Tk()
win.config(bg="orange")

def add_pts(team,score):
    connection=pymysql.connect(host="192.168.1.70",user="root",password="IAMACODER78",database="quiz",port=3306)
    cursor=connection.cursor()
    query="SELECT MAX(Sno) FROM quiz_entries"
    cursor.execute(query) 
    result=cursor.fetchall()
    for i in result:
        for row in i:
            Sno=row
    
    query2=f"INSERT INTO {team}(quesno,score) VALUES ({Sno},{score})"
    cursor.execute(query2)
    connection.commit()
    connection.close()

def resetbtn():
    connection=pymysql.connect(host="192.168.1.70",user="root",password="IAMACODER78",database="quiz",port=3306)
    cursor=connection.cursor()
    query="SELECT MAX(Sno) FROM quiz_entries"
    cursor.execute(query)
    result=cursor.fetchall()
    for i in result:
        for row in i:
            Sno=row
    
    query2=f"UPDATE quiz_entries SET reset_entry=\"reset\" WHERE Sno={Sno}"
    cursor.execute(query2)
    connection.commit()
    print ("reset inserted successfully")
    connection.close()



addpoints=Label(win,text="Add points to house",fg="yellow",bg="orange",font=("Arial",20))
addpoints.place(x=0,y=0)

Agni=Label(win,text="Agni: ",fg="red",bg="orange",font=("Arial",24))
Agni.place(x=0,y=130)
Agnibut1=Button(win,text="+5",fg="yellow",bg="red",font=("Arial",20),padx=10,pady=10,command=lambda: add_pts("agni",5))
Agnibut1.place(x=330,y=150)
Agnibut2=Button(win,text="-5",fg="yellow",bg="red",font=("Arial",20),padx=30,pady=10,command=lambda: add_pts("agni",-5))
Agnibut2.place(x=330,y=320)

Neer=Label(win,text="Neer: ",fg="cyan",bg="orange",font=("Arial",24))
Neer.place(x=0,y=510)
Neerbut1=Button(win,text="+5",fg="yellow",bg="blue",font=("Arial",20),padx=10,pady=10,command=lambda: add_pts("neer",5))
Neerbut1.place(x=330,y=530)
Neerbut2=Button(win,text="-5",fg="yellow",bg="blue",font=("Arial",20),padx=30,pady=10,command=lambda: add_pts("neer",-5))
Neerbut2.place(x=330,y=700)

Prithvi=Label(win,text="Prithvi: ",fg="lawn green",bg="orange",font=("Arial",24))
Prithvi.place(x=0,y=870)
Prithvibut1=Button(win,text="+5",fg="red",bg="lawn green",font=("Arial",20),padx=10,pady=10,command=lambda: add_pts("prithvi",5))
Prithvibut1.place(x=420,y=890)
Prithvibut2=Button(win,text="-5",fg="red",bg="lawn green",font=("Arial",20),padx=30,pady=10,command=lambda: add_pts("prithvi",-5))
Prithvibut2.place(x=420,y=1060)

Vayu=Label(win,text="Vayu: ",fg="yellow",bg="orange",font=("Arial",24))
Vayu.place(x=0,y=1230)
Vayubut1=Button(win,text="+5",fg="red",bg="yellow",font=("Arial",20),padx=10,pady=10,command=lambda: add_pts("vayu",5))
Vayubut1.place(x=350,y=1250)
Vayubut2=Button(win,text="-5",fg="red",bg="yellow",font=("Arial",20),padx=30,pady=10,command=lambda: add_pts("vayu",-5))
Vayubut2.place(x=350,y=1430)

reset=Button(win,command=lambda: resetbtn(),text="RESET",fg="yellow",bg="red",font=("Arial",20),padx=10,pady=10)
reset.place(x=400,y=1700)

win.mainloop()