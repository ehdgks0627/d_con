#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

server_domain = '192.168.43.230'
server_port = 5001

@app.route('/')
def index():
    return render_template('chat.html', async_mode=socketio.async_mode)

@socketio.on('write_message', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write', {'data': 'Room ' + message['room'] + ' closed.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])

@socketio.on('room_message', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])

if __name__ == '__main__':
    socketio.run(app, host=server_domain, port=server_port, debug=True)
