from tkinter import *
import customtkinter

class PopupWindow:
    def __init__(self, master, title, message, itens=None):
        self.master = master
        self.title = title
        self.message = message
        self.popup = Toplevel(self.master)
        self.popup.title(self.title)
        if itens:
            self.popup.geometry("500x150")
            self.has_listbox = True
        else:
            self.popup.geometry("500x100")
            self.has_listbox = False
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

        # Add a Listbox widget to display a list of items
        if itens:
            self.listbox = Listbox(self.popup, height=3, width=20)
            for item in itens:
                self.listbox.insert(END, item)
            self.listbox.pack()

        self.button = customtkinter.CTkButton(self.popup, text="OK", command=self.close)
        self.button.pack()

    # Close the popup window and saves the user input from the listbox
    def close(self):
        if self.has_listbox:
            self.listbox_value = self.get_listbox_selection()
        self.popup.destroy()

    # Get the selected value from the listbox while the window is on
    def get_listbox_selection(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            selected_value = self.listbox.get(index)
            return selected_value
        else:
            return None

    # Get the user input from the Entry widget and the selected value from the Listbox widget
    def get_user_input(self):
        if self.has_listbox:
            return self.user_input.get(), self.listbox_value
        return self.user_input.get()
