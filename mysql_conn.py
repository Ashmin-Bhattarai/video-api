from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv


def config_app(app):
    # load .env file
    load_dotenv()

    # get app config details from .env file
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

    # mysql instance
    mysql = MySQL(app)
    return mysql

def insert_video(mysql, file, length, size, cost):
    # insert video details into database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO videos (filename, length, size, cost) VALUES (%s, %s, %s, %s)", (file, length, size, cost))
    mysql.connection.commit()
    cur.close()
    return True


# query_videos with filter 
def query_videos_filter(mysql, qu):
    name = qu['filename']
    date_from = qu['date_from']
    date_to = qu['date_to']
    length_min = qu['length_min']
    length_max = qu['length_max']
    size_min = qu['size_min']
    size_max = qu['size_max']
    cost_min = qu['cost_min']
    cost_max = qu['cost_max']

    # query videos from database
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM videos WHERE \
                 (date BETWEEN '{date_from}' AND '{date_to}') AND\
                 (length BETWEEN {length_min} AND {length_max}) AND\
                 (size BETWEEN {size_min} AND {size_max}) AND \
                 (cost BETWEEN {cost_min} AND {cost_max}) AND \
                 (filename LIKE '{name}' )")

    data = cur.fetchall()
    dis = {}
    
    for row in data:
        td = {}
        td["filename"] = row[1]
        td["length"] = row[2]
        td["size"] = row[3]
        td["cost"] = row[4]
        td["date"] = row[5]
        dis[row[0]] = td

    cur.close()
    return dis


def query_videos(mysql):
    # query all videos from database
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM videos")

    data = cur.fetchall()
    dis = {}
    
    for row in data:
        td = {}
        td["filename"] = row[1]
        td["length"] = row[2]
        td["size"] = row[3]
        td["cost"] = row[4]
        td["date"] = row[5]
        dis[row[0]] = td

    cur.close()
    return dis



    