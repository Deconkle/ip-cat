from flask import request, Flask, send_file # webserver stuff
from PIL import Image, ImageDraw, ImageFont # draw on images
from random import choices # choose random file names
import string # import letters for filenames
from os import environ # read env vars for our api key
from time import sleep # sleep incase we're getting rate limited
import requests # ip geolocate api
from json import loads # load json from ip geolocate api
from io import BytesIO
app = Flask(__name__)

ip_info = {} # here we cache IP's so our api doesn't get mad at us
ipinfo_key = os.environ['IP_KEY'] # take our api key from env
ip_query_url = "https://ipinfo.io/{}/json" # url for our ip geolocate api

URL_TO_MY_WEBSERVER = "http://example.gg" # <-- CHANGE this to your url if you want any hope of this thing working 

def access_control(req): # this will get rid of nearly all bots requesting your home ip address - good since we return 200 on every url lol
    if not req.host_url.startswith(URL_TO_MY_WEBSERVER)
        #print("host_url = host ip")
        print("Client didn't pass access control, serving forbidden.")
        return False
    return True
 
def get_ipinfo(ip):
    if ip in ip_info.keys():
        return ip_info[ip]
    else:
        r = requests.get(ip_query_url.format(ip), headers={"Authorization": "Bearer "+ipinfo_key})
        if r.ok:
            response = loads(r.text)
            ip_info[ip] = response
            return response # return json obj of ip information returned from api
        else: # if not ok: uhh shit
            print("Ip info request returned: "+str(r.status_code)) # what happened?
            print(r.content)
            print(r.request.url)
            sleep(2)
            get_ipinfo(ip) # surely it's okay 2 seconds later 👀

 
def write_image(ip):
    data = get_ipinfo(ip)
    img = Image.open("templates/wutcat.jpg") # open the template
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("FRAMDCN.ttf",50)
    font2 = ImageFont.truetype("FRAMDCN.ttf",25)
    draw.text((15,10), "heres ur ip incase u forgor", font=font, fill=(0,0,0)) # write on it  # (15,10) x (15,65) was quite good at size 60
    draw.text((15,65), ip, font=font, fill=(0,0,0))
    draw.text((15,120), "and rmembr u live in: "+data['city'], font=font, fill=(0,0,0))
    draw.text((15,175), "u can contact ur isp here: "+data['org'], font=font, fill=(0,0,0))
    return img
 
@app.errorhandler(Exception)
def handle_error(e):
    if access_control(request):
        img = write_image( request.headers['X-Forwarded-For'] ) # write ip info on image in memory
        img_io = BytesIO() # use bytesio to send file from memory instead of temp files
        img.save(img_io, "JPEG", quality=70) 
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpg') # sending the file from memory (so this image is never visible to me)
    else: # no access control (bots trying to hit my webserver)
        return "no", 403
 
