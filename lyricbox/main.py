from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

import requests

root = Tk()
root.title('Lyric Box')
root.iconbitmap(r"images\songwriter.ico")
root.geometry("400x600")


# button command


def getlyrics():
    artist = artistName.get()
    title = songName.get()
    url = r"https://api.lyrics.ovh/v1/" + artist + "/" + title

    response = requests.get(url)
    lyrics = str(response.content)
    lyrics = (lyrics[13:-3])
    lyrics = lyrics.replace(r"\\n", "\n").replace("\\", "")

    mylabel3 = Label(second_frame,text="LYRICS :")
    mylabel3.grid(row=6,column=0)
    mylabel4 = Label(second_frame, text="------------------------")
    mylabel4.grid(row=7, column=0)

    mylabel5 = Label(second_frame, text=lyrics)
    mylabel5.grid(row=8, column=0)

    mylabel6 = Label(second_frame, text="------------------------")
    mylabel6.grid(row=9, column=0,pady=10)


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
go_Btn = Button(second_frame, text="Go!", command=getlyrics)

# GRID
imageLabel.grid(row=0, column=0, pady=(20, 10))
myLabel1.grid(row=1, column=0, pady=(20, 10), padx=140)
songName.grid(row=2, column=0, padx=10, pady=(0, 10))
myLabel2.grid(row=3, column=0, pady=(20, 10))
artistName.grid(row=4, column=0, padx=10, pady=(0, 10))
go_Btn.grid(row=5, column=0, pady=(0, 20))

root.mainloop()
