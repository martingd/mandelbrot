#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import argparse
from tkinter import Tk, Canvas, PhotoImage, mainloop

class ScreenCoords:
    def __init__(self, args):
        self.reRange = args.reMaxFloat - args.reMinFloat
        self.imRange = args.imMaxFloat - args.imMinFloat
        aspectRatio = self.imRange / self.reRange
        self.rePixels = args.rePixels
        self.imPixels = int(self.rePixels * aspectRatio)
        
        self.reMinFloat = args.reMinFloat
        self.imMinFloat = args.imMinFloat

    '''
    Pixel coordinates counting from (0,0) upper left are transformed into
    the corresponding complex number.
    '''
    def complexFromIndex(self, reIndex, imIndex):
        reFloat = ((float(reIndex) / self.rePixels) * self.reRange) + self.reMinFloat
        imFloat = ((float(imIndex) / self.imPixels) * self.imRange) + self.imMinFloat
        return reFloat + imFloat*1j
        

def isMandel(c, maxIterations):
    z = 0
    for i in range(1,maxIterations):
        z = z**2 + c
        if abs(z) > 2:
            return i
    # Exceeded max iterations
    return -1

def makeColors(args, gammaFunction = None):
    maxIterations = args.maxIterations
    minBlue = args.colorMin
    maxBlue = args.colorMax
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
    rePixels = screenCoords.rePixels
    imPixels = screenCoords.imPixels

    mandelbrotResult = []
    for imIndex in range(imPixels):
        reList = []
        mandelbrotResult.append(reList)
        for reIndex in range(rePixels):
            c = screenCoords.complexFromIndex(reIndex, imIndex)
            i = isMandel(c, args.maxIterations)
            reList.append(i)
            sign = '*' if i == -1 else ' '
    
    return mandelbrotResult

def drawResult(args, screenCoords, mandelbrotResult):
    width  = screenCoords.rePixels
    height = screenCoords.imPixels

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
    parser.add_argument('-p', '--pixels-real',
                        dest = 'rePixels',
                        help = 'The number of pixels in the real axis. (default is 500)',
                        type = int,
                        default = 500)
    parser.add_argument('-i', '--max-iterations',
                        dest = 'maxIterations',
                        help = 'The maximum number of iterations of the Mandelbrot formula to try before ' +
                               'accepting a point in the complex plane to be within the set.',
                        type = int,
                        default = 200)
    parser.add_argument('-c', '--color-min',
                        dest = 'colorMin',
                        help = 'The lowest blue color value used for points outside ' +
                               'the Mandelbrot set. (default is 40)',
                        type = float,
                        default = 40)
    parser.add_argument('-C', '--color-max',
                        dest = 'colorMax',
                        help = 'The highest blue color value used for points outside ' +
                               'the Mandelbrot set. (default is 40)',
                        type = int,
                        default = 255)
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
