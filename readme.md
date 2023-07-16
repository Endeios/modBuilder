# Complies and installs a kernel module from gui, with one click

I made this program for my mum, so she can use her new pc
with her fancy new wi-fi, not in kernel 5.18+. She needs
something that one can just click after kernel update.

She has https://github.com/HRex39/rtl8852be

## Prerequisites

- all the needed building software is installed
- the module is already checked out

## Create virtual environment

Create virtualenev

```bash
virtualenv venv
```

and install dependencies
```bash
./venv/bin activate
pip install -r requirements.txt
```

## Build options

1. wheel 
```bash
python -m build
```
2. pynstaller

```bash
pyinstaller --onefile mod_builder/app.py
```
