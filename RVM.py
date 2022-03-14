from distutils.log import error
from sqlite3 import connect
from tkinter import Button
from unicodedata import name
from kivy.app import App
from kivy.app import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.lang import Builder
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

# app.root.current = "prompt"
#                     root.manager.transition.direction = "left"

# registerPage Class******************************************************************************

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

    def mainpage(self):
        database.create(database, 
                        self.ids.studentID.text, 
                        self.ids.studentName.text, 
                        self.ids.studentProgramme.text, 
                        self.ids.studentPhone.text, 
                        self.ids.studentEmail.text)
        App.get_running_app().root.transition.direction = "right"
        App.get_running_app().root.current = "main"
        
# end of registerPage Class*************************************************************************
        
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
                             password='Mysql0644961-',
                             database='RVM',
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

kv = Builder.load_file("my.kv")

sm = WindowManager()
# registerPage is added to allow navigation to registerPage when register button is clicked
screens = [mainPage(name="main"), registerPage(name="register"), promptPage(name="prompt"), loadingPage(name="loading")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

class myApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    myApp().run()
