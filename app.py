from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import DBhandler
import sys
import sqlite3

application = Flask(__name__)
application.secret_key = 'SUPERSECRETKEY'
DB = DBhandler()

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    
    datas = DB.get_restaurants()
    total_count = len(datas)

    return render_template("list.html", datas = datas, total_count = total_count)

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/register_restaurant")
def reg_restaurant():
    return render_template("register_restaurant.html")

@application.route("/submit_restaurant")
def reg_restaurant_submit():
    name=request.args.get("name")
    addr=request.args.get("addr")
    tel=request.args.get("tel")
    category=request.args.get("category")
    park=request.args.get("park")
    time=request.args.get("time")
    site=request.args.get("site")
    print(name,addr,tel,category,park,time,site)

@application.route("/submit_restaurant_post", methods=['POST'])
def reg_restaurant_submit_post():

    image_file=request.files["file"]
    image_file.save("static/{}".format(image_file.filename))
    data=request.form

    if DB.insert_restaurant(data['name'], data, image_file.filename):
        return render_template("submit_restaurant_result.html", data=data, image_path="static/"+image_file.filename)
    else:
        return "Restaurant name already exist!"


@application.route('/dynamicurl/<variable_name>')
def DynamicUrl(variable_name):
    return str(variable_name)


# 상세페이지
@application.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))

    if str(data) == "None":
        flash("올바르지 않은 맛집 이름입니다.")
        return view_list()
    
    return render_template("detail.html", name = name, data=data)

@application.route("/remove",methods=['POST'])
def remove():
    data = request.form
    DB.remove_restaurant(data['name'])
    return view_list()
@application.route("/modify",methods=['POST'])
def modify():
    data = request.form
    datas = DB.get_restaurant_byname(data['name'])
    #print(datas)
    return render_template("modify_info.html", datas=datas)

@application.route("/modify_restaurant_post", methods=['POST'])
def mod_restaurant_submit_post():

    image_file=request.files["file"]
    #image_file.save("static/{}".format(image_file.filename))
    data=request.form
    #print(data)

    if DB.modify_restaurant(data['origin_name'], data, image_file.filename):
        return view_restaurant_detail(data['name'])

    else:
        return "Restaurant name already exist!"

@application.route("/register_review")
def reg_review():
    return render_template("register_review.html")
    
@application.route("/board")
def view_board():
    return render_template("board.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    conn=sqlite3.connect("database.db", check_same_thread=False) 
    cor = conn.cursor()
    conn.row_factory = sqlite3.Row

    id_=request.form['id']
    pw_=request.form['pw']
    
    cor.execute("INSERT INTO user(id, pw) VALUES(?,?)",(id_,pw_))
    conn.commit()
    conn.close()
    
    return redirect('/login')

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():

    id_=request.form['id']
    pw_=request.form['pw']
        
    if DB.find_user(id_, pw_):
       session['id']=id_
       return redirect('/')
    else:
        return render_template("login.html")


@application.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

@application.route("/notice")
def view_notice():
    return render_template("notice.html")

@application.route("/myaccount/3")
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


@application.route("/myaccount_edit/3")
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


@application.route("/myaccount_edit_ok")
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
    application.run(host='0.0.0.0', port=5000, debug=True)
