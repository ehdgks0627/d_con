#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
from pymysql import connect

# 채팅내역 DB 연동
async_mode = None

server_domain = "0.0.0.0"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
conn = connect(host='layer7.kr', port=3306, user='em', passwd='fuckkk', db='d_con', charset ='utf8')
cur = conn.cursor()

@app.route('/list/')
def list():
    return render_template('chat_list.html', async_mode=socketio.async_mode)

@app.route('/make/')
def make():
    return render_template('chat_make.html', async_mode=socketio.async_mode)

#todo chat_{$room}

@socketio.on('create', namespace='/chat_base')
def create(message):
    try:
        if message['room_name'] != "":
            cur.execute("INSERT INTO `room_list` (`name`,`password`) VALUES ('%s','%s')"%(message['room_name'], message['room_password']))
            conn.commit()
            cur.execute("CREATE TABLE `room_%s` (`message` VARCHAR(4096) NOT NULL)ENGINE=InnoDB"%(cur.lastrowid))
            conn.commit()
            emit('success', {'url': '/list/'})#delete
        else:
            emit('failure', {'data': 'room_name is empty'})#delete
    except:
        emit('failure', {'data': 'error'})

@socketio.on('get_message', namespace='/chat_base')
def get(message):
    try:
        cur.execute("SELECT * FROM `room_list` WHERE `key`='%s' AND `password`='%s'"%(message['room_key'],message['room_pwd']))
        datas = cur.fetchall()[0]
        if datas == ():
            emit('write_log', {'data': 'failure'})
        else:
            cur.execute("SELECT * FROM `room_%s`"%(message['room_key']))
            datas = cur.fetchall()
            for data in datas:
                emit('write_message', {'data': 'log=%s'%(str(data[0]))})
    except:
        emit('write_log', {'data': 'error'})

@socketio.on('leave', namespace='/chat_base')
def leave(message):
    try:
        cur.execute("DROP TABLE `room_%s`"%(message['leave_key']))
        conn.commit()
        cur.execute("DELETE FROM `room_list` WHERE `key`='%s'"%(message['leave_key']))
        conn.commit()
        emit('write_log', {'data': 'deleted'})
    except:
        emit('write_log', {'data': 'error'})

@socketio.on('send_message', namespace='/chat_base')
def send_room_message(message):
    try:
        cur.execute("INSERT INTO `room_%s` VALUES ('%s')"%(message['send_key'],message['send_msg']))
        conn.commit()
        emit('write_log', {'data': 'success'})
    except:
        emit('write_log', {'data': 'error'})

@socketio.on('connect', namespace='/chat_base')
def test_connect():
    global thread
    emit('write_log', {'data': 'Connected', 'count': 0})

@socketio.on('room_list', namespace='/chat_base')
def get_room_list():
    try:
        cur.execute("SELECT * FROM `room_list`")
        rows = cur.fetchall()
        for row in rows:
            data = "%s-%s-%s"%(row[0],row[1],row[2])
            emit('write_room_list', {'data': data})
    except:
        emit('write_log', {'data': 'error'})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host=server_domain)
