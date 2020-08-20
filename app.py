from kivy.uix.gridlayout import GridLayout
import client
import threading
import sys
import time
import random

import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from client import DISCONNECT_MESSAGE

USERCOLOR = random.choice(['#bf3d19', '#b543c4', '#50c443', '#43afc4', '#9bc443', '#c49343'])

Builder.load_file('design.kv')

class PopupWindow(GridLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    input = ObjectProperty(None)

    @property
    def username(self):
        return self.input.text

class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        receiveThread = threading.Thread(target=self.receiveMsg)
        receiveThread.start()

        Window.bind(on_resize=self.on_resize)
        Window.bind(on_request_close=self.closeApp)

        self.showPopup()

    USERNAME = ""
    input = ObjectProperty(None)
    output = ObjectProperty(None)

    @property
    def maxLines(self):
        return self.height/23

    def delLines(self):
        if len(self.output.text.splitlines()) >= self.maxLines:
            self.output.text = self.output.text.split('\n', 2)[2]

    def on_resize(self, window, width, height):
        self.delLines()


    def closeApp(self, *largs, **kwargs):
        client.send("!close")

    def btn(self):
        if self.input.text:
            client.send(f"[color={USERCOLOR}]{self.USERNAME}[/color]: {self.input.text}")
            self.input.text = ""

    def receiveMsg(self):
        while True:
            msg = client.receive()

            if msg == DISCONNECT_MESSAGE:
                print("Thread ended")
                return
            
            self.output.text += f"{msg}\n"
            self.delLines()

    def showPopup(self):
        self.show = PopupWindow()

        self.popupWindow = Popup(title="Username", content=self.show, size_hint=(None, None), size=(400, 200))
        self.popupWindow.open()

    def hidePopup(self):
        if self.show.username:
            self.USERNAME = self.show.username
            self.popupWindow.dismiss()


        
class ChatApp(MDApp):

    def build(self):
        self.mainLayout = MainLayout()
        return self.mainLayout
    
if __name__ == '__main__':
    ChatApp().run()