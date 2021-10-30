# coding: utf-8

import time
from selenium import webdriver
import chromedriver_binary
import pyautogui

import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")

GAME_URL = config_ini.get("DEFAULT", "game")
X_HOME = int(config_ini.get("DEFAULT", "x_home"))
Y_HOME = int(config_ini.get("DEFAULT", "y_home"))

class PicrossBot():

    def __init__(self):

        self.open_game()

    def open_game(self):

        options = webdriver.ChromeOptions()
        options.add_argument("--start-fullscreen")
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(GAME_URL)

    def fill_cell(self, line_name, i):

        dir = line_name[0]
        if dir == "X":
            x = X_HOME + (int(line_name[1:])-1) * 18
            y = Y_HOME + i * 18
        elif dir == "Y":
            x = X_HOME + i * 18
            y = Y_HOME + (int(line_name[1:])-1) * 18

        time.sleep(0.1)
        pyautogui.click(x, y)

    def close_cell(self, line_name, i):

        dir = line_name[0]
        if dir == "X":
            x = X_HOME + (int(line_name[1:])-1) * 18
            y = Y_HOME + i * 18
        elif dir == "Y":
            x = X_HOME + i * 18
            y = Y_HOME + (int(line_name[1:])-1) * 18

        time.sleep(0.1)
        pyautogui.rightClick(x, y)
