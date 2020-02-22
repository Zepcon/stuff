'''
What to reach: Rename multiple items in the same folder in specific patterns.

Differnce if the folder is an album or just a collection of new tracks:
1) Album: Same Interpret, Year, Genre, Album Name
          Different Track Numbers
'''
import eyed3 as d3
import os
import os.path
import glob

path = "C:\\Users\\Flavio\\Music\\Youtube"
os.chdir(path)

'''
2) Tracks: Option for same genre, all title numbers get a 1 and same year, different artists, tracke name and Single as album

Tracks are saved as "Artist - TrackName"
'''
def nameTracks(folder):
    os.chdir(folder)
    for file in glob.glob("*.mp3"):
        artist = file.partition("-")[0]
        title = file.partition("-")[1].partition(".")[0]
        audiofile = d3.load(file)
        audiofile.tag.artist = artist
        audiofile.tag.album = title +' Single'
        audiofile.tag.title = title
        audiofile.tag.save()
        os.rename(file, title)
        

def nameAlbum():
    return

question = input(('Album or Tracks? '))

if question == 'Tracks' or 'tracks' or 't':
    os.chdir("Weiteres")
    while True:
        folder = input("Enter folder name: ")
        #check for folder name
        if os.path.exists(folder):
            nameTracks(folder)
        else:
            print("Folder not found")
        
else:
    question = input("Which Artist? ")




