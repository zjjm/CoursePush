# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify
import os,sqlite3
from datetime import datetime

DATABASE = "H:/Python/Bot/WXBot/flask/db/class.sqlite"

app = Flask(__name__, instance_relative_config=True)    #工厂模式

app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

#防止中文被转义
app.config['JSON_AS_ASCII'] = False

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

#首页
@app.route('/')
#@limiter.limit("20 per hour")  #自定义访问速率
def index():
    now = datetime.today().date()
    return now

#用户数据
@app.route('/api/course', methods=('GET','POST'))
#@limiter.limit("20 per hour")  #自定义访问速率
def get_course():
    class_name = []
    class_time=[]
    t_name=[]
    class_room=[]
    class_course=[]
    class_week=[]
    s = ""

    classname = request.args.get('classname','')
    classweek = request.args.get('classweek','')
    classday = request.args.get('classday','')
    
    data = ['and','like','exec','insert','select','drop','grant','alter','delete','update','count','chr','mid','master','truncate','char','delclare','or','\b','(\*',';']
    for v in data:
        if classname == v or classweek == v or classday== v:
            error = 400
            return {error:'error'}

    if classname == '' or classweek=='' or classday=='':
        error = 400
        return {error:'error'}
    else:
        sql = ("SELECT * FROM classtable WHERE classname='%s' and classweek=%s and classday = '%s'" % (classname,classweek,classday))
    print(sql)

    try:
        sqliteDB = sqlite3.connect(DATABASE)
        #sql查询
        cur = sqliteDB.execute(sql)
        for row in cur.fetchall():
            class_name.append(row[1])
            class_course.append(row[2])
            class_week.append(row[3])
            class_time.append(row[4])
            t_name.append(row[5])
            class_room.append(row[6])
        sqliteDB.close()
        return jsonify({classday:[{"c_name":class_name,"c_course":class_course,"c_week":class_week,"c_time":class_time,"t_name":t_name,"c_room":class_room,"state_code":"200"}]})
    except Exception as error:
        print('error')
        return {400:'error'}

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=55)
