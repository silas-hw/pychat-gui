class User():
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

class Message():
    def __init__(self, content, user):
        self.content = content
        self.user = user  