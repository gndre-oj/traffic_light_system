# -*- coding: utf-8 -*-

try:
    import tkinter as tk
    from tkinter import *
    from tkinter import ttk
    from PIL import Image, ImageTk, ImageOps
    import time

except ImportError:
    from subprocess import call
    from tkinter import StringVar, ttk, Tk


    def download():
        text_var.set("Der Download beginnt...")
        fenster.update()
        call("curl https://bootstrap.pypa.io/get-pip.py -o get -pip.py")
        call("python -m pip install -I pip")
        call("pip install pillow")
        text_var.set("Download abgeschlossen.")
        fenster.update()
        fenster.after(5000, fenster.destroy)


    fenster = Tk()
    fenster.config(bg="#3b3b3b")
    text_var = StringVar()
    text_var.set("Fehlende Daten downloaden?")
    ttk.Label(fenster, textvariable=text_var).grid(column=0, row=0, pady=4, padx=4)
    ttk.Button(fenster, text="Download", command=download).grid(column=0, row=1, pady=4, padx=4)


class Ampel:
    def __init__(self, state_number):
        self.state_number = state_number
        self.state = 0
        self.sleep = 0

    def is_ready(self):
        """
        Returns true, if the next phase can be set
        """
        return int(time.time()) >= self.sleep

    def next(self, wait):
        """
        Sets the next state and the new wait time for the state

        params wait - Wait time in seconds
        """

        self.state = (self.state + 1) % self.state_number
        self.sleep = int(time.time()) + wait


