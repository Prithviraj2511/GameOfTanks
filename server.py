import socket
from _thread import *
import sys
import pickle
from player import *
server="192.168.43.33"
port=5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection , Server started")


pos=[((200, 200, 0),(150, 250), 90),((0, 0, 200),(650, 450),-90)]
pos2={0:(90,pygame.Rect(100,100,100,100),90,0.0,0,100),1:(-90,pygame.Rect(600,400,100,100),-90,0.0,0,100)}
def threaded_client(conn,player):
    conn.send(pickle.dumps(pos[player]))

    reply=""
    while True:
        try:
            data=pickle.loads(conn.recv(2049))
            pos2[player]=data
            if not data:
                print("Disconnected")
                break
            else:
                if player==1:
                    reply=pos2[0]
                else:
                    reply=pos2[1]
                print("Received : ",data)
                print("Sending : ",reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost connection")
    conn.close()

currentplayer=0
F=0
while True:
    conn,addr=s.accept()
    if conn:
        F+=1
    print("Connected to : ",addr)
    start_new_thread(threaded_client,(conn,currentplayer))
    currentplayer+=1