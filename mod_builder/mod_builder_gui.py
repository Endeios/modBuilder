import logging
import os.path
import sys
from threading import Thread
from tkinter import Tk, StringVar, DISABLED, ACTIVE, N, S, W, E
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Entry, Label, Button, Frame

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
        self.root = Frame(self, padding=(3, 3, 12, 12))
        self.password = StringVar()
        self.upper_panel = Frame(self.root, padding=(3, 3, 12, 12))
        self.title("Build and install a kernel module")
        self.log_widget = ScrolledText(self.root, height=20, width=80, font=("consolas", "8", "normal"))
        self.execute_build_button = Button(self.upper_panel, text="Execute Build", command=self.run_build)
        self.password_label = Label(self.upper_panel, text="Password", padding=(3, 3, 3, 3))
        self.password_entry = Entry(self.upper_panel, width=7, textvariable=self.password)
        self.redirect_logging()

        self.upper_panel.grid(column=0, row=0, rowspan=1)
        self.log_widget.grid(column=0, row=1, rowspan=3, sticky=N+S+E+W)
        self.root.grid(column=0, row=0, sticky=N+S+E+W)
        self.password_label.grid(column=0, row=0, sticky=N+E+W+S)
        self.password_entry.grid(column=1, row=0, columnspan=3, sticky=N+E+W, padx=10)
        self.execute_build_button.grid(column=0, row=1, columnspan=4, rowspan=2, sticky=N+S+E+W)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.wm_minsize(300, 500)
        self.root.columnconfigure(0, weight=1, minsize=300)
        self.root.rowconfigure(0, weight=1, minsize=100)
        self.root.rowconfigure(1, weight=4, minsize=400)
        self.upper_panel.rowconfigure(0, weight=1)
        self.upper_panel.rowconfigure(1, weight=1)
        self.upper_panel.columnconfigure(0, weight=1)
        self.upper_panel.columnconfigure(1, weight=1)
        self.upper_panel.columnconfigure(2, weight=1)




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


def main():
    app = MainGUI()
    app.mainloop()


if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
