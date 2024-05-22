from itertools import chain
from sympy import *
import builtins

# from libs.imports import *
import libs.tools as tools
from libs.types import *



def calculate():
    __displayVariableTable()

    inputEquation = input("Equation: ")

    if inputEquation == "":
        print()
        return (0 if __DEBUG else 1)
    

    # * Parse syntax
    for key, value in syntaxDictionary.items():
        inputEquation = inputEquation.replace(key, value)


    # * Solve for, Multicharacter variables, & Variable assignment
    solveFor = ""
    solveForGenerator = iter(list(inputEquation))

    bucketIndex = 0
    iteration = 0
    
    variables = [""]

    assignmentOperatorIndex = inputEquation.find(":=")
    assignNewVariable = False
    

    # Sort the equation into variables
    while True:
        character = next(solveForGenerator, None)

        if character == None:
            break
        
        
        # This if statement is a bit of a mess, so here: 
        # - The first two checks are to see if the character is an assignment operator
        # - The third check removes all empty strings and duplicate variables temporarily from the list, 
        #   so that it can check to see if there is only one variable before the assignment operator 
        # - The fourth check makes sure we don't overwrite any keywords, variables, or functions 
        #   that aren't previously assigned variables or the characters list
        if character == ":" and iteration == assignmentOperatorIndex and len(set(variables) - {""}) == 1 and not __nameExists(variables[0]):
            assignNewVariable = True

            solveFor = variables[0]
            inputEquation = inputEquation.replace(":=", "=")
            
        if character.isalpha() or character == "_" or (character.isdigit() and variables[bucketIndex] != ""):
            variables[bucketIndex] += character
        else:
            bucketIndex += 1
            variables.append("")
        
        iteration += 1

    upperCaseVariables = [cache for cache in variables if cache not in ["E", "I", ""] and cache.replace("_", "").isupper() and not cache in assignedVariables.keys() ]
    # // multiCharacterVariables = [cache for cache in variables if not __nameExists(cache) and not cache == ""]

    if not upperCaseVariables == [] and not assignNewVariable:
        solveFor = list(set(upperCaseVariables))


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
        if assignNewVariable:
            # Make all assigned variables into sympy symbols so that they can be used in the equation without representing soulutions when a new variable is assigned
            for variable in assignedVariables.keys():
                # // exec(f"{variable} = Symbol(\"{variable}\")", globals())
                # print(f'"{type(assignedVariables[variable])}"')
                if str(type(assignedVariables[variable])) in ("point", "Vec"):
                    # print(type(assignedVariables[variable]))
                    continue

                __initializeVariable(variable)

            # // exec(f"{solveFor} = Symbol(\"{solveFor}\")", globals())
            __initializeVariable(solveFor)

        # print(equation)

        """
        try:
            print(a)
        except:
            pass
        """
        # print(f"Equation: {equation}")
        parsedEquation = eval(equation)

        # print(parsedEquation)
        # print(type(parsedEquation))
        

        # Check if the equation is a function call, and handle it accordingly
        if type(parsedEquation) == dict and "func" in parsedEquation.keys():
            if parsedEquation["func"] == "remvar":
                print(parsedEquation["message"])
                return 1



        if not solveFor == "":
            # print(parsedEquation)
            solutions = solve(parsedEquation, solveFor)

            if assignNewVariable:
                print(f"Solution: {solutions}\n")
                if len(solutions) > 1:
                    __index = 0
                    __solutionIterator = iter(solutions)
                    __solution = next(__solutionIterator, None)
                    while True:
                        if __solution == None:
                            break

                        variableName = f"{solveFor}_{__index}"
                        __index += 1

                        # TODO: Fix so that previously assigned variables are not overwritten
                        if __nameExists(variableName) or variableName in assignedVariables.keys() :
                            continue


                        assignedVariables[variableName] = __solution

                        __solution = next(__solutionIterator, None)

                elif len(solutions) == 1:
                    assignedVariables[solveFor] = solutions[0]
                    # print(repr(solutions[0]), type(solutions[0]))
                else:
                    # print(f"No solutions found for {solveFor}\n")
                    raise ValueError(f"No solutions found for: \"{solveFor}\" ({solutions})")
                    

                # Reassign all assigned variables to their solutions
                __reassignVariables()

                return 1
            
            # Print the solution
            match type(solutions):
                case tools.LIST_TYPE:
                    if len(solveFor) == 1: print(f"{solveFor[0]} = {solutions}\n")
                    else: print(f"{solveFor} = {solutions}\n")
                case tools.DICT_TYPE:
                    # print(F"Solution: {solutions}\n")
                    print(f"{solutions}\n")
                case _:
                    print(f"{solveFor} = {solutions}\n")
            
            return 1
        
        print(f"Solution: {solve(parsedEquation, dict=True)}\n")
        return 1
    except Exception as exc:
        if __DEBUG:
            raise exc
        
        print(f"[{str(exc.__class__)[8:-2]}] {str(exc).capitalize()}\n")
        return 1


