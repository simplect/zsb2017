# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
from sudoku.image_parser import SudokuImageParser, ImageError
from sudoku.solver import SudokuSolver, ContradictionError

from skimage import exposure
import numpy as np
import argparse

def crop(image):
    # http://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
    # https://www.quora.com/How-can-I-detect-an-object-from-static-image-and-crop-it-from-the-image-using-openCV
    # load the query image, compute the ratio of the old height
    # to the new height, clone it, and resize it
    ratio = image.shape[0] / 300.0
    orig = image.copy()

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                x,y,w,h = cv2.boundingRect(screenCnt)
                if w>50 and h>50:
                    return image[y-10:y+h+10,x-10:x+w+10]

def solve(image_name):
    parser = SudokuImageParser()
    solver = SudokuSolver()
    stringified_puzzle = ''

    try:
        image_data = cv2.imread(image_name, cv2.IMREAD_COLOR)
        img = crop(image_data.copy())

        stringified_puzzle = parser.parse(img)
    except (IndexError, ImageError) as e:
        solution = False

    try:
        solution = solver.solve(stringified_puzzle)
    except (ContradictionError, ValueError) as e:
        solution = False

    return (stringified_puzzle, solution)
