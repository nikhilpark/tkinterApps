from tkinter import Tk, ttk, Label, Frame, BOTH, Canvas, LEFT, VERTICAL, RIGHT, Y, Entry, Button
from io import BytesIO
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import requests
import threading
global albumartimg, artist, title, albumname, lyrics

root = Tk()
root.title('Lyric Box')
root.iconbitmap(r"images\songwriter.ico")
root.geometry("450x600")




def getinput():

    global title
    global artist

    title = songName.get()
    artist = artistName.get()


def getalbumname():

    global albumname

    urlalbum = requests.get(
       "https://www.last.fm/music/" + artist.replace(" ", "+")
       + "/_/" + title.replace(" ", "+") + "/+albums",
       timeout=10
    )

    srcc = urlalbum.content
    soupp = BeautifulSoup(srcc, 'lxml')
    albumname = soupp.find_all("a", {"class": "link-block-target"})[0]

    albumname = str(albumname)
    loc = albumname.find("url") + 5
    albumname = (albumname[loc:-4])


def getalbumart():
    global albumartimg
    urlalbumart = requests.get(
        "https://www.last.fm/music/" + artist.replace(" ", "+")
        + "/" + albumname.replace(" ", "+") + "/+images",
        timeout=10
    )
    src = urlalbumart.content
    soup = BeautifulSoup(src, 'lxml')
    albumart = soup.find_all("a", {"class": "image-list-item"})[0]
    albumart = (str(albumart))
    locate = albumart.find("src") + 5
    albumart = (albumart[locate:-8]) + ".png"
    imgresponse = requests.get(albumart)
    img_data = imgresponse.content

    albumartimg = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))


def getlyrics():

    global lyrics

    url = r"https://api.lyrics.ovh/v1/" + artist + "/" + title

    response = requests.get(url)
    lyrics = str(response.content)
    lyrics = (lyrics[13:-3])
    lyrics = lyrics.replace(r"\\n", "\n").replace("\\r", "")
    lyrics = lyrics.replace("\\", "").replace("xe2x80x85", "").replace("xc2x85", "")


def printstuff():

    artlabel = Label(second_frame, image=albumartimg)
    artlabel.grid(row=0, column=0, pady=(20, 10))

    mylabel3 = Label(
        second_frame, text=artist.capitalize() + " - " + title.capitalize() + " (" + albumname + ") " + "\n\nLYRICS :"
    )
    mylabel3.grid(row=8, column=0)

    mylabel4 = Label(second_frame, text="------------------------")
    mylabel4.grid(row=9, column=0)

    mylabel5 = Label(second_frame, text=lyrics)
    mylabel5.grid(row=10, column=0, padx=10)

    mylabel6 = Label(second_frame, text="------------------------")
    mylabel6.grid(row=11, column=0, pady=10)


def buttonaction():

    message = "Not found! try different input"

    mylabel7 = Label(second_frame, text="Processing... ")
    mylabel7.grid(row=8, column=0)

    getinput()
    getalbumname()
    try:
        getalbumname()
        
    except IndexError:
        print("Error grabbing albumname")
        mylabel8 = Label(second_frame, text=message)
        mylabel8.grid(row=8, column=0)
        exit()

    try:
        getalbumart()
    except IndexError:
        print("Error grabbing albumart")

        mylabel8 = Label(second_frame, text=message)
        mylabel8.grid(row=8, column=0)
        exit()

    try:
        getlyrics()
    except IndexError:
        print("Error grabbing lyrics")
        mylabel8 = Label(second_frame, text=message)
        mylabel8.grid(row=8, column=0)
        exit()

    printstuff()


'''
                                           FULL SCREEN SCROLL BAR STARTS
                                                                                                    '''
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

second_frame = Frame(my_canvas)

my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

'''
                               FULL SCROLL BAR ENDS
                                                                                           '''
# IMAGE
my_img1 = ImageTk.PhotoImage(Image.open(r"images\lyric_box.jpg"))
imageLabel = Label(second_frame, image=my_img1)

# INPUT
myLabel1 = Label(second_frame, text="Enter name of the song")
songName = Entry(second_frame, width=50, borderwidth=5)

myLabel2 = Label(second_frame, text="Enter name of Artist")
artistName = Entry(second_frame, width=50, borderwidth=5)


# BUTTON
go_Btn = Button(second_frame, text="Go!", command=lambda: threading.Thread(target=buttonaction).start())

# GRID
imageLabel.grid(row=0, column=0, pady=(20, 10))
myLabel1.grid(row=1, column=0, pady=(20, 10), padx=160)
songName.grid(row=2, column=0, padx=10, pady=(0, 10))

myLabel2.grid(row=3, column=0, pady=(20, 10))
artistName.grid(row=4, column=0, padx=10, pady=(0, 10))


go_Btn.grid(row=7, column=0, pady=(0, 20))

root.mainloop()
