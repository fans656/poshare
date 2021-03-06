# coding: utf-8
from flask import g

db = 'mysql'
db = 'sqlite'

if db == 'sqlite':
    import sqlite3 as db
    # localhost
    connect_args = {
        'database': 'data.db',
    }
    def to_array(d):
        return [t[0] for t in d]
elif db == 'mysql':
    import MySQLdb as db
    import MySQLdb.cursors

    def to_array(d):
        return [t.values()[0] for t in d]

    # pythonanywhere.com
    connect_args = {
        'host': 'fans656.mysql.pythonanywhere-services.com',
        #'port': 3306,
        'user': 'fans656',
        'passwd': 'test',
        'db': 'fans656$default',
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    # localhost
    connect_args = {
        'host': 'localhost',
        'port': 3306,
        'user': 'fans656',
        'passwd': '',
        'db': 'test',
        'cursorclass': MySQLdb.cursors.DictCursor
    }

def get_db():
    t = getattr(g, '_database', None)
    if t is None:
        t = g._database = db.connect(**connect_args)
    return t

def get_cursor():
    return get_db().cursor()

def create(cur, table_name, schema, data):
    cur.execute(u'drop table if exists {}'.format(table_name))
    cur.execute(u'create table {} {}'.format(table_name, schema))
    lines = data.split('\n')
    lines = [line for line in lines if line.strip()]
    for line in lines:
        cmd = u'insert into {} values {}'.format(table_name, line)
        cur.execute(cmd.encode('utf-8'))

def create_tables():
    con = db.connect(**connect_args)
    cur = con.cursor()
    # lessons
    create(cur, 'lessons',
        '''(
            lesson varchar(255),
            teacher varchar(255),
            building varchar(255),
            floor int,
            room int,
            weekday int,
            beg int,
            end int
            )''',
        u'''
        ('计算机网络实验', '马跃', '教3', 2, 239, 1, 1, 2)
        ('自然辩证法概论', '赵玲', '教3', 2, 239, 1, 5, 6)
        ('图论及其应用', '卓新建', '教3', 1, 132, 3, 1, 3)
        ('中国特色社会主义理论与实践研究', '李钢', '教3', 2, 239, 3, 5, 6)
        ('高级数理逻辑', '潘维民', '教3', 2, 235, 3, 9, 11)
        ('移动通信网原理与技术', '周文安', '主楼', 2, 206, 4, 5, 6)
        ('计算机网络原理', '马跃', '主楼', 2, 212, 5, 1, 2)
        ''')

    # rooms
    def gen_rooms(building, floors):
        return [
            u"('{}', '{}', '{}{:02}')".format(
                building, floor, floor, room)
            for floor in range(1, floors+1) for room in range(1,40+1)
            ]

    create(cur, 'rooms',
        '''(
        building varchar(255),
        floor int,
        room int
        )''',
        '\n'.join(gen_rooms(u'教1', 8) +
        gen_rooms(u'教2', 8) +
        gen_rooms(u'教3', 15) +
        gen_rooms(u'教4', 8) +
        gen_rooms(u'主楼', 3))
        )

    con.commit()
    con.close()
