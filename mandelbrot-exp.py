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

#reMinFloat = -0.752
#reMaxFloat = -0.742
#imMinFloat =  0.075
#imMaxFloat =  0.100

# Pixels per [0;1[ intervals in any direction
#maxIterations = 255

class ScreenCoords:
    def __init__(self, args):
        resolution = args.resolution
        self.reMin = int(args.reMinFloat*resolution)
        self.reMax = int(args.reMaxFloat*resolution)
        self.imMin = int(args.imMinFloat*resolution)
        self.imMax = int(args.imMaxFloat*resolution)

def isMandel(c, maxIterations):
    z = 0
    for i in range(1,maxIterations):
        z = z**2 + c
        if abs(z) > 2:
            return i
    # Exceeded max iterations
    return -1

def complexFromIndex(reIndex, imIndex, resolution):
    re = float(reIndex)/resolution
    im = float(imIndex)/resolution
    return re + im*1j

def makeColors(args, gammaFunction = None):
    maxIterations = args.maxIterations
    minBlue = 50
    maxBlue = 255
    rangeBlue = maxBlue - minBlue
    colors = []
    for i in range(0, maxIterations):
        blue = (i * rangeBlue / maxIterations - 1) + minBlue
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

def calculateMandelbrot(args, screenCoords):
    resolution = args.resolution

    reMin = screenCoords.reMin
    reMax = screenCoords.reMax
    
    imMin = screenCoords.imMin
    imMax = screenCoords.imMax

    mandelbrotResult = []
    for imIndex in range(imMax, imMin-1, -1):
        reList = []
        mandelbrotResult.append(reList)
        for reIndex in range(reMin, reMax+1):
            c = complexFromIndex(reIndex, imIndex, resolution)
            i = isMandel(c, args.maxIterations)
            reList.append(i)
            sign = '*' if i == -1 else ' '
    
    return mandelbrotResult

def drawResult(args, screenCoords, mandelbrotResult):
    width  = screenCoords.reMax - screenCoords.reMin + 1
    height = screenCoords.imMax - screenCoords.imMin + 1

    window = Tk()
    canvas = Canvas(window, width=width, height=height, bg="#000000")
    canvas.pack()
    img = PhotoImage(width=width, height=height)
    canvas.configure(background='white')
    canvas.create_image((width/2, height/2), image=img, state="normal")
    
    colors = makeColors(args)

    for y in range(height):
        for x in range(width):
            pixel = mandelbrotResult[y][x]
            color = "#000000" if pixel == -1 else colors[pixel]
            img.put(color, (x,y))
    
    mainloop()

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def getArgparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--real-min',
                        dest = 'reMinFloat',
                        help = 'The lowest value on the real axis. (default is -2.0)',
                        type = float,
                        default = -2.0)
    parser.add_argument('-X', '--real-max',
                        dest = 'reMaxFloat',
                        help = 'The highest value on the real axis. (default is +0.5)',
                        type = float,
                        default = +0.5)
    parser.add_argument('-y', '--imaginary-min',
                        dest = 'imMinFloat',
                        help = 'The lowest value on the imaginary axis. (default is -1.0)',
                        type = float,
                        default = -1.0)
    parser.add_argument('-Y', '--imaginary-max',
                        dest = 'imMaxFloat',
                        help = 'The highest value on the imaginary axis. (default is +1.0)',
                        type = float,
                        default = +1.0)
    parser.add_argument('-r', '--resolution',
                        dest = 'resolution',
                        help = 'The number of pixels corresponding to an interval of [0;1). (default is 200)',
                        type = int,
                        default = 200)
    parser.add_argument('-i', '--max-iterations',
                        dest = 'maxIterations',
                        help = 'The maximum number of iterations of the Mandelbrot formula to try before ' +
                               'accepting a point in the complex plane to be within the set.',
                        type = int,
                        default = 200)
    return parser

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    try:
        try:
            argParser = getArgparser()
            parsedArgs = argParser.parse_args(argv)
        except argparse.ArgumentError as msg:
             raise Usage(msg)

        screenCoords = ScreenCoords(parsedArgs)
        mandelbrotResult = calculateMandelbrot(parsedArgs, screenCoords)
        drawResult(parsedArgs, screenCoords, mandelbrotResult)

    except Usage as err:
        print(err.msg, file=sys.stderr)
        print("for help use --help", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
