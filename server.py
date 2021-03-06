from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from asgiref.wsgi import WsgiToAsgi

"https://levelup.gitconnected.com/data-stream-from-your-webcam-and-microphone-videochat-with-javascript-step-1-29895b70808b"

'''
Set-ExecutionPolicy -ExecutionPolicy bypass -scope CurrentUser
TO RUN THE SERVER PASTE THIS INTO THE TERMINAL:
uvicorn server:app
TO STOP THE SERVER SIMPLY HOLD Ctrl AND PRESS c:
Ctrl + c
MAKE SURE YOU HAVE VENV ACTIVATED BEFORE STARTING:
'''

app = Flask(__name__)
socket = SocketIO(app)
wsgi = WsgiToAsgi(app)


@app.route('/')
async def index():
    return render_template('index.html')

@socket.on('data')
async def connect():
    print("[CLIENT CONNECTED]:", request.sid)

@socket.on('data')
async def disconn():
    print("[CLIENT DISCONNECTED]:", request.sid)

@socket.on('data')
async def notify(user):
    await sio.emit('notify', user, broadcast=True, skip_sid=request.sid)

@socket.on('data')
async def emitback(data):
    await sio.emit('returndata', data, broadcast=True)


'''''
sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files = {
    '/': './public/index.html',
    '/index.js': './public/index.js',
    '/functions.js': './public/functions.js'
})
client_count = 0
a_count= 0
b_count = 0



async def task(sid):
    await sio.sleep(5)
    result = await sio.call('mult', {'numbers': [3,4]}, to=sid)
    print(result)

@sio.event
async def connect(sid, environ):
    global client_count


    username = environ.get('HTTP_X_USERNAME')
    print('username:', username)
    if not username:
        return False

    async with sio.session(sid) as session:
        session['username'] = username
    await sio.emit('user_joined', username)

    global a_count
    global b_count

    if random.random() > 0.5:
        sio.enter_room(sid, 'a')
        a_count += 1
        await sio.emit('room_count', a_count, to='a')
    else:
        sio.enter_room(sid, 'b')
        b_count += 1
        await sio.emit('room_count', b_count, to='b')
    client_count += 1
    print(sid, 'connected')
    sio.start_background_task(task,sid)
    await sio.emit('client_count', client_count)

@sio.event
async def disconnect(sid):
    global client_count
    global b_count
    global a_count
    client_count -= 1
    print(sid, 'disconnected')
    await sio.emit('client_count', client_count)
    if 'a' in sio.rooms(sid):
        a_count -= 1
        await sio.emit('room_count', a_count, to='a')
    else:
        b_count -= 1
        await sio.emit('room_count', b_count, to='b')

    async with sio.session(sid) as session:
        await sio.emit('user_left', session['username'])

@sio.event
async def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    return result
    
    '''
