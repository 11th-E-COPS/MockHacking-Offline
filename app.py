from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
db_file=''

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/board")
def view_board():
    return render_template("board.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/notice")
def view_notice():
    return render_template("notice.html")

@app.route("/myaccount/3")
def getUser():
    #@app.route("/myaccount/<int:u_idx>", method=['GET'])
    #def getUser(u_idx):
    # if session.get('logFlag') != True:
    #     return redirect(url_for('login'))
    
    # 사용자 정보 가져와서 출력
    #conn = sqlite3.conect(db_file)
    # conn = sqlite3.conect('')
    # cursor = conn.cursor()
    # sql = "select pw from member where idx = ?"
    # cursor.execute(sql, (u_idx,))
    # row = cursor.fetchone()
    # user_pw=row['pw']
    # return render_template('myaccount.html', u_idx=u_idx, user_pw=user_pw)
    return render_template('myaccount.html')


@app.route("/myaccount_edit/3")
def tmpUser(edit_idx):
    #@app.route("/myaccount_edit/<int:edit_idx>", method=['GET'])
    # if session.get('logFlag') != True:
    #     return redirect(url_for(hello))
    # 사용자 정보 가져오고 입력 받아서 넘겨주기    
    #conn = sqlite3.conect(db_file)
    conn = sqlite3.conect('')
    cursor = conn.cursor()
    sql = "select pw from member where idx = ?"
    cursor.execute(sql, (edit_idx,))
    row = cursor.fetchone()
    edit_pw=row['pw']
    return render_template('myaccount_edit.html', edit_idx=edit_idx, edit_pw=edit_pw)


@app.route("/myaccount_edit_ok")
def editUser():
    # @app.route("/myaccount_edit_ok", method=['POST'])
    idx=request.form['idx']
    user_id=request.form['user_id']
    user_pw=request.form['user_pw']
    
    # 사용자 정보 수정
    #conn = sqlite3.conect(db_file)
    conn = sqlite3.conect('')
    cursor = conn.cursor()
    sql = "update member set pw=? where idx = ?"
    cursor.execute(sql, (user_pw,idx))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for(hello))
    
    
# app.secret_key

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
