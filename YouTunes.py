# coding: utf-8
# Goal: Rename multiple mp3 files with their properties to get them ready for iTunes

"""
Idea space:
- Ask user to delete the Cover_Images folder on end
"""

import eyed3 as d3
import os, os.path, datetime, requests, re, string, PIL.Image, youtube_dl
from bs4 import BeautifulSoup

# path = "C:\\Users\\Flavio\\Music\\Youtube\\Weiteres"
# os.chdir(path)
d3.log.setLevel("ERROR")  # So there are no warnings for non-standard genres


def nameTracks(folderpath, genre="[Hip-Hop/Rap]"):
    """ Tracks are saved as "Artist - TrackName"
    Tracks: Option for same genre, all title numbers get a 1, same year, different artists, track name, album like "Track Name - Single"
    """
    for file in os.listdir(folderpath):
        if file.endswith(".mp3"):
            if file.find("-") != -1:
                filepath = folderpath + "/" + file
                trackArtist = file.partition("-")[0].strip()
                title = file.partition(" - ")[2].partition('.mp3')[0].strip()
                singleCover = findSingleCover(trackArtist, title)
                audiofile = d3.load(filepath)
                audiofile.tag.genre = genre
                audiofile.tag.release_date = datetime.datetime.now().year  # bug: year is shown on windows explorer but not in iTunes, same string
                audiofile.tag.artist = trackArtist
                audiofile.tag.track_num = 1
                if title.find(" ft.") != -1:  # cut off features als well for the album name
                    audiofile.tag.album = title.partition(" ft.")[0] + " - Single"
                else:
                    audiofile.tag.album = title + ' - Single'
                if singleCover != "Error":
                    audiofile.tag.images.set(3, open(singleCover, "rb").read(), "image/jpeg")
                audiofile.tag.title = title
                audiofile.tag.save()
                # also rename the whole file to have just the title of the track
                os.rename(filepath, folderpath + "/" + title + ".mp3")
            else:
                print("File already formatted or not named properly! ")
        else:
            print("File not formatted because not mp3!")
    print("All Tracks managed! ")


def nameAlbum(folderpath, artist, album, genre="[Hip-Hop/Rap]"):
    """ Albums are saved in a folder inside the folder of the artist
    Album: Same Interpret, Year, Genre, Album Name, Different Track Numbers
    """
    trackList = generateTracklist(artist, album)
    cover = findAlbumCover(artist, album)
    for file in os.listdir(folderpath):
        if file.endswith(".mp3"):
            title = file.partition(".mp3")[0]
            audiofile = d3.load(folderpath + "/" + file)
            audiofile.tag.genre = genre
            audiofile.tag.release_date = datetime.datetime.now().year
            audiofile.tag.artist = artist
            try:
                # todo: Check so machen, dass nur groß oder nur kleinschreibung angeschaut werden und Zeichen wie ' berücksichtigen
                trackNum = trackList.index(string.capwords(title.partition(" ft.")[0].partition(" feat.")[0])) + 1  # automation of track numbers
                audiofile.tag.track_num = trackNum
            except:
                print("Error occured, track has to be numbered manually")
                number = input("Enter track number of " + title + " : ")
                audiofile.tag.track_num = int(number)
            audiofile.tag.album = album
            if cover != "Error":
                audiofile.tag.images.set(3, open(cover, "rb").read(), "image/jpeg")
            audiofile.tag.title = title
            audiofile.tag.save()
    print("Album finished! ")


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
            titles[i] = re.sub(" +", " ", titles[i].text.partition("Lyrics")[0].replace("\n", "").replace("\xa0", " ")).replace("’", "").strip()  # das kann noch schöner
            # Cut Features off for better comparison
            titles[i] = string.capwords(re.sub("[(\[].*?[)\]]", "", titles[i]).strip())
        if len(titles) == 0:
            print("Could not find titles to album")
        return titles
    except:
        print("Could not find titles to album")


def findAlbumCover(artist, album):
    """
    Using genius.com to find the album cover to given Artist and album
    """
    base = "https://genius.com/albums"
    url = base + "/" + artist.replace(" ", "-") + "/" + album.replace(" ", "-")
    raw = requests.get(url)
    #imagePath = "C:/Users/Flavio/Music/Youtube/CoverTemp/"
    imagePath = getcwdFormat() + "/" + "Cover_Images/"
    if not os.path.exists("Cover_Images"):
        os.mkdir("Cover_Images")
    soup = BeautifulSoup(raw.text, "html.parser")
    try:
        imageURL = soup.findAll(
            class_="cover_art-image")[0]['srcset'].split(" ")[0]  # fucking bullshit
        splittedLink = imageURL.split("/")
        # Download images in 1000x1000 resolution
        splittedLink[4] = "1000x1000"
        imageURL = "/".join(splittedLink)
        coverRaw = requests.get(imageURL, stream=True)
        filename = artist + "-" + album + ".jpg"
        with open(imagePath + filename, "wb") as outfile:
            for block in coverRaw.iter_content(1024):
                if not block:
                    break
                outfile.write(block)
        print("Cover found! Resolution is: " +
              str(PIL.Image.open(imagePath + filename).size))
        return imagePath + filename
    except:
        print("Error, cover not found")
        return "Error"


