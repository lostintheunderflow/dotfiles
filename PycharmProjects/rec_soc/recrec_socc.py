import urllib2
from bs4 import BeautifulSoup
import re
from collections import namedtuple
from operator import attrgetter
import string
import random
import datetime
from copy import deepcopy
from pushbullet.pushbullet import PushBullet
import subprocess
import os.path
import time



apiKey = "ENTER_KEY"
p = PushBullet(apiKey)
# Get a list of devices
devices = p.getDevices()
outdir = '/mnt/42c9/xbmc/Video/Recording/'


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in xrange(length))

event = namedtuple("event", "priority line link hd sky celtic")

#team = 'celtic'
team = 'roma'
soc_url = "https://www.reddit.com/r/soccerstreams/"
while True:
    hdr = { 'User-Agent' : random_string(10) }
    req = urllib2.Request(soc_url, headers=hdr)
    html = urllib2.urlopen(req).read()
    found = False

    soup = BeautifulSoup(html,'html.parser')
    for a in soup.find_all('a', href=True):
        if team in a['href'] and 'http' in a['href']:
            match_url = a['href']
            print "Found the URL:", match_url
            found = True

    if not found:
        print 'not found'
        time.sleep(5 * 60)
        continue
    #match_url = 'test.html'
    #    match_url = 'https://www.reddit.com/r/soccerstreams/comments/9ur0ek/2000_gmt_inter_vs_barcelona/'

    matchname = re.findall('\/([^\/]+)\/?$',match_url)[0]
    dt = datetime.datetime.now()
    matchname = dt.strftime("Y%y%b%w_") + matchname
    print matchname


    req = urllib2.Request(match_url, headers=hdr)
    match_html = urllib2.urlopen(req).read()

    match_soup = BeautifulSoup(match_html,'html.parser')
    code_blocks = match_soup.findAll('code')
    acelist = []
    for block in code_blocks:
        lines = re.findall('acestream://[^\n]+', block.text)
        for line in lines:
            if line:
                priority = 0
                link = re.findall('acestream://[^\s]+',line)
                if re.findall('HD',line) or re.findall('1080p',line):
                    hd = True
                    priority = priority + 4
                else:
                    hd = False
                if re.findall('sky',line):
                    sky = True
                    priority = priority + 2
                else:
                    sky = False
                if re.findall('celtic',line):
                    celtic = True
                    priority = priority + 1
                else:
                    celtic = False


                acelist.append(event(priority,line,link,hd,sky,celtic))


    sorted_list = sorted(acelist, key=attrgetter('priority'), reverse=True)
    streamtoget = sorted_list[0]
    acelink = streamtoget.link[0]


    outfile = outdir + matchname + '.mpg'

    launchcmd = ['acestream-launcher', '-p', '\'vlc --sout=file/ts:' + outfile +'\'', acelink]
    launchstr = 'acestream-launcher -p \"vlc --sout=file/ts:' + outfile +'\" ' + acelink

    #launchcmd = ['acestream-launcher', '-p', '"vlc"', acelink]
    if not os.path.isfile(outfile):
        p.pushLink(devices[0]["iden"], matchname, acelink)
        os.system(launchstr)
        #p = subprocess.Popen(launchcmd, stdout=subprocess.PIPE)

    time.sleep( 5*60 )
