from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Login')
root.geometry('300x200')  
root.configure(bg="#fff")

def signin():
    username=user.get()
    password=code.get()

    if username== 'admin' and password=='1234':
        screen=Toplevel(root)
        screen.title("app")
        screen.geometry('925x500+300+200')
        screen.config(bg="white")

        label(screen,text="Hello everone!",bg='#fff',font=('calibri(body)')).pack(expand=True)

        screen.mainloop()

    elif username!='admin' and password!='1234':
        messagebox.showerror("Invalid","Invalid username and password")
    
    elif password!="1234":
        messagebox.showerror("Invalid","Invalid password")
    
    elif username!="admin":
        messagebox.showerror("Invalid","Invalid username")


img= PhotoImage(file='login.png')
Label(root,image=img,bg="white").place(x=60,y=100)

frame=Frame(root,width=700,height=500,bg="white")
frame.place(x=580,y=20)

heading=Label(frame,text='sign in',fg='#57a1f8',bg='white',font=('microsoft Yahei UI light', 23,'bold'))
heading.place(x=150,y=10)
###_________________________________________________________________________________________________________

def on_pass_enter(event):
    e = event.widget
    
    if e.get() == 'username':
        e.delete(0, 'end')
        e.config(show='', fg='black')

def on_pass_leave(event):
    e = event.widget
    
    if not e.get():
        e.config(show='', fg='grey')
        e.insert(0, 'username')



user=Entry(frame,width=25,fg='black',border=2,bg='white',font=('microsoft Yahei UI light', 23,'bold'))
user.place(x=20,y=80)
user.insert(0,'username')
user.bind('<FocusIn>', on_pass_enter)
user.bind('<FocusOut>', on_pass_leave)



Frame(frame,width=200,height=0,bg='black').place(x=180,y=120)

###_________________________________________________________________________________________________________

def on_pass_enter(event):
    e = event.widget
    # If the placeholder text is showing, clear it
    if e.get() == 'password':
        e.delete(0, 'end')
        e.config(show='*', fg='black')

def on_pass_leave(event):
    e = event.widget
    # If the user left the field empty, restore placeholder
    if not e.get():
        e.config(show='', fg='grey')
        e.insert(0, 'password')

code=Entry(frame,width=25,fg='black',border=2,bg='white',font=('microsoft Yahei UI light', 23,'bold'))
code.place(x=20,y=160)
code.insert(0,'password')

code.bind('<FocusIn>', on_pass_enter)
code.bind('<FocusOut>', on_pass_leave)

Frame(frame,width=200,height=0,bg='black').place(x=180,y=200)

#######################################################################



Button(frame,width=50,pady=9, text='sign in',bg='#57a1f8',fg='white',border=0, command=signin).place(x=70,y=250)
label=Label(frame,text="don't have any account?",fg='black',bg='white',font=('microsoft Yahei UI light',9))
label.place(x=75,y=290)

sign_up=Button(frame,width=6,text='sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8')
sign_up.place(x=220,y=290)


root.mainloop()
