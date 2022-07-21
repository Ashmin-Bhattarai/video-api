from secrets import choice
import requests

BASE = "http://localhost:5000/"

# give path to the video
file_to_upload  = {"file" : open("./video.mp4", "rb")}

file_to_query = {"filename" : "%",
         "date_from" : "2022-01-01",
         "date_to" : "2022-07-30",
         "length_min" : 0,
         "length_max" : 600,
         "size_min" : 0,
         "size_max" : 1024**3,
         "cost_min" : 0.0,
         "cost_max" : 35.0}

print("1. Uploading video")
print("2. Computing Cost")
print("4. Querying videos")
choice = int(input("Enter your choice: "))
if choice == 1:
    res = requests.post(BASE + "upload", files=file_to_upload)
    print(res.json())
elif choice == 2:
    res = requests.post(BASE + "getCost", files=file_to_upload)
    print(res.json())
elif choice == 4:
    res = requests.post(BASE + "getVideos", json=file_to_query)
    print(res.json())
else:
    print("Invalid choice")
    exit(1)


