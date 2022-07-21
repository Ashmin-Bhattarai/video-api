Video Api Docs
==============

This is a simple API created using python flask server. It is used to store and retrieve videos.  
This API contains three endpoints:  

*   http://localhost:5000/
*   http://localhost:5000/upload
*   http://localhost:5000/getCost
*   http://localhost:5000/getVideos

**/**  
This endpoint is used to render index.html i.e. the current page.  
  
**/upload**  
This endpoint is used to upload a video. It works on **POST** request method. It takes a file as a parameter, validates wheather file in mp4 or mkv and check size and video length.Once the verification is compleated the is will store video file to upload directory and stores it's name, size, uploaded date, etc in the database.  
  
**/getCost**  
This endpoint is used to get the cost of a video. It also works on **POST** request method. It takes a video name as a parameter and returns the cost of the video.  
  
**/getVideos**  
This endpoint is used to get all the videos. It works on both **GET** and **POST** request method. If GET method is used the it returns all the videos in the database. If POST method is used it takes a video name as a parameter and returns the video details.  
  

Initial Database Setup
----------------------

Before using this API you need to setup a database. This database will be used to store the videos information.  
To setup the database you need to create **.env** file in root directory and it must contain as below:  

                MYSQL_HOST = 'localhost'
                MYSQL_USER = 'ashmin'  --> username of the database
                MYSQL_PASSWORD = 'password' --> password of the database
                MYSQL_DB = 'test' --> name of the database
            

Create a datebase **test**  
To create database in msql prompt run the following command:  

                CREATE DATABASE test;
                use test;
            

Then source dump file by:

                source initial_dump.sql;
            

DataBase Info
-------------

*   Database Server : MySQL
*   Database Name : test
*   Table Name : videos
*   Columns :
    *   id : int primary key auto increament
    *   filename : varchar(255) name of the video
    *   length : int length of the video
    *   size : int size of the video
    *   cost : float cost of the video
    *   date :datetime default(current timestamp) date of the video upload

Used Libraries
--------------

*   flask
*   flask-mysql
*   os
*   time
*   werkzeug

**Note:**  
All required Libraries can be installed using **requirement.txt** file by:  

            pip install -r requirement.txt
        

Run the API
-----------

To run the API you need to run the following command in root directory :  

                python3 server.py
            

Test the API
------------

To test the API you can run **client.py** or in browser goto end of home page: