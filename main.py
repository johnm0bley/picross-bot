# coding: utf-8

import board

if __name__ == "__main__":

    # create a instance
    board = board.Board()

    # start to process
    while True:

        # X
        for i in range(board.size):

            index = "X" + str(i+1)
            board.fill_absolute(index)

            index = "Y" + str(i+1)
            board.fill_absolute(index)

        for i in range(board.size):
            index = "X" + str(i+1)

            board.close_absolute(index)

        break

    print(board.sheet.values)
