from flask import Flask, render_template, request,redirect,url_for
from random import choice
from flask_socketio import SocketIO,emit
import random
from msg import Msg
from person import Person
from room import Room

app=Flask(__name__)
app.secret_key = 'your secret'
app.config['SESSION_TYPE'] = 'filesystem'

socketio = SocketIO(app, cors_allowed_origins="*" )
roomidlst=[]
pidlst=[]
chats={}

def emitDataToRoom(msgname, roomid,data):
  room=chats[roomid]
  sids=room.sidlst
  for sid in sids:
    print("emiting to sid",sid)
    socketio.emit(msgname, data, room=sid)

def generateRID():
  letters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  roomid=""
  for i in range(6):
    roomid+=random.choice(letters)
  if roomid in roomidlst:
    generateRID()
  else:
    roomidlst.append(roomid)
    return roomid



def generatePID():
  letters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  pid=""
  
  for i in range(6):
    pid+=random.choice(letters)
  if pid in pidlst:
    generatePID()
  else:
    roomidlst.append(pid)
    return pid



@app.route('/')
def home():
  return render_template('home.html')

@app.route('/new')
def new():
  roomid=generateRID()
  newroom=Room(roomid)
  chats[roomid]=newroom
  return redirect(url_for('name',roomid=roomid))

@app.route('/name')
def name():
  roomid=request.args['roomid']
  
  return render_template('name.html',roomid=roomid,name=name)

@app.route('/join')
def join():
  return render_template('join.html')

@app.route('/chat',methods=['POST'])
def chat():
  roomid=request.form['roomid']
  if roomid in chats.keys():
    
    name=request.form['name']
    pid=generatePID()
    newperson=Person(name,pid,roomid)
    chats[roomid].addPerson(newperson)
    emitDataToRoom("newperson",roomid,{"name":name,"pid":pid})
    
    return render_template('chat.html',roomid=roomid,name=name,people=[chats[roomid].people[pid].name for pid in chats[roomid].people.keys()],pid=pid)
  else:
    return "ROOM DOESN'T EXIST"

@socketio.on("sentmsg")
def gotMsg(data):
  print("got data",data["msg"])
  room=chats[data["roomid"]]
  print("from room",room.roomid)
  newmsg=Msg(room.people[data["pid"]],data["msg"])
  room.addMsg(newmsg)
  emitDataToRoom("receivemsg",data["roomid"],{"pid":data["pid"],"name":newmsg.sentby.name,"text":data["msg"]})

@socketio.on("joinroom")
def joinroom(data):
  chats[data["roomid"]].addSID(request.sid)
  room=chats[data["roomid"]]
  

if __name__=='__main__':
  socketio.run(app,host='0.0.0.0', port=5000,debug=True)

