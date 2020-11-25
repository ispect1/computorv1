# ComputorV1

## Before start
`python3 -m venv venv && source venv/bin/activate`

## Description
A program for solving polynomial equations of degree no higher than two. Knows how to work with complex solutions

## Usage
`./computor.py` - run program

```
usage: computor.py [-h] [-c] [-d] [-i] [-s] [equation]

positional arguments:
  equation              The equation to be solved. If this argument is not present,
                        it will ask you to write via standard input

optional arguments:
  -h, --help            show this help message and exit
  -c, --common          display the result in ordinary fractions
  -d, --debug           debug mode
  -i, --interactive     interactive mode (only unix or Docker) - save history input (⇥ ↑ ↓)
  -s, --superscripts    display math symbols
```

## Examples
`./computor.py`

`./computor.py "X^2+X-2=0"`

`./computor.py "X^2+1/9-2/3*X=0" -c`

`./computor.py X^12+12=0 -d`

`./computor.py X^3=X^3-1 -s`

`./computor.py "X^12+X^10-X^5-X^(-19)=0" -s`

`./computor.py -i`


## If everything is bad, use magic (Docker required)
```shell script
docker build -t my_computor .
docker run -it --rm my_computor
./computor.py
```