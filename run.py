import cleanify as c
import sys

def run(inputUri):
    sp = c.iniializeAPI()
    c.getPlaylist(sp,inputUri)

