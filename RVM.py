from pymysql import *
from distutils.log import error
from sqlite3 import connect
from tkinter import Button
from unicodedata import name
from kivy.app import App
from kivy.app import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.lang import Builder
import openpyxl
import pandas.io.sql as sql
import pymysql.cursors
Config.set('kivy', 'keyboard_mode', 'systemanddock')


class mainPage(Screen):
    studentID = ObjectProperty(None)
    studentELE = ObjectProperty(None)

    def keyboard(self):
        keyboard = VKeyboard()
        # database.insert(database)
        # database.alltables(database)
        # database.read(database)
        return keyboard

    def start(self):
        # if len(self.ids.studentID.text) != 10 and type(self.ids)
        if len(self.ids.studentID.text) != 10 or len(self.ids.studentELE.text) != 4 :
            self.ids.startbtn.disabled = True
        else:
            try:
                type_id = int(self.ids.studentID.text)
                type_ele = int(self.ids.studentELE.text)
                self.ids.startbtn.disabled =False
            except Exception as es:
                self.ids.startbtn.disabled = True
                
        print(self.ids.studentID.text)
        print("Student ID:", self.ids.studentID.text)

    # to register new user into db
    def register(self):
        self.ids.studentID.text = ""
        self.ids.studentELE.text = ""
        App.get_running_app().root.transition.direction = "left"
        App.get_running_app().root.current = "register"
        
    def integer(self):
        result = database.alltables(database)
        array = []
        for i in result:
            array.append(i['id'])
        if int(self.ids.studentID.text) in array:
            database.insert_ELE(database, self.ids.studentELE.text, self.ids.studentID.text)
            App.get_running_app().root.transition.direction = "left"
            App.get_running_app().root.current = "prompt"
        else:
            App.get_running_app().root.transition.direction = "left"
            App.get_running_app().root.current = "register"

    
    # go to admin page to export sql data
    def admin_btn(self):
        App.get_running_app().root.transition.direction = "left"
        App.get_running_app().root.current = "admin"
        
# app.root.current = "prompt"
#                     root.manager.transition.direction = "left"



class AdminPage(Screen):
    admin_username = ObjectProperty(None)
    admin_password = ObjectProperty(None)

    def keyboard(self):
        keyboard = VKeyboard()
        return keyboard
    
    # Text Verification
    def text_check(self):
        username = self.ids.admin_username.text
        password = self.ids.admin_password.text

        if username =="" or password =="":
            self.ids.downloadbtn.disabled = True
        else:
            self.ids.downloadbtn.disabled = False

    # to unsuccessful popup
    def invalid_msg(self):
        popup = FailedPopup()
        popup.open()

    # to success popup
    def success_msg(self):
        popup = SuccessPopup()
        popup.open()
        
    def back(self):
        self.ids.admin_username.text = ""
        self.ids.admin_password.text = ""
        App.get_running_app().root.transition.direction = "right"
        App.get_running_app().root.current = "main"

    # export sql data into spreadsheet, will pop up unsuccessful msg if incorrect username and password else pop up successful msg
    def downloadbtn(self):
        result = database.download(database, self.ids.admin_username.text, self.ids.admin_password.text)
        self.ids.admin_username.text = ""
        self.ids.admin_password.text = ""
        if result:
                self.success_msg()
                App.get_running_app().root.transition.direction = "right"
                App.get_running_app().root.current = "main"
        else:
            self.invalid_msg()


class FailedPopup(Popup):
    pass

class SuccessPopup(Popup):
    pass

class registerPage(Screen):
    studentName = ObjectProperty(None)
    studentID = ObjectProperty(None)
    studentProgramme= ObjectProperty(None)
    studentEmail = ObjectProperty(None)
    studentPhone = ObjectProperty(None)
    
    def keyboard(self):
        keyboard = VKeyboard()
        # database.insert(database)
        # database.alltables(database)
        # database.read(database)
        return keyboard
    
    def text_check(self):
        Id = self.ids.studentID.text
        name = self.ids.studentName.text
        programme = self.ids.studentProgramme.text
        email = self.ids.studentEmail.text
        phone = self.ids.studentPhone.text
        bool_name = any([char.isdigit() for char in name])
        bool_programme = any([char.isdigit() for char in programme])

        if Id == "" and name == "" and programme == "" and email =="" and phone=="" or ((bool_name == True) or (bool_programme == True)):
            self.ids.completebtn.disabled = True
        else:
            try:
                type_id = int(Id)
                type_phone = int(phone)
                self.ids.completebtn.disabled = False
            except Exception as es:
                self.ids.completebtn.disabled = True
                
    def mainpage(self):
        database.create(database, 
                        self.ids.studentID.text, 
                        self.ids.studentName.text, 
                        self.ids.studentProgramme.text, 
                        self.ids.studentPhone.text, 
                        self.ids.studentEmail.text)
        self.ids.studentID.text = ""
        self.ids.studentName.text = ""
        self.ids.studentProgramme.text = "" 
        self.ids.studentPhone.text = ""
        self.ids.studentEmail.text =""
        App.get_running_app().root.transition.direction = "right"
        App.get_running_app().root.current = "main"
        
        
class promptPage(Screen):
    pass

class loadingPage(Screen):
    pass

class summaryPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class database():
    def connection():
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             database='rvm1',
                             cursorclass=pymysql.cursors.DictCursor)
        if connection:
            print("success")
            return connection
        else:
            print("error")
            raise Exception("error connecting to DB")

    def create(self, studentID, studentName, studentProgramme, studentPhone, studentEmail):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "INSERT INTO student (id, name, programme, contact, email) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(cmd, (studentID, studentName, studentProgramme, studentPhone, studentEmail))
            connection.commit()


    def read(self, studentID):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "SELECT * FROM  student"
            cursor.execute(cmd)
            result = cursor.fetchall()
            print(result)
            
    def insert_ELE(self, studentELE, studentID):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "UPDATE student set ele_code = concat("'"MPU"'", + %s) WHERE id = %s"
            cursor.execute(cmd, (studentELE, studentID))
            connection.commit()
    
    def insert_points(self):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd ="UPDATE student set points = points + %s WHERE id = %s"
            #"INSERT INTO student (studentID, points, items) VALUES (%s, %s, %s)"
            cursor.execute(cmd, (point, studentID))
            connection.commit()
            
    def insert(self):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "INSERT INTO studentid (studentID, points, items) VALUES (%s, %s, %s)"
            cursor.execute(cmd, (1001, 15, 11))
            connection.commit()

    def alltables(self):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "SELECT id FROM student"
            cursor.execute(cmd)
            result = cursor.fetchall()
            connection.commit()
            return result

    def download(self, username, password):
        try:
            connection = pymysql.connect(host='localhost',
                             user=username,
                             password=password,
                             database='rvm1',
                             cursorclass=pymysql.cursors.DictCursor)
            if connection:
                df = sql.read_sql('select * from student', connection)
                df.to_excel('rvm.xlsx')
                return True
        except Exception as es:
            return False
            

kv = Builder.load_file("my.kv.txt")

sm = WindowManager()
# registerPage is added to allow navigation to registerPage when register button is clicked
screens = [mainPage(name="main"), AdminPage(name="admin"), registerPage(name="register"), promptPage(name="prompt"), loadingPage(name="loading")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

class myApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    myApp().run()
