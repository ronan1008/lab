import datetime
last_id = 0
class Note:
    def __init__(self, memo, tags =''):
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global last_id
        last_id += 1
        self.id = last_id
    def match(self, filter):
        return filter in self.memo or filter in self.tags

class Notebook:
    def __init__(self):
        self.notes=[]
    def new_note(self, memo, tags=''):
        self.notes.append(Note(memo,tags))

    def _find_note(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def modify_memo(self, note_id, memo):
        self._find_note(note_id).memo = memo

    def search(self, filter):
        return [note for note in self.notes if note.match(filter)]

if __name__ == '__main__':
    # n1 = Note("hello first")
    # n2 = Note("hello again")

    # print(n1.id, n2.id)

    # print(n1.match('hello'), n2.match('second'))

    n = Notebook()
    n.new_note("hello world")
    n.new_note("hello again")
    print(n.notes)
    print(n.notes[0].id, n.notes[1].id, n.notes[0].memo)
    print(n.search("hello"),n.search("world"))
    n.modify_memo(1, "hi world")
    print(n.notes[0].memo)