from distutils.log import error
from sqlite3 import connect
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
        database.read(database)
        return keyboard

    def start(self):
        print("Student ID:", self.studentID.text)
        self.studentID.text = ""

class promptPage(Screen):
    pass

class loadingPage(Screen):
    pass

class summaryPage(Screen):
    pass

class Manager(ScreenManager):
    # main = ObjectProperty(None)
    # prompt = ObjectProperty(None)
    # loading = ObjectProperty(None)
    # summary = ObjectProperty(None)
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

    def read(self):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "SELECT * FROM studentid"
            cursor.execute(cmd)
            result = cursor.fetchall()
            print(result)
    
    def insert(self):
        connection = self.connection()
        with connection.cursor() as cursor:
            cmd = "INSERT INTO studentid (studentID, points, items) VALUES (%s, %s, %s)"
            cursor.execute(cmd, (1001, 15, 11))
            connection.commit()


class myApp(App):
    def build(self):
        return loadingPage()

if __name__ == "__main__":
    myApp().run()
