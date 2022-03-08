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

    def keyboard(self):
        keyboard = VKeyboard()
        # database.insert(database)
        # database.alltables(database)
        # database.read(database)
        return keyboard

    def start(self):
        # if len(self.ids.studentID.text) != 10 and type(self.ids)
        if len(self.ids.studentID.text) != 10 and type(int(self.ids.studentID.text)) != "int":
            self.ids.startbtn.disabled = True
        else:
            self.ids.startbtn.disabled = False
        print(self.ids.studentID.text)
        print("Student ID:", self.ids.studentID.text)

    
    def integer(self):
        result = database.alltables(database)
        array = []
        for i in result:
            array.append(i["Tables_in_rvm"])
        if "'" + self.ids.studentID.text + "'" in array:
            App.get_running_app().root.transition.direction = "left"
            App.get_running_app().root.current = "prompt"
        else:
            database.create(database, self.ids.studentID.text)
            App.get_running_app().root.transition.direction = "left"
            App.get_running_app().root.current = "prompt"

# app.root.current = "prompt"
#                     root.manager.transition.direction = "left"

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

    def create(self, studentID):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "CREATE TABLE `%s` (itemName TEXT(30), category TEXT(30), points INT(3))"
            cursor.execute(cmd, str(studentID))


    def read(self, studentID):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "SELECT * FROM  `%s`"
            cursor.execute(cmd, studentID)
            result = cursor.fetchall()
            print(result)
    
    def insert(self):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "INSERT INTO studentid (studentID, points, items) VALUES (%s, %s, %s)"
            cursor.execute(cmd, (1001, 15, 11))
            connection.commit()

    def alltables(self):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "SHOW TABLES"
            cursor.execute(cmd)
            result = cursor.fetchall()
            return result

kv = Builder.load_file("my.kv")

sm = WindowManager()
screens = [mainPage(name="main"), promptPage(name="prompt"), loadingPage(name="loading")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

class myApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    myApp().run()
