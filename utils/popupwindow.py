from tkinter import *
import customtkinter

class PopupWindow:
    def __init__(self, master, title, message):
        self.master = master
        self.title = title
        self.message = message
        self.popup = Toplevel(self.master)
        self.popup.title(self.title)
        self.popup.geometry("300x100")
        self.popup.resizable(False, False)
        self.popup.grab_set()
        self.popup.focus_set()
        self.popup.transient(master)
        self.popup.protocol("WM_DELETE_WINDOW", self.close)
        self.label = customtkinter.CTkLabel(self.popup, text=self.message)
        self.label.pack()

        # Add an Entry widget to receive user input
        self.user_input = StringVar()
        self.entry = Entry(self.popup, textvariable=self.user_input)
        self.entry.pack()

        self.button = customtkinter.CTkButton(self.popup, text="OK", command=self.close)
        self.button.pack()

    def close(self):
        self.popup.destroy()
        self.master.destroy()

    def get_user_input(self):
        return self.user_input.get()
