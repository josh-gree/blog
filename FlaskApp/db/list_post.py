import os
import glob
import datetime
import sys
from mongoengine import connect


sys.path.append('/opt/anaconda3/bin')
from model import Post, Random

directory = sys.argv[1]
post_or_rand = sys.argv[2]
connect('blog_posts')

os.chdir(directory)

if post_or_rand == 'p':
    title = " ".join(directory.split('/')[-1].split('_'))
    content = glob.glob('*.md')[0]
    description = glob.glob('*.desc')[0]
    date = datetime.datetime.now()
    js = glob.glob('*.js') + glob.glob('*.coffee')

    Post(title = title,content = content,date = date,js_resorces = js,description = description).save()

elif post_or_rand == 'r':
    description = glob.glob('*.desc')[0]
    description = open(description).read()
    media = glob.glob('*.med')[0]
    media = open(media).readlines()
    vid_or_img = media[0].strip()
    if vid_or_img == 'v':
        tag = '<iframe width="560" height="315" src="{}"></iframe>'.format(media[1])
    elif vid_or_img == 'i':
        tag = '<img src="{}" class="rands">'.format(media[1])
    else:
        print("Image or Video?")
    Random(description=description,tag=tag).save()

else:
    print("Is this a post or a random? p or r for second argument")
