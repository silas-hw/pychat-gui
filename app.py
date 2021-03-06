import client
import threading
import sys
import time
import random
import pickle
import emoji
import json
import os

import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from client import DISCONNECT_MESSAGE
from classes import User, Message

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

        if not os.path.isfile(".\\user\\data.txt"):
            self.showPopup()

    input = ObjectProperty(None)
    output = ObjectProperty(None)

    @property
    def maxLines(self):
        return self.height/23

    @property
    def user(self):
        try:
            with open(".\\user\\data.txt", "r") as f:
                username = f.read()
        except FileNotFoundError:
            username = "Caitlyn"
            
        return User(username, USERCOLOR)

    def setUsername(self, name: str):
        with open(".\\user\\data.txt", "w") as f:
            userData = f.write(name)

    def delLines(self):
        if len(self.output.text.splitlines()) >= self.maxLines:
            self.output.text = self.output.text.split('\n', 2)[2]

    def on_resize(self, window, width, height):
        self.delLines()

    def closeApp(self, *largs, **kwargs):
        msg = Message("!close", self.user)
        client.send(msg)

    def btn(self):
        if self.input.text:
            msg = Message(self.input.text, self.user)
            client.send(msg)
            self.input.text = ""

    def receiveMsg(self):
        while True:
            msg = client.receive()

            if msg == 0:
                self.output.text += "SERVER CONNECTION CLOSED"
                self.delLines()

                #stop user from sending messages
                self.input.text = ""
                self.input.disabled = True
                return

            if not isinstance(msg, str):
                if msg.content == DISCONNECT_MESSAGE:
                    return
                
                self.output.text += emoji.emojize(f"[color={msg.user.colour}]{msg.user.name}[/color]: {msg.content}\n", use_aliases=True)
                self.delLines()

    def showPopup(self):
        self.show = PopupWindow()
        self.popupWindow = Popup(title="Username", content=self.show, size_hint=(None, None), size=(400, 200))
        self.popupWindow.open()

    def hidePopup(self):
        if self.show.username:
            self.setUsername(self.show.username)
            self.popupWindow.dismiss()

class ChatApp(MDApp):

    def build(self):
        self.mainLayout = MainLayout()
        return self.mainLayout
    
if __name__ == '__main__':
    ChatApp().run()