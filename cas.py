from sympy.solvers import solve
from itertools import chain
from sympy import *


characters = [chr(i) for i in chain(range(65, 90+1), range(97, 122+1))]

characters.remove("E")  # Remove the letter "E" so that Euler's number doesn't get overwritten
characters.remove("I")  # Remove the letter "I" so that the imaginary number doesn't get overwritten

syntaxDictionary = {
    ">=": ">%",
    "<=": "<$",
    "eval=": "evaluate&&",
    "evaluate=": "evaluate&&"
}

placeholderDictionary = {
    ">%": ">=",
    "<$": "<=",
    "&&": "="
}

for character in characters:
    # // characterDictionary[character.upper()] = character
    exec(f"{character} = Symbol(\"{character}\")")

# Variable to solve for, set "" for any
solveFor = ""

def calculate():
    inputEquation = input("Equation: ").replace("^", "**")  # Replace the exponent character, with the python syntax exponent

    if inputEquation == "":
        return 0

    # for i in characterDictionary.keys():
    #    inputEquation = inputEquation.replace(i, characterDictionary[i])

    # Parse syntax
    for key, value in syntaxDictionary.items():
        inputEquation = inputEquation.replace(key, value)


    # Solve for
    solveFor = ""
    solveForGenerator = iter(list(inputEquation))

    index = 0
    variables = [""]

    while True:
        character = next(solveForGenerator, None)

        if character == None:
            break

        if character.isalpha() or character == "_":
            variables[index] += character
        else:
            index += 1
            variables.append("")

    upperCaseVariables = [cache for cache in variables if cache not in ["E", "I", ""] and cache.replace("_", "").isupper()]

    if not upperCaseVariables == []:
        solveFor = upperCaseVariables[0]

    # Split and sort the equation, if it contains an "equal" sign
    try:
        # Attempt to split the equation on the "equal" sign
        splitInputEquation = inputEquation.split("=")

        # Sort the equation to one side of the "equal" sign
        equation = f"{splitInputEquation[0]} -({splitInputEquation[1]})"
    except IndexError:
        equation = inputEquation

    # Replace syntax placeholders
    for key, value in placeholderDictionary.items():
        equation = equation.replace(key, value)
    
    try:
        print(f"{solveFor}: {solve(eval(equation), solveFor)}\n" if not solveFor == "" else f"Solution: {solve(eval(equation), dict=True)}\n")
        return 1
    except Exception as exc:
        print(f"[{str(exc.__class__)[8:-2]}] {str(exc).capitalize()}\n")
        return 1

