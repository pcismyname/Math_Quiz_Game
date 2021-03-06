from tkinter import *
import socket

  
def exit_b(window):
    window.destroy()
    main_win.deiconify()
    button_new_game["state"] = "normal"
    button_score["state"] = "normal"


def new_game():

    def reset():
        game_win.destroy()
        login()

    def finish(sum_score):
        place_score = user_name+"  "+sum_score+"\n\n"
        f = open("scoreBoard.txt", "a")
        f.write(place_score)
        f.close()

    def next():
        button_next.place_forget()
        canvas_game.itemconfig(server_result, text="")
        button_submit.place(x=400, y=400, anchor="center")
        equation = tcpSocket.recv(2048).decode()
        canvas_game.itemconfig(equation_server, text = equation[:-1])
        canvas_game.itemconfig(number, text=("No: " + equation[len(equation)-1]))

        
        
        


    def send_to_server():
        user_data = user_entry.get()
        tcpSocket.send(user_data.encode())
        print(user_data)
        user_entry.delete(0, END)
        global result
        result = tcpSocket.recv(2048).decode()

        if result.isalpha():
            canvas_game.itemconfig(server_result,text = result)
            button_submit.place_forget()  
            button_next.place(x=400, y=400, anchor=CENTER)
        else :
            canvas_game.itemconfig(server_result,text = result[1:])
            canvas_game.itemconfig(equation_server, text = "score : "+result[0])
            button_submit.place_forget()
            new_btn.place(x=400, y=400, anchor=CENTER)
            finish(result[0])
        
        tcpSocket.send("client receive".encode())       

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    tcpSocket.connect(("127.0.0.1", 8000))
    equation = tcpSocket.recv(2048).decode()[:-1]

    button_new_game["state"] = "disable"
    button_score["state"] = "disable"

    game_win = Toplevel(main_win)
    game_win.geometry("800x600")
    game_win.resizable(0, 0)
    game_win.title("Game")
    canvas_game = Canvas(game_win, width=640, height=480)
    canvas_game.pack(fill="both", expand=True)
    canvas_game.create_image(0,0, image=bg_main, anchor="nw")
    canvas_game.create_rectangle(50, 120, 750, 450, fill="#2881CE", outline='#7e3a95')

    equation_server = canvas_game.create_text(400, 180, text=equation, fill="white",font="Times 34", anchor="n", justify="center")

    number = canvas_game.create_text(60, 130, text="No: 1", fill="white",                       
                                      font="Times 18", justify="center", anchor="nw")
    canvas_game.create_text(60, 160,text=("Player: "+user_name), fill="white",
            font="Times 18", anchor="nw")
  
    
    user_entry = Entry(game_win, width=4, font="Times 26 bold", justify="center", bg="#BDF2F2")
    canvas_game.create_window(400, 320,  window=user_entry)

    button_submit = Button(game_win, text="SUBMIT", height=2, width=26, bg="#7EA5F2", relief="raised",  
                      activebackground="#85B4F2", state=NORMAL, font="Times 16", command=send_to_server)

    button_next = Button(game_win, text="NEXT", height=2, width=26, bg="#7EA5F2", relief="raised",  
                      activebackground="#85B4F2", state=NORMAL, font="Times 16", command=next)

    new_btn =  Button(game_win, text="FINISHED", height=2, width=26, bg="#7EA5F2", relief="raised",  
                      activebackground="#85B4F2", state=NORMAL, font="Times 16", command=reset) 

    

    server_result = canvas_game.create_text(400, 250, text="", fill="white",                       
                                      font="Times 30", justify=CENTER, anchor=N)

    button_submit.place(x=400, y=400, anchor="center")
    button_submit.bind("<Enter>", hover_in)
    button_submit.bind("<Leave>", hover_out)

    button_exit_score = Button(game_win, text="EXIT", height=2, width=26, bg="#7EA5F2", relief="raised",    # Exit Button
                          activebackground="#85B4F2", command=lambda:exit_b(game_win), state=NORMAL, font="Times 16")

    button_exit_score.place(x=400, y=530, anchor="center")
    button_exit_score.bind("<Enter>", hover_in)
    button_exit_score.bind("<Leave>", hover_out)





