#!/usr/bin/python
# -*- coding: utf8 -*-

#################################################################
# File name: digit_recognizer_testing.py                        #
# Description: Recognize and test digits on an image.           #
# Version: 0.0.1                                                #
# Author: Gökhan Sari                                           #
# E-mail: g-sari@g-sari.com                                     #
#################################################################

import cv2
import numpy as np
from Digit_recognize.picture import Pic
import pathlib
import math


class DigitRecognizerTesting:
    """Class used to test digits on an image"""

    def __init__(self):
        #test_img_path = str(pathlib.Path(__file__).parent.absolute()) + "\\training.png"
        test_img_path = "scr.png"
        self.image_to_test = Pic(pic_name=test_img_path, contour_dimension_from_h=21, contour_dimension_to_h=38)
        self.load_training_data()
        self.model = cv2.ml.KNearest_create()
        self.model.train(self.samples, cv2.ml.ROW_SAMPLE, self.responses)

    def contour_sorting_method(self, ctr1, ctr2):
        [x1, y1, w1, h1] = cv2.boundingRect(ctr1)
        [x2, y2, w2, h2] = cv2.boundingRect(ctr2)
        if y1 - y2 < 6:
            return x1 - y1
        return cv2.boundingRect(ctr)[0] + (cv2.boundingRect(ctr)[1]/9) * im.shape[1]

    def load_training_data(self):
        self.samples = np.loadtxt('ocr_training.data', np.float32)
        self.responses = np.loadtxt('ocr_responses.data', np.float32)
        self.responses = self.responses.reshape((self.responses.size, 1))

    def get_numbers(self):
        im = cv2.imread(self.image_to_test.pic_name)
        out = np.zeros(im.shape, np.uint8)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
        sudoku_numbers_output = ""
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        #TODO the culprit is possible difference in rows - contour that is 2 pixels below will have higher index - should normalize such changes
        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + (round(cv2.boundingRect(ctr)[1]/14)) * im.shape[1])
        #contours = sorted(contours, key=self.contour_sorting_method)

        last_row = 0
        last_col = 0
        container = [
            [0 for _ in range(9)] for _ in range(9)
        ]
        row = 0
        col = 0

        for cnt in contours:
            if cv2.contourArea(cnt) > self.image_to_test.contour_dimension_to_h:
                [x, y, w, h] = cv2.boundingRect(cnt)
                if h > self.image_to_test.contour_dimension_from_h and h < self.image_to_test.contour_dimension_to_h:
                    cv2.line(im, (x-1, y-1), (im.shape[0], y-1), (0, 255, 0), thickness=1)
                    cv2.rectangle(im, (x - 1, y - 1), (x + 1 + w, y + 1 + h), (0, 255, 0), 1)
                    roi = thresh[y:y + h, x:x + w]
                    roismall = cv2.resize(roi, (10, 10))
                    roismall = roismall.reshape((1, 100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = self.model.findNearest(roismall, k=1)
                    string = str(int((results[0][0])))
                    
                    decrement = 1 #when we step over empty cell we should not count the first filled one, except when going on new row where we start counting from 0
                    if y - last_row > 50:
                        sudoku_numbers_output += "0" * math.floor((im.shape[0] - last_col) / (im.shape[0]/9))
                        sudoku_numbers_output += "\n"
                        last_col = 0
                        row += 1
                        col = 0
                        #TODO add first n empty cells in new row
                    if last_col == 0: decrement = 0
                    if (x - last_col) > im.shape[0] / 9:
                        empty_spaces = round((x - last_col) / (im.shape[0] / 9) - decrement)
                        sudoku_numbers_output += "0" * empty_spaces
                        col += empty_spaces

                    last_row = y
                    last_col = x
                    sudoku_numbers_output += string
                    container[row][col] = int(string)
                    col += 1
                    cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))

        if (im.shape[0] - last_col) > im.shape[0]/9: sudoku_numbers_output += "0" * round((im.shape[0] - last_col) / (im.shape[0] / 9) - 1)
        print("Detected sudoku numbers:\n" + sudoku_numbers_output)
        #cv2.imshow('input', im)
        #cv2.imshow('output', out)
        #cv2.waitKey(0)
        empty_positions = []
        for i in range(9):
            for j in range(9):
                if container[i][j] == 0: empty_positions.append((i,j))
        return container, empty_positions


# Start the testing process
if __name__ == '__main__':
    DigitRecognizerTesting().get_numbers()
