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

@app.before_request
def before_request():
    if not 'key' in session:
        session['key'] = -1

@app.route('/')
@app.route('/list/')
def list():
    try:
        ren = render_template('chat_list.html')
        return ren
    except:
        return "error"

@app.route('/make/')
def make():
    try:
        ren = render_template('chat_make.html')
        return ren
    except:
        return "error"

@app.route('/chat/', methods=['POST'])
def chat():
    try:
        ren = render_template('chat_chat.html', login_key=request.form['login_key'])
        return ren
    except:
        return "error"

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
        cur.execute("SELECT * FROM `room_list` WHERE `key`='%s'"%(message['room_key']))
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

@socketio.on('room_list', namespace='/chat_base')
def get_room_list():
    try:
        cur.execute("SELECT * FROM `room_list`")
        rows = cur.fetchall()
        for row in rows:
            emit('write_room_list', {'key': row[0], 'name': row[1]})
    except:
        emit('write_log', {'data': 'error'})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host=server_domain)
