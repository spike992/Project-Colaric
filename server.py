import socketio

'''
TO RUN THE SERVER PASTE THIS INTO THE TERMINAL:
uvicorn server:app
TO STOP THE SERVER SIMPLY HOLD Ctrl AND PRESS c:
Ctrl + c
MAKE SURE YOU HAVE VENV ACTIVATED BEFORE STARTING:
cd D:/Projekt-Colarič
./venv/scripts/activate
'''


sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files = {
    '/': './public/index.html',
    '/index.js': './public/index.js'
})
client_count = 0



async def task(sid):
    await sio.sleep(5)
    result = await sio.call('mult', {'numbers': [3,4]}, to=sid)
    print(result)

@sio.event
async def connect(sid, environ):
    global client_count
    client_count += 1
    print(sid, 'connected')
    sio.start_background_task(task,sid)
    await sio.emit('client_count', client_count)


@sio.event
async def disconnect(sid):
    global client_count
    client_count -= 1
    print(sid, 'disconnected')
    await sio.emit('client_count', client_count)


@sio.event
async def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    return result


