#!/usr/bin/python

import md5
import unicodedata
import string
import sys

DIRIN="/home/javier/.cache/album-art/"
DIROUT="/home/javier/.cache/media-art/"

def dropInsideContent(s, startMarker, endMarker):
    startPos = s.find(startMarker)
    endPos = s.find(endMarker)
    if startPos > 0 and endPos > 0 and endPos>startPos:
            return s[0:startPos] + s[endPos+1:len(s)]
    return s

def parseFileName(name):
    nameString = dropInsideContent(name,"[","]" )
    nameString = dropInsideContent(nameString,"{","}" )
    nameString = dropInsideContent(nameString,"(",")" )    
    nameString = nameString.strip('()_{}[]!@#$^&*+=|\\/"\'?<>~`')
    nameString = nameString.lstrip(' ')
    nameString = nameString.rstrip(' ')
    nameString = dropInsideContent(nameString,"{","}" )
    nameString = nameString.lower()
    nameString = string.replace(nameString,"\t"," ")
    nameString = string.replace(nameString,"  "," ")    
    
    try: 
        nameString = unicodedata.normalize('NFKD',nameString).encode()
        nameString = nameString.encode()
    except:
        try:
            nameString = nameString.encode('latin-1', 'ignore')
            nameString = unicodedata.normalize('NFKD',nameString).encode("ascii")
            nameString = str(nameString)
        except:
            nameString = "unknown"
    if len(nameString)==0: nameString=" "
    
    return nameString

def getCoverArtFileName(artist, album):
    """Returns the cover art's filename that is formed from the artist & album name."""
    if artist == u'':
        artistString = " "    
    else:
        artistString = parseFileName(artist)
    
    albumString = parseFileName(album)
    print >> sys.stderr, "%s - %s" % (artistString, albumString)
    artistMD5 = md5.new(artistString).hexdigest()
    albumMD5 = md5.new(albumString).hexdigest()
    albumArt = "album-" + artistMD5 + "-" + albumMD5 + ".jpeg"
    return albumArt

if __name__ == "__main__":
    try:
        print getCoverArtFileName(unicode(sys.argv[1]), unicode(sys.argv[2]))
    except:
        print getCoverArtFileName(u'', unicode(sys.argv[1]))