class Traffic_Light:

    def __init__(self, master):

        self.master = master

        w = 1000
        h = 1000
        self.x = w / 2
        self.y = w / 2

        # self.tk = tk.Tk()
        # self.tk.title("Traffic Light")
        # self.tk.geometry("1000x1000+0+0")

        self.toplevel = tk.Toplevel(master)
        self.toplevel.geometry("+%d+%d" % (1010, 0))
        self.toplevel.title("Steuerzentrale")

        self.style = ttk.Style(self.toplevel)
        self.style.theme_use('clam')

        self.scrollbar = tk.Scrollbar(master, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.c = tk.Canvas(master, width=w, height=h, scrollregion=(0, 0, 1000, 1000),
                           yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.c.yview)
        self.c.pack()

        self.checkbox_var = tk.IntVar()
        # self.text_var = tk.StringVar()
        # self.text_var.set("Schaltung Aus")
        global is_on
        is_on = False

        self.ampelAn = Ampel(5)
        self.ampelAus = Ampel(2)

        self.__build()

    def circuit_default(self):
        add = 0
        global is_on

        if is_on:
            if not self.ampelAn.is_ready():
                return

            if self.ampelAn.state == 0:
                self.c.itemconfigure(self.top, image=self.r_top)
                self.c.itemconfigure(self.bottom, image=self.r_bottom)
                self.c.itemconfigure(self.right, image=self.g_right)
                self.c.itemconfigure(self.left, image=self.g_left)
                self.c.update()

                add = 5

            elif self.ampelAn.state == 1:
                self.c.itemconfigure(self.top, image=self.r_y_top)
                self.c.itemconfigure(self.bottom, image=self.r_y_bottom)
                self.c.itemconfigure(self.right, image=self.y_right)
                self.c.itemconfigure(self.left, image=self.y_left)
                self.c.update()

                add = 1

            elif self.ampelAn.state == 2:
                self.c.itemconfigure(self.top, image=self.g_top)
                self.c.itemconfigure(self.bottom, image=self.g_bottom)
                self.c.itemconfigure(self.right, image=self.r_right)
                self.c.itemconfigure(self.left, image=self.r_left)
                self.c.update()

                add = 5

            elif self.ampelAn.state == 3:
                self.c.itemconfigure(self.top, image=self.y_top)
                self.c.itemconfigure(self.bottom, image=self.y_bottom)
                self.c.itemconfigure(self.right, image=self.r_y_right)
                self.c.itemconfigure(self.left, image=self.r_y_left)
                self.c.update()

                add = 1

            elif self.ampelAn.state == 4:
                self.c.itemconfigure(self.top, image=self.r_top)
                self.c.itemconfigure(self.bottom, image=self.r_bottom)
                self.c.itemconfigure(self.right, image=self.g_right)
                self.c.itemconfigure(self.left, image=self.g_left)
                self.c.update()

                add = 5

            self.ampelAn.next(add)
        else:
            if not self.ampelAus.is_ready():
                return

            if self.ampelAus.state == 0:
                self.c.itemconfigure(self.top, image=self.y_top)
                self.c.itemconfigure(self.bottom, image=self.y_bottom)
                self.c.itemconfigure(self.right, image=self.y_right)
                self.c.itemconfigure(self.left, image=self.y_left)
                self.c.update()

            elif self.ampelAus.state == 1:
                self.c.itemconfigure(self.top, image=self.off_top)
                self.c.itemconfigure(self.bottom, image=self.off_bottom)
                self.c.itemconfigure(self.right, image=self.off_right)
                self.c.itemconfigure(self.left, image=self.off_left)
                self.c.update()

            self.ampelAus.next(1)

    def __build(self):
        def switch():
            global is_on

            if is_on:
                switch_button.config(image=self.img_off)
                is_on = False
            else:
                switch_button.config(image=self.img_on)
                is_on = True

        #
        # Achtung! Bei Tonny "r"traffic_light_system\" aus Image.open entfernen
        #

        # Create Crossing
        old_crossing = (Image.open(r"img\kreuzung.jpg"))
        resized_crossing = old_crossing.resize((1000, 1000), Image.ANTIALIAS)
        self.new_crossing = ImageTk.PhotoImage(resized_crossing)
        self.c.create_image(500, 500, anchor="center", image=self.new_crossing)

        img_on = (Image.open(r"img\on.png"))
        self.img_on = ImageTk.PhotoImage(img_on)
        img_off = (Image.open(r"img\off_button.png"))
        self.img_off = ImageTk.PhotoImage(img_off)

        self.img_var = self.img_off

        # Open Images Vertical
        old_r = (Image.open(r"img\red.png"))
        old_r_y = (Image.open(r"img\red_yellow.png"))
        old_y = (Image.open(r"img\yellow.png"))
        old_g = (Image.open(r"img\green.png"))
        old_off = (Image.open(r"img\off.png"))

        # Edit (Flip) Vertical Images
        r_flip = ImageOps.flip(old_r)
        r_y_flip = ImageOps.flip(old_r_y)
        y_flip = ImageOps.flip(old_y)
        g_flip = ImageOps.flip(old_g)
        off_flip = ImageOps.flip(old_off)

        # Open Horizontal Images
        old_r_h = (Image.open(r"img\red_hori.png"))
        old_r_y_h = (Image.open(r"img\red_yellow_hori.png"))
        old_y_h = (Image.open(r"img\yellow_hori.png"))
        old_g_h = (Image.open(r"img\green_hori.png"))
        old_off_h = (Image.open(r"img\off_hori.png"))

        # Edit (Mirror) HorizontalImages
        r_mirror = ImageOps.mirror(old_r_h)
        r_y_mirror = ImageOps.mirror(old_r_y_h)
        y_mirror = ImageOps.mirror(old_y_h)
        g_mirror = ImageOps.mirror(old_g_h)
        off_mirror = ImageOps.mirror(old_off_h)

        # Create Var's for Traffic Lights Top, Bottom, Right, Left
        self.r_bottom = ImageTk.PhotoImage(old_r)
        self.r_y_bottom = ImageTk.PhotoImage(old_r_y)
        self.y_bottom = ImageTk.PhotoImage(old_y)
        self.g_bottom = ImageTk.PhotoImage(old_g)
        self.off_bottom = ImageTk.PhotoImage(old_off)

        self.r_top = ImageTk.PhotoImage(r_flip)
        self.r_y_top = ImageTk.PhotoImage(r_y_flip)
        self.y_top = ImageTk.PhotoImage(y_flip)
        self.g_top = ImageTk.PhotoImage(g_flip)
        self.off_top = ImageTk.PhotoImage(off_flip)

        self.r_right = ImageTk.PhotoImage(old_r_h)
        self.r_y_right = ImageTk.PhotoImage(old_r_y_h)
        self.y_right = ImageTk.PhotoImage(old_y_h)
        self.g_right = ImageTk.PhotoImage(old_g_h)
        self.off_right = ImageTk.PhotoImage(old_off_h)

        self.r_left = ImageTk.PhotoImage(r_mirror)
        self.r_y_left = ImageTk.PhotoImage(r_y_mirror)
        self.y_left = ImageTk.PhotoImage(y_mirror)
        self.g_left = ImageTk.PhotoImage(g_mirror)
        self.off_left = ImageTk.PhotoImage(off_mirror)

        # Create First Traffic Light (Top, Bottom, Right, Left) in state off
        self.top = self.c.create_image(310, 140, anchor="nw", image=self.off_top)
        self.bottom = self.c.create_image(650, 765, anchor="nw", image=self.off_bottom)
        self.right = self.c.create_image(765, 310, anchor="nw", image=self.off_right)
        self.left = self.c.create_image(140, 650, anchor="nw", image=self.off_left)

        # Create Button
        switch_button = Button(self.toplevel, image=self.img_off, borderwidth=0, command=switch)
        switch_button.pack(pady=10)

        # ttk.Button(self.toplevel, text="Quit", command=self.master.destroy).pack(padx=4, pady=4)


def main():
    root = tk.Tk()
    root.title("Traffic Light")
    root.geometry("1000x1000+0+0")

    app = Traffic_Light(root)
    root.update_idletasks()

    while True:
        app.circuit_default()
        root.update()


if __name__ == "__main__":
    main()