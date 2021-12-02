import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./images")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#GUI Starting point
window = tk.Tk() 

#Specified the window size
window.geometry("470x800")
window.configure(bg = "#5C5C5C")

canvas = tk.Canvas(
    window,
    bg = "#5C5C5C",
    height = 800,
    width = 470,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

#function for run the hand tracking program
pid = ()
def run():
    global pid
    pid = subprocess.Popen('start python ./modules/Freedom-Play.py', shell=True)

    print("Freedom-Play module started")
    print("Start PID : " , pid.pid)
     

#logo image
logo_img = tk.PhotoImage(
    file=relative_to_assets("logo.png"))
logo = canvas.create_image(
    99.0,
    105.0,
    image=logo_img
)

#play button
play_img = tk.PhotoImage(
    file=relative_to_assets("play.png"))
play_btn = tk.Button(
    image=play_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: run(),
    relief="flat"
)
play_btn.place(
    x=207.0,
    y=64.0,
    width=109.0,
    height=74.0
)

#info button
info_img = tk.PhotoImage(
    file=relative_to_assets("info.png"))
info_btn = tk.Button(
    image=info_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
info_btn.place(
    x=342.0,
    y=64.0,
    width=109.0,
    height=74.0
)

#checkbox
entry_image_1 = tk.PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    396.0,
    174.5,
    image=entry_image_1
)
entry_1 = tk.Text(
    bd=0,
    bg="#E5E5E5",
    highlightthickness=0
)
entry_1.place(
    x=209.0,
    y=157.0,
    width=374.0,
    height=33.0
)

canvas.create_rectangle(
    435.0,
    166.0,
    451.0,
    182.0,
    fill="#C4C4C4",
    outline="")

#instruction part
canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    246.0,
    470.0,
    765.0,
    fill="#333333",
    outline="")

#instruction image slide
image_image_1 = tk.PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    175.0,
    506.0,
    image=image_image_1
)

#next image button
next_img = tk.PhotoImage(
    file=relative_to_assets("next.png"))
next_btn = tk.Button(
    image=next_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("next_btn clicked"),
    relief="flat"
)
next_btn.place(
    x=372.0,
    y=391.0,
    width=79.0,
    height=99.0
)

#prev image button
prev_img = tk.PhotoImage(
    file=relative_to_assets("prev.png"))
prev_btn = tk.Button(
    image=prev_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("prev_btn clicked"),
    relief="flat"
)
prev_btn.place(
    x=372.0,
    y=521.0,
    width=79.0,
    height=99.0
)


window.resizable(False, False)
window.mainloop() #GUI end

# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer