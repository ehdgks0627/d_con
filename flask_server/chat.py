#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from pymysql import connect

# 채팅내역 DB 연동
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
server_domain = "192.168.43.230"
conn = connect(host='layer7.kr', port=3306, user='root', passwd='fuck2016', db='d_con', charset ='utf8')
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('chat.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/chat_base')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write_log',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('join', namespace='/chat_base')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    cur.execute("INSERT INTO room_list (`name`,`password`) VALUES ('%s','%s')"%(message.))

    emit('write_log',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('leave', namespace='/chat_base')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write_log',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('my_room_event', namespace='/chat_base')
def send_room_message(message):
    data =  "%s - %s - %s"%(session.get('receive_count', 0) + 1,message['data'],message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write_log',
         {'data': data, 'count': session['receive_count']},
         room=message['room'])

@socketio.on('disconnect_request', namespace='/chat_base')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('write_log',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/chat_base')
def test_connect():
    global thread
    emit('write_log', {'data': 'Connected', 'count': 0})

@socketio.on('room_list', namespace='/chat_base')
def get_room_list():
    cur.execute("SELECT * FROM room_list")
    rows = cur.fetchall()
    for row in rows:
        data = "%s-%s-%s"%(row[0],row[1],row[2])
        emit('write_room_list', {'data': data})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host=server_domain)
