# Goal: Rename multiple mp3 files with their properties to get them ready for iTunes
# todo: Find a way to add the music cover to every track

import eyed3 as d3
import os
import os.path
import glob
import datetime
import requests
from bs4 import BeautifulSoup
import re
import string
import shutil

path = "C:\\Users\\Flavio\\Music\\Youtube\\Weiteres"
os.chdir(path)
d3.log.setLevel("ERROR")


def nameTracks(folder, genre="[Hip-Hop/Rap]"):
    """ Tracks are saved as "Artist - TrackName"
    Tracks: Option for same genre, all title numbers get a 1, same year, different artists, track name, album like "Track Name - Single"
    """
    # os.chdir(folder)
    for file in glob.glob(os.path.join(folder, "*.mp3")):
        if file.find("-") != -1:
            trackArtist = os.path.basename(file).partition("-")[0]
            title = os.path.basename(file).partition(" - ")[2].partition(".mp3")[0]
            audiofile = d3.load(file)
            audiofile.tag.genre = genre
            audiofile.tag.release_date = datetime.datetime.now().year
            audiofile.tag.artist = trackArtist
            audiofile.tag.track_num = 1
            if title.find(" ft.") != -1:  # cut off features als well for the album name
                audiofile.tag.album = title.partition(" ft.")[0] + " - Single"
            else:
                audiofile.tag.album = title + ' - Single'
            audiofile.tag.title = title
            audiofile.tag.save()
            os.rename(file, os.path.join(folder, title + ".mp3"))  # also rename the whole file to have just the title of the track
        else:
            print("File already formatted or not named properly! ")
    print("Track naming finished! ")


def nameAlbum(artist, album, genre="[Hip-Hop/Rap]"):
    """ Albums are saved in a folder inside the folder of the artist
    Album: Same Interpret, Year, Genre, Album Name, Different Track Numbers
    """
    trackList = generateTracklist(artist, album)
    cover = findCover(artist, album)
    for file in glob.glob("*.mp3"):
        title = file.partition(".mp3")[0]
        audiofile = d3.load(file)
        audiofile.tag.genre = genre
        audiofile.tag.release_date = datetime.datetime.now().year
        audiofile.tag.artist = artist
        try:
            trackNum = trackList.index(title.partition(" ft.")[0].partition(" feat.")[0]) + 1  # automation of track numbers
            audiofile.tag.track_num = trackNum
        except:
            print("Error occured, track has to be numbered manually")
            number = input("Enter track number of " + title + " : ")
            audiofile.tag.track_num = int(number)
        audiofile.tag.album = album
        audiofile.tag.images.set(3, open(cover, "rb").read(), "image/jpeg")
        audiofile.tag.title = title
        audiofile.tag.save()
    print("Album named! ")


def generateTracklist(artist, album):
    """
    Using genius.com pattern to get the tracklist of the album.
    """
    base = "https://genius.com/albums"
    url = base + "/" + artist.replace(" ", "-") + "/" + album.replace(" ", "-")
    raw = requests.get(url)
    soup = BeautifulSoup(raw.text, "html.parser")
    try:
        titles = soup.findAll(class_="chart_row-content-title")
        for i in range(len(titles)):
            titles[i] = re.sub(" +", " ", titles[i].text.partition("Lyrics")[0].replace("\n", "").replace("\xa0", " ")).strip()  # das kann noch schöner
            titles[i] = string.capwords(re.sub("[(\[].*?[)\]]", "", titles[i]))  # Cut Features off for better comparison
        if len(titles) == 0:
            print("Could not find titles to album")
        return titles
    except:
        print("Could not find titles to album")


def findCover(artist, album):
    """
    Genius also should work for finding an album cover, single maybe not (too bad resolution).
    """
    # .findAll(class_="cover_art-image")[0]['src']
    # todo: Find a reliable way to get cover in good quality (about 1000 x 1000)
    #  Download cover (at best only temporarily)
    #  Set cover for every track of album (should work with eyed3)
    base = "https://genius.com/albums"
    url = base + "/" + artist.replace(" ", "-") + "/" + album.replace(" ", "-")
    raw = requests.get(url)
    imagePath = "C:/Users/Flavio/Music/Youtube/CoverTemp/"
    soup = BeautifulSoup(raw.text, "html.parser")
    try:
        imageURL = soup.findAll(class_="cover_art-image")[0]['src']
        coverRaw = requests.get(imageURL, stream=True)
        filename = album + ".jpg"
        with open(imagePath + filename, "wb") as outfile:
            coverRaw.raw.decode_content = True
            shutil.copyfileobj(coverRaw.raw,outfile)
            #outfile.write(coverRaw.content)
        print("Cover found!")
        return imagePath + filename
    except:
        print("Error, cover not found")


# Mainloop
while True:
    question = input('Album or Tracks? ')
    # name a couple of tracks
    if question in ["Tracks", "Track", "t", "T", "tr"]:
        os.chdir("C:\\Users\\Flavio\\Music\\Youtube\\Weiteres")
        while True:
            foldername = input("Enter folder name: ")
            if os.path.exists(foldername):
                print("Folder found!")
                nameTracks(foldername)
                break
            else:
                print("Folder not found")
    # name an album
    elif question in ["Album", "a", "A", "al"]:
        os.chdir("C:\\Users\\Flavio\\Music\\Youtube")
        while True:
            albumArtist = input("Which Artist? ")
            albumName = input("Which Album? ")
            if os.path.exists(albumArtist + "\\" + albumName):
                os.chdir(albumArtist + "\\" + albumName)
                specialGenre = input("Name a genre (default: [Hip-Hop/Rap]): ")
                if specialGenre != "":
                    nameAlbum(albumArtist, albumName, specialGenre)
                else:
                    nameAlbum(albumArtist, albumName)
                break
            else:
                print("Artist or Album not found! ")
    # exit
    elif question == "exit":
        exit()
    else:
        print("Please enter valid answer! ")
