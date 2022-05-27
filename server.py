from tkinter import *
import socket
import random
import threading



def start_server():
    global tcpSocket
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.bind(("",8000))
    threading._start_new_thread(start_game, ())
    start_btn["state"] = "disable"

def stop_server():
    main_win.destroy()


def new_equation():
    question = str(random.randint(1,9)) #equation start with number
    operands = random.randint(2,4)
    operators =  ['+', '-', '*', '/']
    for i in range(operands-1):
        operator = random.choice(operators)
        operand = str(random.randint(1, 9))
        question += f" {operator} {operand}"
    return question

def start_game():
    count = 0
    while True:
        tcpSocket.listen(1)
        (client, (ip, port)) = tcpSocket.accept()

        print("connect")
        canvas_main.create_text(80, 100+count*25, text=f"client connected", fill="#BDF2F2",
                    font="Times 15 bold",justify="center",anchor=N)
       

        no = 1
        print("question number", no)

        data = new_equation()
        canvas_main.create_text(80, 100+(no)*25, text=f"Q.{no} answer is {round(eval(data),2)}", fill="#BDF2F2",
                    font="Times 15 bold",justify="center",anchor=N)
        client.send(data.encode()+str(no).encode())
        
        ans = (client.recv(2048).decode())
    
        
        if eval(ans) == round(eval(data),2):
            client.send("correct".encode())
        else :
            client.send("wrong".encode())
        
        print(client.recv(2048).decode())
                  
        while no < 5:
            
            no += 1
            print("question number", no)
            data = new_equation()
            client.send(data.encode()+str(no).encode())

            canvas_main.create_text(80, 100+(no)*25, text=f"Q.{no} answer is {round(eval(data),2)}", fill="#BDF2F2",
                    font="Times 15 bold",justify="center",anchor=N)

            ans = (client.recv(2048).decode())


            if eval(ans) == round(eval(data),2):
                client.send("correct".encode())
            else :
                client.send("wrong".encode())
            
            print(client.recv(2048).decode())

        count += 1

def hover_in(e):                                                         
    e.widget["background"] = "#85B4F2"


def hover_out(e):                                                         
    e.widget["background"] = "#7EA5F2"


main_win = Tk()
main_win.geometry("350x600")
main_win.resizable(0, 0)
main_win.title("Server Monitor")

canvas_main = Canvas(main_win, width=350, height=600,bg="black")
canvas_main.pack(fill="both", expand=True)
canvas_main.create_text(150, 15, text="Server", fill="#BDF2F2",
                        font="Times 18 bold",justify="center",anchor="n")
start_btn = Button(canvas_main,text="start",command=start_server, bg="#7EA5F2", relief="groove",
                activebackground="#85B4F2")
stop_btn = Button(canvas_main,text="stop",command=stop_server, bg="#7EA5F2", relief="groove",
                activebackground="#85B4F2")


start_btn.place(x=125,y=50,anchor=NE)
start_btn.bind("<Enter>", hover_in)
start_btn.bind("<Leave>", hover_out)

stop_btn.place(x=175,y=50,anchor=NW)
stop_btn.bind("<Enter>", hover_in)
stop_btn.bind("<Leave>", hover_out)

main_win.mainloop()