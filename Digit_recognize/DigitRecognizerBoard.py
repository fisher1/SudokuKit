import cv2
import numpy as np
import pathlib
import math


class DigitRecognizerBoard:
    """Class used to recognize digits on a cropped image of a Sudoku board"""

    def __init__(self):
        self.load_training_data()
        self.model = cv2.ml.KNearest_create()
        self.model.train(self.samples, cv2.ml.ROW_SAMPLE, self.responses)

    def load_training_data(self):
        self.samples = np.loadtxt('ocr_training.data', np.float32)
        self.responses = np.loadtxt('ocr_responses.data', np.float32)
        self.responses = self.responses.reshape((self.responses.size, 1))

    def get_numbers(self, pic_name):
        im = cv2.imread(pic_name)
        out = np.zeros(im.shape, np.uint8)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
        sudoku_numbers_output = ""

        container = [
            [0 for _ in range(9)] for _ in range(9)
        ]
        empty_positions = []

        square_size = math.floor(im.shape[0] / 9)
        for row in range(0, 9):
            for col in range(0, 9):
                crop_inward_thickness = 3 #shows how much should be cropped from each side to avoid the borders of each square
                y = row * square_size + crop_inward_thickness
                x = col * square_size + crop_inward_thickness
                square = thresh[y:y + square_size - crop_inward_thickness, x:x + square_size - crop_inward_thickness]
                #kNN is trained on close cropped digits, so we have to find contours and cannot just pass the whole square
                contours, _ = cv2.findContours(square, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                added_value = False
                for cnt in contours:
                    [x, y, w, h] = cv2.boundingRect(cnt)
                    #a whole digit should take more than 1/3 of the height of a square - this could be modified for different cases
                    min_digit_height = square_size/3
                    if h > min_digit_height:
                        cv2.rectangle(square, (x - 1, y - 1), (x + 1 + w, y + 1 + h), (0, 255, 0), 3)
                        roi = square[y:y + h, x:x + w]
                        roismall = cv2.resize(roi, (10, 10))
                        roismall = roismall.reshape((1, 100))
                        roismall = np.float32(roismall)
                        retval, results, neigh_resp, dists = self.model.findNearest(roismall, k=1)
                        digit = int((results[0][0]))
                        container[row][col] = digit
                        added_value = True
                if added_value == False:
                    container[row][col] = 0
                empty_positions.append((row,col))
        return container, empty_positions
