import client
import threading
import sys
import time

import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from client import DISCONNECT_MESSAGE

USERNAME = input("Enter username to use: ")

Builder.load_file('design.kv')

class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        receiveThread = threading.Thread(target=self.receiveMsg)
        receiveThread.start()

        Window.bind(on_resize=self.on_resize)
        Window.bind(on_request_close=self.closeApp)

    
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
            client.send(f"{USERNAME} {self.input.text}")
            self.input.text = ""

    def receiveMsg(self):
        while True:
            msg = client.receive()

            if msg == DISCONNECT_MESSAGE:
                print("Thread ended")
                return
            
            self.output.text += f"{msg}\n"
            self.delLines()

class ChatApp(MDApp):

    def build(self):
        return MainLayout()
    
if __name__ == '__main__':
    ChatApp().run()