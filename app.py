from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import DBhandler
import sys
application = Flask(__name__)
DB = DBhandler()

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    
    datas = DB.get_restaurants()
    total_count = len(datas)

    return render_template("list.html", datas = datas, total_count = total_count)

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
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form

    if DB.insert_restaurant(data['name'], data, image_file.filename):
        return render_template("submit_restaurant_result.html", data=data, image_path="static/image/"+image_file.filename)
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
        return redirect(url_for('list'))
    
    return render_template("detail.html", name = name, data=data)

@application.route('/remove',methods=['POST'])
def remove():
    data = request.form
    DB.remove_restaurant(data['name'])
    return view_list()

    

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)


