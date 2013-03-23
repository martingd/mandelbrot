#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import argparse
from tkinter import Tk, Canvas, PhotoImage, mainloop

'''Move these constants to command-line parameters.'''

#reMinFloat = -2.0
#reMaxFloat =  0.5
#imMinFloat = -1.0
#imMaxFloat =  1.0

# Pixels per [0;1[ intervals in any direction
#resolution = 200

#reMinFloat = -1.0
#reMaxFloat = -0.5
#imMinFloat =  0.0
#imMaxFloat =  0.3

# Pixels per [0;1[ intervals in any direction
#resolution = 2000

reMinFloat = -0.752
reMaxFloat = -0.742
imMinFloat =  0.075
imMaxFloat =  0.100

# Pixels per [0;1[ intervals in any direction
resolution = 3200

reMin = int(reMinFloat*resolution)
reMax = int(reMaxFloat*resolution)

imMin = int(imMinFloat*resolution)
imMax = int(imMaxFloat*resolution)

maxIterations = 255


def isMandel(c, maxIterations):
    z = 0
    for i in range(1,maxIterations):
        z = z**2 + c
        if abs(z) > 2:
            return i
    # Exceeded max iterations
    return -1

def complexFromIndex(reIndex, imIndex):
    re = float(reIndex)/resolution
    im = float(imIndex)/resolution
    return re + im*1j

def makeColors(number, gammaFunction = None):
    minBlue = 50
    maxBlue = 255
    rangeBlue = maxBlue - minBlue
    colors = []
    for i in range(0,number):
        blue = (i * rangeBlue / number-1) + minBlue
        if gammaFunction:
            blueNormalized = float(blue)/maxBlue
            blueNormalizedCorrected = gammaFunction(blueNormalized)
            blueCorrected = int(blueNormalizedCorrected*maxBlue)
        else:
            blueCorrected = blue
        colors.append("#0000%02X" % blueCorrected)
    return colors

#colors = makeColors(maxIterations)

# Playing with the color gammacorrection.
#colors = makeColors(maxIterations, lambda normColor: normColor**2)

def calculateMandelbrot():
    mandelbrotResult = []
    for imIndex in range(imMax, imMin-1, -1):
        reList = []
        mandelbrotResult.append(reList)
        for reIndex in range(reMin, reMax+1):
            c = complexFromIndex(reIndex, imIndex)
            i = isMandel(c, maxIterations)
            reList.append(i)
            sign = '*' if i == -1 else ' '
    
    print("Done!")
    print("  height = %d" % len(mandelbrotResult))
    print("  length = %d" % len(mandelbrotResult[0]))
    return mandelbrotResult

WIDTH, HEIGHT = reMax-reMin+1, imMax-imMin+1

def drawResult(mandelbrotResult):
    window = Tk()
    canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
    canvas.pack()
    img = PhotoImage(width=WIDTH, height=HEIGHT)
    canvas.configure(background='white')
    canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")
    
    colors = makeColors(maxIterations)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = mandelbrotResult[y][x]
            color = "#000000" if pixel == -1 else colors[pixel]
            img.put(color, (x,y))
    
    mainloop()

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    try:
        try:
            argparser = argparse.ArgumentParser()
            parsedArgs = argparser.parse_args(argv)
        except argparse.ArgumentError as msg:
             raise Usage(msg)

        mandelbrotResult = calculateMandelbrot()
        drawResult(mandelbrotResult)

    except Usage as err:
        print(err.msg, file=sys.stderr)
        print("for help use --help", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
