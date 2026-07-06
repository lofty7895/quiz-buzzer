import pymysql
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

import sys

def donothing():
    pass
def verify():
    username=userentry.get()
    password=pwentry.get()
    if username=="admin" and password=="securequiz":
        temp.after(0,temp.destroy())
    else:
        userentry.delete(0,END)
        pwentry.delete(0,END)
        label.config(text="incorrect password or username")

temp=Tk()
temp.protocol("WM_DELETE_WINDOW",donothing)
userx=StringVar()
user=Label(temp,text="username")
user.place(x=0,y=0)
userentry=Entry(temp,textvariable=userx)
userentry.place(x=70,y=0)
pwx=StringVar()
pw=Label(temp,text="password")
pw.place(x=0,y=20)
pwentry=Entry(temp,textvariable=pwx,show="*")
pwentry.place(x=70,y=30)
label=Label(temp,text="",fg="red")
label.place(x=20,y=110)
submit=Button(temp,text="SUBMIT",command=lambda: verify())
submit.place(x=60,y=60)
temp.mainloop()

def sendmsg(message):
    text_output.insert(END,message+"\n")
    text_output.see(END)


# Set up the MySQL connection
def handle_client(client_socket):
        global reset
        request = client_socket.recv(1024).decode()
        print (request)
        sendmsg (request)
        
        # Example parsing the request, suppose we expect "SEND_QUIZ:<score>"
        if request.startswith("CHECK FOR RESET EXTRA:"):
            Sno = int(request.split(":")[1])
            reset=""
            db = pymysql.connect(
            host="localhost",
            user="root",
            password="IAMACODER78",
            database="quiz"
            )
            cursor=db.cursor()
            cursor.execute(f"SELECT reset_entry FROM quiz_entries WHERE Sno={Sno}")
            result = cursor.fetchall()
            for i in result:
                for j in i:
                    reset=j
            db.close()
            if len(result)==0:
                client_socket.send(str("x").encode())
                sendmsg(f"x msg sent")
            elif reset=="":
                client_socket.send(str("y").encode())
                sendmsg (f"y msg sent")
            else:
                client_socket.send(str(reset).encode())
                sendmsg (f"{reset} msg sent")
                

        elif request.startswith("CHECK FOR RESET:"):
            Sno = int(request.split(":")[1])
            reset=""
            while reset!="reset":
                db = pymysql.connect(
                host="localhost",
                user="root",
                password="IAMACODER78",
                database="quiz"
                )
                cursor=db.cursor()
                cursor.execute(f"SELECT reset_entry FROM quiz_entries WHERE Sno={Sno}")
                result = cursor.fetchall()
                for i in result:
                    for j in i:
                        reset=j
                db.close()
            sendmsg (reset)
            # Send data back to ESP8266
            client_socket.send(str(reset).encode())
            sendmsg ("reset msg sent")
            
        
        elif request.startswith("SEND TO SERVER,"):
            db = pymysql.connect(
            host="localhost",
            user="root",
            password="IAMACODER78",
            database="quiz"
            )
            cursor=db.cursor()
            data=request.split(",")
            l2=[]
            for i in range(1,5):
                l2.append(data[i].strip())
            cursor.execute(f"INSERT INTO quiz_entries VALUES ({int(l2[0])}, \"{l2[1]}\",\"{l2[2]}\",\"\",{float(l2[3])})")
            sendmsg ("data inserted successfully")
            db.commit()
            db.close()
        client_socket.close()
        sendmsg (f"closed connection from {addr}")


def start():
    try:
        global addr,server,text_output,running,client
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 8080))  # Replace with host IP and port if necessary
        server.listen(10)
        text_output=ScrolledText(win, wrap=WORD, width=80, height=20)
        text_output.place(x=50,y=100)
        sendmsg("Server is listening...")
        running=True

        while running:
            client, addr = server.accept()
            thread=threading.Thread(target=handle_client, args=(client,))
            thread.start()
            sendmsg(f"Accepted connection from {addr}")
    except OSError:
        print("server closed os error in start function")
        

def end():
    try:   
        global running
        running=False
        client.close()
        server.close()
    except OSError:
        print("server closed os errorin end function")
    except NameError:
        print("client not found in end function")
    finally:
        text_output.destroy()


def broadcast():
    local_ip = socket.gethostbyname(socket.gethostname())
    message = f"{local_ip}"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.2)

    broadcast_ip = "255.255.255.255"  
    port = 12345                     
    print(f"Broadcasting IP: {message}")
    
    sock.sendto(message.encode(), (broadcast_ip, port))
    sock.close()
    start()

win=Tk()
win.geometry("800x600")
win.config(bg="orange")
StartServer=Button(win,text="START",font=("Arial",20),padx=10,pady=10,command=lambda: threading.Thread(target=start, daemon=True).start(),fg="red",bg="yellow")
StartServer.place(x=10,y=0)  
EndServer=Button(win,text="END",font=("Arial",20),padx=10,pady=10,command=lambda: end(),fg="white",bg="red")
EndServer.place(x=650,y=0)
BroadcastIP=Button(win,text="Broadcast IP",font=("Arial",20),padx=10,pady=10,command=lambda: threading.Thread(target=broadcast, daemon=True).start(),fg="red",bg="lime")
BroadcastIP.place(x=300,y=250)  

win.mainloop()