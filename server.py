import socketio
from eventlet import wsgi,listen

sio=socketio.Server(cors_allowed_origins="*")
app=socketio.WSGIApp(sio)

players={}

@sio.event
def connect(id, env):
    print("Ada yg masuk")


@sio.event
def disconnect(id):
    print("Ada yg keluar")


@sio.on("player_add")
def player_add(id, name):
    if id not in players:
        players[id] = {"name": name, "x": 150, "y": 150}
        print(f"Player {name} added!")
        sio.emit("players_update", players)

@sio.on("player_remove")
def player_remove(id, name):
    players.pop(id,None)
    sio.emit("players_update", players)
    print(f"Player {name['name']} has disconnected")

    
@sio.event
def move(id, data):
    if id in players:
        # players[id]['name']=data.get("name","")
        players[id]['x']+=data.get("dx",0)
        players[id]['y']+=data.get("dy",0)
        sio.emit("players_update", players)

if __name__ == '__main__':
    wsgi.server(listen(("0.0.0.0",5000)),app)


