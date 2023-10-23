from flask import Flask, render_template, request, json, session, jsonify
from flask_mysqldb import MySQL
import requests
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = 'vttp1003'
app.config['MYSQL_DB'] = 'Test'
app.secret_key = 'ysxabc8'


mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    message = ''
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    IsMod = request.form['IsMod']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account WHERE username = % s', (username, ))
    account = cursor.fetchone()
    if account:
        message = 'Username exists'
    else:
       cursor.execute('INSERT INTO Account (username,password,email,IsMod) VALUES(%s, %s, %s, %s)',(username,password,email,IsMod))
       mysql.connection.commit()
       message = 'Done'
    return message

@app.route('/login', methods =['POST'])
def login():
    message = ''
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Account WHERE username = % s AND password = % s', (username, password, ))
    user = cursor.fetchone()
    if user:
        session['loggedin'] = True
        session['id'] = user['id']
        session['username'] = user['username']
        session['email'] = user['email']
        message = 'Logged in successfully !'
    else:
        message = 'Please enter correct email / password !'
    return message

@app.route('/changepassword', methods = ['POST'])
def changepassword():
    message = ''
    username = request.form['username']
    password = request.form['password']
    newPass = request.form['new_password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Account WHERE username = % s AND password = % s', (username, password, ))
    user = cursor.fetchone()
    if user:
        id = user['id']
        cursor.execute('UPDATE Account SET password = % s WHERE id = %s',(newPass, id))
        message = 'Done'
        mysql.connection.commit()
    else:
        message = 'Fail'
    return message

@app.route('/searchemail', methods = ['GET'])
def searchemail():
    email = request.form['email']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE email = %s', (email, ))
    userList = cursor.fetchall()
    if userList:
        respone = []
        for user in userList: 
            item = {'id': user['id_user'], 'user_name': user['user_name'], 'link_avatar': user['link_avatar'],
                   'ip_register': user['ip_register'],'device_register': user['device_register'], 
                   'password': user['password'],'email': user['email'], 'count_sukien': user['count_sukien'],
                   'count_comment': user['count_comment'], 'count_view': user['count_view']}
            respone.append(item)
        return jsonify(respone)
    else:
        respone = {'respone': 'No User Found'}
        return jsonify(respone)
    
@app.route('/searchip', methods = ['GET'])
def searchip():
    ip_register = request.form['ip_register']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE ip_register = %s', (ip_register, ))
    userList = cursor.fetchall()
    if userList:
        respone = []
        for user in userList: 
            item = {'id': user['id_user'], 'user_name': user['user_name'], 'link_avatar': user['link_avatar'],
                   'ip_register': user['ip_register'],'device_register': user['device_register'], 
                   'password': user['password'],'email': user['email'], 'count_sukien': user['count_sukien'],
                   'count_comment': user['count_comment'], 'count_view': user['count_view']}
            respone.append(item)
        return jsonify(respone)
    else:
        respone = {'respone': 'No User Found'}
        return jsonify(respone)
    

@app.route('/search', methods = ['GET'])
def search():
    if 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email, ))
        userList = cursor.fetchall()
        if userList:
            respone = []
            for user in userList: 
                item = {'id': user['id_user'], 'user_name': user['user_name'], 'link_avatar': user['link_avatar'],
                   'ip_register': user['ip_register'],'device_register': user['device_register'], 
                   'password': user['password'],'email': user['email'], 'count_sukien': user['count_sukien'],
                   'count_comment': user['count_comment'], 'count_view': user['count_view']}
                respone.append(item)
            return jsonify(respone)
        else:
            respone = {'respone': 'No User Found'}
            return jsonify(respone)
    elif 'ip_register' in request.form:
        ip_register = request.form['ip_register']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE ip_register = %s', (ip_register, ))
        userList = cursor.fetchall()
        if userList:
            respone = []
            for user in userList: 
                item = {'id': user['id_user'], 'user_name': user['user_name'], 'link_avatar': user['link_avatar'],
                   'ip_register': user['ip_register'],'device_register': user['device_register'], 
                   'password': user['password'],'email': user['email'], 'count_sukien': user['count_sukien'],
                   'count_comment': user['count_comment'], 'count_view': user['count_view']}
                respone.append(item)
            return jsonify(respone)
        else:
            respone = {'respone': 'No User Found'}
            return jsonify(respone)
    elif 'id_toan_bo_su_kien' in request.form:
        id_toan_bo_su_kien = request.form['id_toan_bo_su_kien']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM add_sukien WHERE id_toan_bo_su_kien = %s', (id_toan_bo_su_kien, ))
        userList = cursor.fetchall()
        if userList:
            respone = []
            for user in userList: 
                item = {'id_add': user['id_add'], 'id_toan_bo_su_kien': user['id_toan_bo_su_kien'], 'id_user': user['id_user'],
                   'ten_sukien': user['ten_sukien'],'noidung_su_kien': user['noidung_su_kien'], 
                   'ten_nam': user['ten_nam'],'ten_nu': user['ten_nu'], 'device_them_su_kien': user['device_them_su_kien'],
                   'ip_them_su_kien': user['ip_them_su_kien'], 'link_image': user['link_img'], 'link_video': user['link_video'],
                   'id_template': user['id_template'], 'thoigian_themsk': user['thoigian_themsk'],
                   'so_thu_tu_su_kien': user['so_thu_tu_su_kien'], 'count_comment': user['count_comment'],
                   'count_view': user['count_view'], 'status': user['status']}
                respone.append(item)
            return jsonify(respone)
        else:
            respone = {'respone': 'No Event Found'}
            return jsonify(respone)
    elif 'noi_dung_Comment' in request.form:
        noi_dung_Comment = request.form['noi_dung_Comment']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM comment WHERE noi_dung_Comment = %s', (noi_dung_Comment, ))
        userList = cursor.fetchall()
        if userList:
            respone = []
            for user in userList: 
                item = {'id_Comment': user['id_Comment'], 'noi_dung_Comment': user['noi_dung_Comment'], 'id_user': user['id_user'],
                   'IP_Comment': user['IP_Comment'],'device_Comment': user['device_Comment'], 
                   'id_toan_bo_su_kien': user['id_toan_bo_su_kien'],'imageattach': user['imageattach'], 'thoi_gian_release': user['thoi_gian_release'],
                   'id_user': user['id_user'], 'user_name': user['user_name'], 'avatar_user': user['avatar_user'],
                   'so_thu_tu_su_kien': user['so_thu_tu_su_kien'], 'location': user['location']}
                respone.append(item)
            return jsonify(respone)
        else:
            respone = {'respone': 'No Comment Found'}
            return jsonify(respone)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return 'logout'

if __name__ == "__main__":
    app.run()
