class Room:
    def __init__(self, rid ):
        self.people={}
        self.roomid=rid
        self.msgs=[]
        self.sidlst=[]
    def addPerson(self,person):
        self.people[person.pid]=person
    def addMsg(self,msg):
        self.msgs.append(msg)
    def addSID(self,sid):
        if not sid in self.sidlst:
            self.sidlst.append(sid)