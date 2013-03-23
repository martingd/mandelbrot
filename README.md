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

There are a lot of options to change both the section of the complex plane
inspected as well as the colors used for the points outside the Mandelbrot set.

Examples
--------
Mandelbrot as we know it with the program's default section of the complex
plane and default coloring: blue to cyan through the spectrum:

    ./mandelbrot.py

![Default Mandelbrot image](/images/1-default.png)

Same as above, but cycling backwards from blue towards cyan, so we get no red
or yellow:

    ./mandelbrot.py -C 0.5

![Default Mandelbrot image with blue to cyan colors](/images/2-default-C0.5.png)

Same as above, but cycling through the spectrum 5 times from blue to red and
then 5 more times to red all the way through:

    ./mandelbrot.py -C 5.0

![Default Mandelbrot image with blue to red to red 5 times](/images/3-default-C5.0.png)

A zoom into the top canyon:

    ./mandelbrot.py -x -1.0 -X -0.5 -y 0.0 -Y 0.3

![Mandelbrot top canyon](/images/4-top-canyon.png)

A deeper zoom into the Seahorse Spiral with default colors:

    ./mandelbrot.py -x -0.752 -X -0.742 -y 0.075 -Y 0.100

![Mandelbrot Seahorse Spiral](/images/5-seahorse.png)

Same with blue to cyan colors:

    ./mandelbrot.py -x -0.752 -X -0.742 -y 0.075 -Y 0.100 -C 0.5

![Mandelbrot Seahorse Spiral with blue to cyan colors](/images/6-seahorse-C0.5.png "Mandelbrot Seahorse Spiral with blue to cyan colors")

And once more cycling through the spectrum 5 times from blue to red and
then 5 more times to red all the way through:

    ./mandelbrot.py -x -0.752 -X -0.742 -y 0.075 -Y 0.100 -C 5.0

![Mandelbrot Seahorse Spiral with blue to red to red 5 times](/images/7-seahorse-C5.0.png)
