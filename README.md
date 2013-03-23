mandelbrot
==========
This is a simple and naïve Mandelbrot generator that displays a section of the
Mandelbrot set and its surroundings.

The code is written in Python using tkinter for rendering the result.

The program was written together with my son after talking about what
the Mandelbrot set was as a way to play with programming and math.

No emphasis has been put on performance or a lot of nice features as that was
not the objective of this afternoon project. So be patient if you try it out.

A lot of other brilliant Mandelbrot renderers already exists and my son is
already off to play with one of them.

Usage
-----
To run the program, clone this project and issue this command:

    ./mandelbrot.py

This will render the Mandelbrot set using the default values of the program.
The defaults are listed as part of the help text which is written to stdout
when you run the program with the `--help` option:

    ./mandelbrot.py --help

Examples
--------
These are examples where we zoom in on some details:

    ./mandelbrot.py -x -1.0 -X -0.5 -y 0.0 -Y 0.3
    ./mandelbrot.py -x -0.752 -X -0.742 -y 0.075 -Y 0.100
