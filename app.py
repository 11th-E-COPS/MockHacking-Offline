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

    if request.method == 'POST':
        id_=request.form['id']
        pw_=request.form['pw']
        
        if DB.find_user(id_, pw_):
            session['logFlag'] = True
            session['id']=id_
            return redirect(url_for('view_list'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@application.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

@application.route("/notice")
def view_notice():
    return render_template("notice.html")

# db에서 사용자 비번 조회해서 넘겨주기
@application.route("/myaccount")
def getUser():
    if session.get('logFlag') != True:
        return redirect('/login')   
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "select pw from user where id = ?"
    id= session['id']
    cursor.execute(sql, (id,))
    row = cursor.fetchone()
    user_pw=row[0]
    return render_template('myaccount.html', id=id, pw=user_pw)

# db에서 사용자 비번 조회해서 넘겨주기
@application.route("/myaccount_edit")
def editUser():
    if session.get('logFlag') != True:
        return redirect('/login')   
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "select pw from user where id = ?"
    id= session['id']
    cursor.execute(sql, (id,))
    row = cursor.fetchone()
    user_pw=row[0]
    return render_template('myaccount_edit.html', id=id, pw=user_pw)


# db에서 사용자 정보 수정
@application.route("/myaccount_edit_proc", methods=['POST'])
def myaccount_edit_proc():
    uid=session['id']
    upw=request.form['pw']
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "update user set pw=? where id = ?"
    cursor.execute(sql, (upw,uid))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/login')
    

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)