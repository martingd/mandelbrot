#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import argparse
import colorsys
import math
from Tkinter import Tk, Canvas, PhotoImage, mainloop

class ScreenCoords:
    def __init__(self, args):
        self.reRange = args.reMaxFloat - args.reMinFloat
        self.imRange = args.imMaxFloat - args.imMinFloat
        aspectRatio = self.imRange / self.reRange
        self.rePixels = args.rePixels
        self.imPixels = int(self.rePixels * aspectRatio)
        
        self.reMinFloat = args.reMinFloat
        self.imMaxFloat = args.imMaxFloat

    '''
    Pixel coordinates counting from (0,0) upper left are transformed into
    the corresponding complex number.
    '''
    def complexFromIndex(self, reIndex, imIndex):
        reFloat = ((float(reIndex) / self.rePixels) * self.reRange) + self.reMinFloat
        imFloat = ((float(imIndex) / self.imPixels) * -self.imRange) + self.imMaxFloat
        return reFloat + imFloat*1j
        

def isMandel(c, maxIterations):
    z = 0
    for i in range(1,maxIterations):
        z = z**2 + c
        if abs(z) > 2:
            return i
    # Exceeded max iterations
    return -1

def makeColorTable(args, gammaFunction = None):
    maxIterations = args.maxIterations

    valueMin = args.colorValueMin
    valueMax = args.colorValueMax
    valueRange = valueMax - valueMin

    hueMin = args.colorHueMin
    hueMax = args.colorHueMax
    hueRange = hueMax - hueMin

    colors = []
    for i in range(0, maxIterations):
        value = (i * valueRange / (maxIterations - 1)) + valueMin
        if gammaFunction:
            valueNormalized = float(value)/valueMax
            valueNormalizedCorrected = gammaFunction(valueNormalized)
            valueCorrected = int(valueNormalizedCorrected*valueMax)
        else:
            valueCorrected = value

        hue = (hueRange * i / (maxIterations - 1)) + hueMin
        if hue > 1.0:
            # Fold hue into the interval [0;1]
            hue = math.fmod(hue, 1.0)

        (r,g,b) = colorsys.hsv_to_rgb(hue, 1, valueCorrected)
        colors.append("#%02X%02X%02X" % (int(r*255), int(g*255), int(b*255)))
    return colors

# Playing with the color gammacorrection.
#colors = makeColorTable(maxIterations, lambda normColor: normColor**2)

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
    
    return mandelbrotResult

def drawResult(args, screenCoords, mandelbrotResult):
    width  = screenCoords.rePixels
    height = screenCoords.imPixels
    black = "#000000"

    window = Tk()
    window.wm_title("Mandelbrot")
    canvas = Canvas(window, width=width, height=height, bg=black)
    canvas.pack()
    img = PhotoImage(width=width, height=height)
    canvas.configure(background='white')
    canvas.create_image((width/2, height/2), image=img, state="normal")
    
    colors = makeColorTable(args)

    for y in range(height):
        for x in range(width):
            pixel = mandelbrotResult[y][x]
            color = black if pixel == -1 else colors[pixel]
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
    parser.add_argument('-v', '--color-value-min',
                        dest = 'colorValueMin',
                        help = 'The HSV value used for points found farthest outside ' +
                               'the Mandelbrot set. (default is 0.15)',
                        type = float,
                        default = 0.15)
    parser.add_argument('-V', '--color-value-max',
                        dest = 'colorValueMax',
                        help = 'The HSV value used for points found outside but closest to' +
                               'the Mandelbrot set. (default is 1.0)',
                        type = float,
                        default = 1.0)
    parser.add_argument('-c', '--color-hue-min',
                        dest = 'colorHueMin',
                        help = 'The HSV hue used for points found farthest outside ' +
                               'the Mandelbrot set. All hue values are folded to ' +
                               'the interval [0;1]. (default is 0.666... for blue)',
                        type = float,
                        default = 2.0/3)
    parser.add_argument('-C', '--color-hue-max',
                        dest = 'colorHueMax',
                        help = 'The HSV hue used for points found outside but closest to' +
                               'the Mandelbrot set. All hue values are folded to ' +
                               'the interval [0;1]. (default is 1.5 for cyan)',
                        type = float,
                        default = 1.5)
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
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
