import os
import subprocess

import yaml
import logging

DEFAULT_CONFIG = {
    "mod_folder": "/home/lidia/rtl8852be/",
    "mod_commands": ["make clean", "make -j8"],
    "mod_install_commands": ["sudo -S make install", "sudo -S modprobe 8852be"]
}


def load_config(path):
    logging.debug("Searching config in %s", path)
    if not os.path.exists(path):
        logging.debug("%s does not exist, returning default config", path)
        return DEFAULT_CONFIG
    logging.debug("%s  exist, returning reading config", path)
    with open(path, 'r') as config_file:
        conf = yaml.safe_load(config_file)
        logging.debug("config is legible, returning %s", conf)
        return conf


def build(config):
    """returns true if the build succeeds"""
    try:
        old_wd = os.getcwd()
        os.chdir(config["mod_folder"])
        for command in config["mod_commands"]:
            execute_command(command)
        os.chdir(old_wd)
        return True
    except Exception as error:
        logging.error("Could not execute build!")
        logging.error(error)
        return False


def execute_command(command):
    with subprocess.Popen([command], shell=True, stderr=subprocess.STDOUT,
                          stdout=subprocess.PIPE) as proc:
        log_subprocess_output(proc.stdout)


def execute_input_command(command):
    print("Password:")
    data = input()
    # command = command % data
    logging.debug("Executing: " + command + ", Setting password " + data)
    with subprocess.Popen([command], shell=True, stderr=subprocess.STDOUT,
                          stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True) as proc:
        out_err = proc.communicate(input=data)
        for line in out_err:
            logging.info(line)


def execute_input_command(command, data):
    logging.debug("Executing: " + command + ", Setting password " + data)
    with subprocess.Popen([command], shell=True, stderr=subprocess.STDOUT,
                          stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True) as proc:
        out_err = proc.communicate(input=data)
        for line in out_err:
            logging.info(line)


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        logging.info(line.decode("UTF-8").strip())


def install(config):
    """returns true if the installation succeeds"""
    try:
        old_wd = os.getcwd()
        os.chdir(config["mod_folder"])
        for command in config["mod_install_commands"]:
            execute_input_command(command)
        os.chdir(old_wd)
        return True
    except Exception as error:
        logging.error("Could not finish install!")
        logging.error(error)
        return False


def install_password(config, password):
    """returns true if the installation succeeds"""
    try:
        old_wd = os.getcwd()
        os.chdir(config["mod_folder"])
        for command in config["mod_install_commands"]:
            execute_input_command(command, password)
        os.chdir(old_wd)
        return True
    except Exception as error:
        logging.error("Could not finish install!")
        logging.error(error)
        return False
