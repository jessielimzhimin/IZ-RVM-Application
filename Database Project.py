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

        for F in (SelectionPage, page1, page2):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SelectionPage)

    def show_frame(self, page):
            frame = self.frames[page]
            frame.tkraise()

class SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.button_clicks = 0

        # Machine activation
        def start_machine():
            select_button['state'] = 'disabled'
            select_button.update()
            time.sleep(2)
            self.button_clicks += 1
            select_button ['text'] = "Total Clciks: " + str(self.button_clicks)
            #top = tk.Toplevel()
            #top.title('DONE')
            #tk.Message(top, text="loading",padx=20,pady=20).pack()
            #top.after(5000, top.destroy)
            select_button.config(state='normal')
            select_button.update()
            return int(self.button_clicks)

        

        # Label
        select_label=tk.Label(self, text="RVM application", font=(FONT,12))
        select_label.pack()

        # Button
        select_button=tk.Button(self, text="Start", font=(FONT, 13), command=start_machine)
        select_button.place(x=200, y=150)
        username_label = tk.Label(self, text="Student ID:", font=(FONT, 14),bg='#d7ded9')
        username_label.place(x=200, y=240)
        #password_label = tk.Label(self, text="Password:", font=(FONT,14), bg='#d7ded9')
        #password_label.place(x=200, y=300)

        # Student ID and password entry
        username_entry = tk.Entry(self, width=30, font=(FONT, 12))
        username_entry.place(x=305, y=242)

        # Login FUnction
        def login():
            point = str(self.button_clicks)
            student_ID = username_entry.get()
            if username_entry.get()=="":
                messagebox.showerror("Error","PLease enter your student ID")
            else:
                try:
                    connect = pymysql.connect(host="localhost", user="rvmadmin", password="password", database="rvmdb") #connect to database and update database
                    cursor = connect.cursor()
                    sql_update = """Update studentTable set points = points + %s where student_id = %s"""
                    data_update = (point, student_ID)
                    cursor.execute(sql_update, data_update)
                    connect.commit() 
                    messagebox.showinfo("Success", "SUccessfully inserted")
                except Exception as es:
                    messagebox.showerror("Error",f"Error due to:{str(es)}")
                  

                        
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
            
            def signup_db(): #login to database and register new students
                student_NAME = label1_entry.get()
                student_ID = label2_entry.get()
                points = str(0)
                
                if student_NAME=="" or student_ID=="":
                    messagebox.showerror("Error","All fields are required")
                else:
                    try:
                        connect=pymysql.connect(host="localhost", user="rvmadmin", password="password", database="rvmdb")
                        cursor=connect.cursor()
                        cursor.execute("insert into studentTable values('"+ student_ID +"','"+ student_NAME +"','"+ points +"')")
                        row = cursor.fetchone()
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

 # page1 and page2 class are not used atm
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
