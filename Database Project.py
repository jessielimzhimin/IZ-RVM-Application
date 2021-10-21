import tkinter as tk
import datetime
import time
from tkinter import ttk
from tkinter import messagebox
import pymysql


FONT = 'Times New Roman'


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Creating Window
        window = tk.Frame(self)
        window.pack()

        window.grid_columnconfigure(0, minsize=850)
        window.grid_rowconfigure(0, minsize=650)

        # Creating Title and Icon
        icon = tk.PhotoImage(file='iz logo.png')
        self.iconphoto(True, icon)
        self.title("Initiative Z RVM Application")
        self.frames = {}

        for F in (Startpage, page1, page2):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Startpage)

    def show_frame(self, page):
            frame = self.frames[page]
            frame.tkraise()


class Startpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # IZ photo
        photo = tk.PhotoImage(file='iz logo biggg.PNG')
        photo_label = tk.Label(self,image=photo)
        photo_label.image = photo
        photo_label.place(x=-350, y=0)

        # Border
        border_frame=tk.Frame(self, height=200, width=500, bg='#d7ded9', bd=1, relief='ridge')
        border_frame.place(x=180, y=220)

        # label
        welcome_label = tk.Label(self, text="Welcome to IZ Reverse Vending Machine Application",
                               font=(FONT, 25, 'bold'), fg='black', bg='white')
        welcome_label.pack()

        username_label = tk.Label(self, text="Student ID:", font=(FONT, 14),bg='#d7ded9')
        username_label.place(x=200, y=240)
        #password_label = tk.Label(self, text="Password:", font=(FONT,14), bg='#d7ded9')
        #password_label.place(x=200, y=300)

        # Student ID and password entry
        username_entry_var = tk.StringVar()
        username_entry = tk.Entry(self, width=30, font=(FONT, 12),
                               textvariable=username_entry_var)
        username_entry.place(x=305, y=242)
        #password_entry = tk.Entry(self, width=30, font=(FONT,12), show='*')
        #password_entry.place(x=305, y=302)

        # Login FUnction
        def login():
            if username_entry.get()=="":
                messagebox.showerror("Error","PLease enter your student ID")
            else:
                try:
                    connect = pymysql.connect(host="localhost", user="rvmadmin", password="password", database="rvmdb")
                    cursor = connect.cursor()
                    cursor.execute('select * from studentTable where student_id=%s',username_entry.get())
                    row = cursor.fetchone()
                    if row == None:
                        messagebox.showerror("Error", "Invalid Student ID")
                    else:
                        controller.show_frame(page1)
                        connect.close()
                except Exception as es:
                        messagebox.showerror("Error",f"Error due to : {str(es)}")
                    
            
            

        # Sign Up Function
        def register():
            window1 = tk.Tk()
            window1.geometry("400x200")
            window1.title("Sign Up")
            window1.resizable(0,0)

            signup_label = tk.Label(window1, text="Please enter your name as per your Student ID.",
                                    font=(FONT,14))
            signup_label.place(x=10, y=10)

            label1 = tk.Label(window1, text="Name: ", font=(FONT,14),)
            label1.place(x=10, y=50)
            label1_entry = tk.Entry(window1, width=30, font=(FONT,12))
            label1_entry.place(x=130, y=50)

            label2 = tk.Label(window1, text="Student ID:", font=(FONT, 14))
            label2.place(x=10, y=85)
            label2_entry = tk.Entry(window1, width=30, font=(FONT, 12),)
            label2_entry.place(x=130, y=85)
            
            def signup_db():
                student_NAME = label1_entry.get()
                student_ID = label2_entry.get()
                
                if student_NAME=="" or student_ID=="":
                    messagebox.showerror("Error","All fields are required")
                else:
                    try:
                        connect=pymysql.connect(host="localhost", user="rvmadmin", password="password", database="rvmdb")
                        cursor=connect.cursor()
                        cursor.execute("insert into studentTable values('"+ student_ID +"','"+ student_NAME +"')")
                        connect.commit()
                        connect.close()

                        messagebox.showinfo("Success","Register Successful!")
                    except Exception as es:
                        messagebox.showerror("Error",f"Error due to:{str(es)}")
                        
   
            signup_button = tk.Button(window1, text="Sign Up", font=(FONT, 14),
                                      command=signup_db)
            signup_button.place(x=300, y=150)
            window1.mainloop()

        # Button
        submit_button = tk.Button(self, text="Submit", font=(FONT, 13),
                                command=login)
        submit_button.place(x=585, y=365)
        register_button = tk.Button(self, text="Sign Up", font=(FONT, 13), command=register)
        register_button.place(x=480, y=365)




class page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        username_label2 = tk.Label(self, text="Username2:", font=(FONT, 12))
        username_label2.place(x=190, y=350)

        submit_button = tk.Button(self, text="Next", font=(FONT, 14),
                                  command=lambda: controller.show_frame(page2))
        submit_button.place(x=490, y=348)

        submit_button2 = tk.Button(self, text="Back", font=(FONT, 14),
                                  command=lambda: controller.show_frame(Startpage))
        submit_button2.place(x=490, y=400)


class page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        username_label3 = tk.Label(self, text="Username3:", font=(FONT, 12))
        username_label3.place(x=190, y=350)

        submit_button = tk.Button(self, text="Back", font=(FONT, 14),
                                  command=lambda: controller.show_frame(page1))
        submit_button.place(x=490, y=348)

        submit_button2 = tk.Button(self, text="Homepage", font=(FONT, 14),
                                  command=lambda: controller.show_frame(Startpage))
        submit_button2.place(x=490, y=400)


app = Application()
app.mainloop()
