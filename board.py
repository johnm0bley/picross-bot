# coding: utf-8

import re
import json
import requests
import pandas as pd
import numpy as np

import picrossbot

INFO_URL = "https://www.minicgi.net/logic/logic_feed.cgi?num=42467"

class Board():

    def __init__(self):

        self.bot = picrossbot.PicrossBot()
        self.info = self.get_game_info()

        # length of X and Y
        self.size = self.info["num"]

        self.height = self.info["height"]
        self.width = self.info["width"]

        # made a dict for clues X1 to Yn
        self.clues = dict(zip(
            ["X"+str(i+1) for i in range(self.size)]+\
            ["Y"+str(j+1) for j in range(self.size)],
            [s for s in self.info["stage"]]
        ))

        # made a dataframe X1 to Yn
        self.sheet = pd.DataFrame(
            np.zeros((self.size, self.size), dtype=int),
            columns=["X"+str(i+1) for i in range(self.size)],
            index=["Y"+str(j+1) for j in range(self.size)]
        )

    # get some infomations(size, clues) of from page and define each.
    def get_game_info(self):

        res = requests.get(INFO_URL)

        # reject words outside of "{" and "}"
        info = re.search(r"{(.+)}", res.text).group()

        # add "" to each key words and modifing to dict
        json_text = re.sub("(\w+):", r'"\1":', info)
        game_info = json.loads(json_text)

        return game_info

    def fill_absolute(self, line_name):

        check_list = []
        where_to_start = 0
        absolute_cell = np.zeros(self.size, dtype=int)

        while True:

            index = where_to_start
            possible_line = np.zeros(self.size, dtype=int)

            # find may can paint and add to list
            for clue in self.clues[line_name]: # pick a clue
                for i in range(clue):
                    possible_line[index] = 1
                    index += 1
                index += 1

            # flip the list and sum together
            check_list.append(possible_line)

            if index > self.size:
                break
            else:
                where_to_start += 1

        for i, b in enumerate(np.sum(np.array(check_list), axis=0)):

            if line_name[0] == "X":

                if b == len(check_list):

                    if self.sheet[line_name][i] == 0:
                        self.sheet[line_name][i] = 1
                        self.bot.fill_cell(line_name, i)

                elif b == 0:

                    if self.sheet[line_name][i] == 0:
                        self.sheet[line_name][i] = -1
                        self.bot.close_cell(line_name, i)

            elif line_name[0] == "Y":

                if b == len(check_list):

                    if self.sheet.loc[line_name][i] == 0:
                        self.sheet.loc[line_name][i] = 1
                        self.bot.fill_cell(line_name, i)

                elif b == 0:

                    if self.sheet.loc[line_name][i] == 0:
                        self.sheet.loc[line_name][i] = -1
                        self.bot.close_cell(line_name, i)

    def close_absolute(self, line_name):

        where_to_where = []
        original_line = self.sheet[line_name].values
        possible_line = np.zeros(self.size, dtype=int)

        for i in range(self.clues[line_name][0]):
            possible_line[i] = 1

        for i in range(self.clues[line_name][-1]):
            possible_line[-(i+1)] = 1

        check_line = np.sum(np.vstack((original_line, possible_line)), axis=0)

        for i in range(self.size):
            if check_line[i] == 2:
                where_to_where.append(i)

        print(check_line)
        print(where_to_where)
        print("")

        # print(check_line, self.clues[line_name][0], self.clues[line_name][-1])
