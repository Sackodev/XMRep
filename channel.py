from note import Note

class Channel(object):
    def __init__(self):
        self.notes = []

    def addNote(self, type):
        self.notes.append(Note(type))