def __nameExists(name):
    # Exclude previously assigned variables and the characters list as these can be overwritten
    if name in assignedVariables or name in characters:
        return False 
    
    return name in globals() or hasattr(builtins, name)


def __displayVariableTable():
    if not assignedVariables:
        return

    print("\n[Variables]")
    longestVariableName = max(map(len, assignedVariables.keys()))

    for key, value in assignedVariables.items():
        print(f"{key:<{longestVariableName + 1}}: {value}")
    
    print()


def __initializeVariable(variable: str):
    exec(f'{variable} = Symbol("{variable}")', globals())


def __reassignVariables():
    for variable in assignedVariables.keys():
        # print(f"Re-assigning {variable} to {assignedVariables[variable]}")
        # exec(f"{variable} = {assignedVariables[variable]}", globals())
        # globals()[variable] = assignedVariables[variable]
        # globals()[variable] = exec(f"{assignedVariables[variable]}", globals())
        globals()[variable] = eval(f"{assignedVariables[variable]}")


def __setup():
    global characters, syntaxDictionary, placeholderDictionary, N, solveFor, assignedVariables

    characters = [chr(i) for i in chain(range(65, 90+1), range(97, 122+1))]

    characters.remove("E")  # Remove the letter "E" so that Euler's number doesn't get overwritten
    characters.remove("I")  # Remove the letter "I" so that the imaginary number doesn't get overwritten
    characters.remove("N")  # Remove the letter "N" so that the coordinate system doesn't get overwritten
    
    syntaxDictionary = {
        "^": "**",                      # Replace the exponent character, with the python syntax exponent character
        ">=": ">%",
        "<=": "<$",
        "eval=": "evaluate&&",
        "evaluate=": "evaluate&&",
        "start=": "start&&",
        "end=": "end&&"
    }

    placeholderDictionary = {
        ">%": ">=",
        "<$": "<=",
        "&&": "="
    }


    for character in characters:
        # // exec(f"{character} = Symbol(\"{character}\")", globals())
        __initializeVariable(character)

    # Variable to solve for, set "" for any
    solveFor = ""

    assignedVariables = {}


@tools.alias(names=["RemVar", "Remvar", "remVar", "remvar"], globalsDict=globals())
def removeVariable(variable: str):
    if variable == "*":
        for variable in tuple(assignedVariables.keys()):
            removeVariable(f"{variable}")

        return {"func": "remvar", "status": True, "message": "All variables removed\n"}

    if variable in assignedVariables:
        del assignedVariables[variable]
        del globals()[variable]

        # Incase the variable is single character, re-initialize it
        if len(variable) == 1:
            __initializeVariable(variable)

        # TODO: Re-assign all assigned variables to update their solutions
        __reassignVariables()

        return {"func": "remvar", "status": True, "message": f'Variable "{variable}" removed\n'}
    
    return {"func": "remvar", "status": False, "message": f'Variable "{variable}" does not exist\n'}


if __name__ == "__main__":
    __DEBUG = True
    __setup()

    while True:
        exitCode = calculate()

        if not exitCode:
            break
    
else:
    __DEBUG = False
    __setup()