def score_board():

    main_win.iconify()
    f = open("scoreBoard.txt", "r")
    scoreList = f.read()
    f.close()
    score_window = Toplevel(main_win)
    score_window.title("Score")
    score_window.geometry("480x640")
    score_window.resizable(0, 0)
    canvas_score = Canvas(score_window, width=480, height=640)
    canvas_score.pack(fill="both",expand=True)
    canvas_score.create_image(0, 0, image=bg_score, anchor="nw")

    canvas_score.create_text(240, 100, text="SCORE\nBOARD",
                             fill="#7EA5F2", font="Times 30 bold",
                             justify="center")
    canvas_score.create_text(240, 240, text=scoreList,
                             fill="white", font="Forte 18",
                             justify="center", anchor="n")
    button_exit_score = Button(score_window, text="EXIT", height=2, width=26, bg="#7EA5F2",
                          relief="raised", activebackground="#85B4F2",
                          command=lambda: exit_b(score_window), state=NORMAL, font="Times 16")

    button_exit_score.place(x=240, y=580, anchor="center")
    button_exit_score.bind("<Enter>", hover_in)
    button_exit_score.bind("<Leave>", hover_out)


def hover_in(e):                                                         
    e.widget["background"] = "#85B4F2"


def hover_out(e):                                                         
    e.widget["background"] = "#7EA5F2"


def login():
    main_win.iconify()

    def start_b():
        global user_name
        user_name = enter_name.get()
        print(user_name)
        login_window.destroy()
        new_game()

    login_window = Toplevel(main_win)
    login_window.title("LOGIN")
    login_window.geometry("400x250")
    login_window.resizable(0, 0)
    canvas_login = Canvas(login_window, width=400, height=250)
    canvas_login.pack(fill="both", expand=True)
    canvas_login.create_image(0, 0, image=bg_main, anchor="nw")

    canvas_login.create_text(200, 40, text="Enter Your Name",
                             fill="#BDF2F2", font="Times 30 bold",
                             justify="center")
    enter_name = Entry(canvas_login, width=16, font="Times 26 bold", justify="center", bg="#BDF2F2")
    canvas_login.create_window(200, 100, window=enter_name)

    b_start = Button(login_window, text="START", height=1, width=20, bg="#7EA5F2", relief="raised",  
                     activebackground="#85B4F2", command=start_b, state=NORMAL, font="Times 16")
    button_exit_login = Button(login_window, text="EXIT", height=1, width=20, bg="#7EA5F2", relief="raised",  
                          activebackground="#7e3a95", command=lambda: exit_b(login_window),
                          state=NORMAL, font="Times 16")
    b_start.place(x=200, y=170, anchor="center")
    b_start.bind("<Enter>", hover_in)
    b_start.bind("<Leave>", hover_out)

    button_exit_login.place(x=200, y=220, anchor="center")
    button_exit_login.bind("<Enter>", hover_in)
    button_exit_login.bind("<Leave>", hover_out)


main_win = Tk()
main_win.geometry("640x480")
main_win.resizable(0, 0)
main_win.title("Guess Number")


user_name = ""
bg_main = PhotoImage(file="img/bg-math.png")
bg_score = PhotoImage(file="img/bg-score.png")

canvas_main = Canvas(main_win, width=640, height=480)
canvas_main.pack(fill="both", expand=True)
canvas_main.create_image(0,0, image=bg_main,anchor="nw")

canvas_main.create_text(320, 60, text="Math Quiz", fill="#BDF2F2",
                        font="Times 38 bold",justify="center",anchor="n")
button_new_game = Button(canvas_main, text="NEW GAME", height=2, width=26, bg="#7EA5F2", relief="groove",
                    activebackground="#85B4F2", command=login, state=NORMAL, font="Times 16 ")
button_score = Button(canvas_main, text="SCORE", height=2, width=26, bg="#7EA5F2", relief="groove",
                 activebackground="#85B4F2", command=score_board, state=NORMAL, font="Times 16")
button_exit = Button(canvas_main, text="EXIT", height=2, width=26, bg="#7EA5F2", relief="groove",
                activebackground="#85B4F2", command=main_win.destroy, state=NORMAL, font="Times 16")


button_new_game.place(x=320, y=220, anchor=CENTER)
button_new_game.bind("<Enter>", hover_in)
button_new_game.bind("<Leave>", hover_out)

button_score.place(x=320, y=290, anchor=CENTER)
button_score.bind("<Enter>", hover_in)
button_score.bind("<Leave>", hover_out)

button_exit.place(x=320, y=380, anchor=CENTER)         
button_exit.bind("<Enter>", hover_in)
button_exit.bind("<Leave>", hover_out)

main_win.mainloop()