def findSingleCover(artist, single):
    """
    Using genius.com to find the song cover to given Artist and song
    """
    base = "https://genius.com/"
    url = base + artist.replace(" ", "-") + "-" + single.replace(",","").replace(" ", "-") + "-lyrics"
    raw = requests.get(url)
    # imagePath = "C:/Users/Flavio/Music/Youtube/CoverTemp/"
    imagePath = getcwdFormat() + "/" + "Cover_Images/"
    if not os.path.exists("Cover_Images"):
        os.mkdir("Cover_Images")
    soup = BeautifulSoup(raw.text, "html.parser")
    try:
        imageURL = soup.findAll(class_="cover_art-image")[0]["src"]
        splittedLink = imageURL.split("/")
        # Download images in 1000x1000 resolution
        splittedLink[4] = "1000x1000"
        imageURL = "/".join(splittedLink)
        coverRaw = requests.get(imageURL, stream=True)
        filename = artist + "-" + single + ".jpg"
        with open(imagePath + filename, "wb") as outfile:
            for block in coverRaw.iter_content(1024):
                if not block:
                    break
                outfile.write(block)
        print("Cover found for track " + single)
        return imagePath + filename
    except:
        print("Error, cover not found for track " + single)
        return "Error"


# Download lsit of URLs
def downLoadTracks(trackList, folder=""):
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    for i in range(len(trackList)):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                # result = ydl.extract_info("{}".format(trackList[i]))
                # filename = ydl.prepare_filename(result)
                ydl.download([trackList[i]])
            except:
                print("Could not download track!")
                pass
    for file in (os.listdir(getcwdFormat())):
        if file.endswith(".mp3"):
            try:
                os.rename(getcwdFormat() + "/" + file, getcwdFormat() + "/" + folder + "/" + renameDownloadTrack(file))
            except:
                print("File already exists!")
                pass


# Deletes the url id of youtube_dl and cuts off things in brackets like (Audio) because no one wants this
def renameDownloadTrack(trackName):
    trackName = re.sub("[(\[].*?[)\]]", "", trackName[0:trackName.rindex("-")]).strip()
    return re.sub(' +', ' ', trackName) + ".mp3"


# Make os path suitable for python chdir
def pathReplace(path):
    path = path.replace("\\", "/")
    return path

# Get cwd with right format
def getcwdFormat():
    cwd = os.getcwd().replace("\\", "/")
    return cwd

# Get new foldername
def getnewFolder(folder):
    folderFound = False
    i = 1
    while not folderFound:
        if os.path.exists(folder+str(i)):
            i = i+1
        else:
            folderFound = True
    return folder + "(" + str(i) + ")"

# Mainloop
print("Welcome to YouTunes!")
while True:
    question = input("Download Tracks or album? ")
    # name a couple of tracks
    if question in ["Tracks", "Track", "t", "T", "tr"]:
        folderName = "Singles - " + str(datetime.date.today())
        if os.path.exists(folderName):
            folderName = getnewFolder(folderName)
            os.mkdir(folderName)
        else:
            os.mkdir(folderName)
        folderPath = getcwdFormat() + "/" + folderName
        track_urls = []
        question = input("Enter a song url or \"finish\": ")
        while question not in ["f", "finished", "fi", "finish"]:
            track_urls.append(question)
            question = input("Enter a song url or \"finish\": ")
        downLoadTracks(track_urls, folderName)
        print("Make sure every Track is named like Artist - TrackName Features")
        print("Example: Drake - Sneakin feat. 21 Savage")
        print("If Track has correct name just press enter, otherwise enter correct name and then enter")
        for mp3 in (os.listdir(folderPath)):
            if mp3.endswith(".mp3"):
                print(mp3)
                newname = input("Enter or new name: ")
                if newname == "":
                    pass
                else:
                    os.rename(getcwdFormat() + "/" + folderName + "/" + mp3, getcwdFormat() + "/" + folderName + "/" + newname + ".mp3")
                    print("Saved new name!")
        print("Every file in folder " + folderName + " has been named.")
        print("Next up: Setting the stats for iTunes")  # todo Manage different genres here
        nameTracks(folderPath)
        print("You can quit now or download more tracks or albums: ")
    # name an album
    elif question in ["Album", "a", "A", "al"]:
        # os.chdir("C:\\Users\\Flavio\\Music\\Youtube")
        albumArtist = input("Which Artist? ")
        albumName = input("Which Album? ")
        folderName = albumArtist + " - " + albumName
        if os.path.exists(folderName):
            folderName = getnewFolder(folderName)
            os.mkdir(folderName)
        else:
            os.mkdir(folderName)
        folderPath = getcwdFormat() + "/" + folderName
        track_urls = []
        question = input("Enter a song url or \"finish\": ")
        while question not in ["f", "finished", "fi", "finish", "fin"]:
            track_urls.append(question)
            question = input("Enter a album song url or \"finish\": ")
        downLoadTracks(track_urls, folderName)
        print("Make sure every Track is named like Artist - TrackName Features")
        print("Example: Drake - Sneakin feat. 21 Savage")
        print("If Track has correct name just press enter, otherwise enter correct name and then enter")
        for mp3 in (os.listdir(folderPath)):
            if mp3.endswith(".mp3"):
                print(mp3.split(" - ")[1])
                newname = input("Enter or new name: ")
                if newname == "":
                    os.rename(getcwdFormat() + "/" + folderName + "/" + mp3, getcwdFormat() + "/" + folderName + "/" + mp3.split(" - ")[1] + ".mp3")
                else:
                    os.rename(getcwdFormat() + "/" + folderName + "/" + mp3, getcwdFormat() + "/" + folderName + "/" + newname + ".mp3")
                    print("Saved new name!")
        specialGenre = input("Name a genre (default: [Hip-Hop/Rap]): ")
        print("Now doing the iTunes stats")
        if specialGenre != "":
            nameAlbum(folderPath, albumArtist, albumName, specialGenre)
        else:
            nameAlbum(folderPath, albumArtist, albumName)
        print("You can quit now or download more tracks or albums: ")
    # exit
    elif question == "exit":
        exit()
    else:
        print("Please enter valid answer or \"exit\" to exit! ")
