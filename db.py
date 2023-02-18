import sqlite3
#import os.path as path

class DBhandler:
    
    def __init__(self):

        """def restaurant_duplicate_check(self, name):
        self.cur.execute("SELECT * FROM restaurant('name') as nameInfo")

        for res in nameInfo

        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            if res.key() == name:
                return False
        return True"""


    def insert_restaurant(self, name, data, img_path):
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        #cur = self.con.cursor()
        """restaurant_info ={
            "addr": data['addr'],
            "tel": data['tel'],
            "category": data['category'],
            "park": data['park'],
            "time": data['time'],
            "site": data['site'],
            "img_path": img_path
        }"""

        sql = "INSERT INTO restaurant VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (name, data['addr'], data['category'], img_path, data['park'],data['site'],data['tel'],data['time'],data['writer'])
        cur.execute(sql)
        con.commit()
        con.close()
        return True

        #중복확인하는거 해야흠
        """if self.restaurant_duplicate_check(name):
            sql = "INSERT INTO restaurant VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (data['name'], data['addr'], data['category'], img_path, data['park'],data['site'],data['tel'],data['time'])
            self.cur.execute(sql)
            return True
        else:
            return False"""
        
    def modify_restaurant(self, name, data, img_path):
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        sql = "UPDATE restaurant SET name='%s',addr='%s',category='%s', img_path='%s',park='%s',site='%s', tel='%s',time='%s', writer='%s' WHERE name='%s'" % (data['name'], data['addr'], data['category'], img_path, data['park'],data['site'],data['tel'],data['time'],data['writer'], name)
        cur.execute(sql)
        con.commit()
        con.close()
        return True
        
    def get_restaurants(self):
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
 
        cur.execute("SELECT * FROM restaurant")

        rows = cur.fetchall()
        con.close()
        return rows
    
    def get_restaurant_byname(self, name):
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        
        cur.execute("SELECT * FROM restaurant")
 
        rows = cur.fetchall()

        if(len(rows) ==0 ):#db 비어있는 경우
            return "None"

        for value in rows:
            if str(value['name']) == name:
                return value
        return "None"
    
    def remove_restaurant(self, name):
        #print(name)
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute('DELETE FROM restaurant where name=?',(name,))
        con.commit()
        con.close()
        return

    def find_user(self, id_, pw_):
        con=sqlite3.connect("database.db", check_same_thread=False) 
        cur = con.cursor()

        cur.execute(f"SELECT * FROM user WHERE id='{id_}' AND pw='{pw_}';")
        if  cur.fetchone():
            return True
        else:
            return False


        
