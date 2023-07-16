import logging
import os.path
import sys
from threading import Thread
from tkinter import Tk, Button, Frame, StringVar, DISABLED, ACTIVE
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Entry, Label

from mod_builder import builder

logging.root.setLevel(logging.DEBUG)


class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class MainGUI(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.root = Frame(self)
        self.geometry("600x600")
        self.title("Build and install a kernel module")
        self.log_widget = ScrolledText(self.root, height=40, width=120, font=("consolas", "8", "normal"))
        self.root.pack()
        self.redirect_logging()
        self.execute_build_button = Button(self.root, text="Execute Build", command=self.run_build)
        self.password = StringVar()
        self.password_label = Label(self.root, text="Password")
        self.password_entry = Entry(self.root, width=7, textvariable=self.password)
        self.password_label.pack()
        self.password_entry.pack()
        self.execute_build_button.pack()
        self.log_widget.pack()

    def redirect_logging(self):
        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger

    def run_build(self):
        send_process = Thread(target=lambda: run(self.password.get(), self.enable_button))
        send_process.start()
        self.execute_build_button['state'] = DISABLED

    def enable_button(self):
        self.execute_build_button['state'] = ACTIVE


def run(password, callback):
    file_name = os.path.join(os.getcwd(), "mod_builder_conf.yaml")
    conf = builder.load_config(file_name)
    builder.build(conf)
    builder.install_password(conf, password)
    callback()


if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
