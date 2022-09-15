from flask import request, Flask, send_file # webserver stuff
from PIL import Image, ImageDraw, ImageFont # draw on images
from random import choices # choose random file names
import string # import letters for filenames
import os # delete images using os.system, and read env vars using os.environ
from time import time,sleep # time conf
import requests # ip geolocate api
from json import loads # load json from ip geolocate api
from io import BytesIO
app = Flask(__name__)

ip_info = {} # if you spam the ip info api I use they'll get mad and want me to pay. here we
ipinfo_key = os.environ['IP_KEY'] # take our api key from env
ip_query_url = "https://ipinfo.io/{}/json" # url for our ip geolocate api
 
def access_control(req):
    if not req.host_url.startswith("http://relay.decline.gg") and not req.host_url.startswith("http://e2.decline.gg"):
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
        else: # if not ok: shit
            print("Ip info request returned: "+str(r.status_code)) # what happened?
            print(r.content)
            print(r.request.url)
            sleep(2)
            get_ipinfo(ip) # try again after 2 seconds.

 
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
 
