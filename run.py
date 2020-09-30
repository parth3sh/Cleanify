import cleanifyscript as c
import sys

def run(inputUri):
    sp = c.initializeAPI()
    finalURI = c.getPlaylist(sp,inputUri)
    return finalURI

