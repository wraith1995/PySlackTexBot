from slackbot.bot import respond_to
import slackbot_settings
from slackbot_settings import template,imageDir,tex,poppler,pnmtopng,pdfCrop
import re
import json
import shutil
import time
from subprocess import call
import json
import pyimgur
import os 
import html
@respond_to('(.*)')
def tex(msg,textp):
    text = html.unescape(textp)
    
    os.chdir(slackbot_settings.imageDir)
    stamp = str(time.time())[0:10] #this might bite me in the ass as I'm not sure how slackbot is working/if it is concurrent
    
    resPrefix = imageDir+stamp
    resTex = resPrefix+".tex"
    with open(template) as f: #create the .tex file
        temp = f.read()
        imtext = temp.replace("%replaceme%",text)
        print(imtext)
        with open(resTex,'w+') as g:
            g.write(imtext)
    
    call([slackbot_settings.tex,resTex]) #compile it to a pdf
    
    call([pdfCrop,resPrefix+".pdf"]) #crop the tex file
    #pdftoppm document-crop.pdf -png > 
    png = resPrefix + ".png"
    with open(png,'w+') as f: 
        call([slackbot_settings.poppler,resPrefix+"-crop.pdf","-png"],stdout=f) #create png
    
    im = pyimgur.Imgur(slackbot_settings.imgurClientId) #upload to imgur
    upimg = im.upload_image(png, title="some tex")
    attachments = [
        {
            "title" : "Compiled Tex",
            "image_url" : upimg.link
        }]
    msg.send_webapi('', json.dumps(attachments))
    
    
    
    



    
            

        

    
