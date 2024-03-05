from sympy.simplify import simplify
from sympy import Symbol, sympify, solve

from itertools import zip_longest
from typing import Iterable
import libs.tools as tools


@tools.alias(names=["Point", "point", "Pt", "pt"], globalsDict=globals())
class _Point:
    def __init__(self, *coordinates):
        self.coordinates = coordinates
        self.shape = len(coordinates)


    # * Attributes
    def __str__(self): return f"point{self.coordinates}"
    def __repr__(self): return f"point{self.shape}D{self.coordinates}"
    def __name__(self): return f"_Point"
    def __iter__(self): return iter(self.coordinates)
    def __len__(self) -> int: return self.shape
    def _sympy_(self): return self


    # * Comparison
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, _Point):
            return all(_1 == _2 for _1, _2 in zip_longest(self, __value, fillvalue=0))
        
        return False
    
    def __ne__(self, __value: object) -> bool: return not self == __value


    # * Arithmetic
    def __add__(self, __other):
        if isinstance(__other, _Point):
            return _Point(*tuple(simplify(f"({_1}) + ({_2})") for _1, _2 in zip_longest(self, __other, fillvalue=0)))
        elif isinstance(__other, _Vector):
            return _Vector(start=(self), end=(self + __other.end))
        elif isinstance(__other, (int, float)):
            return _Point(*tuple(simplify(f"({_1}) + ({__other})") for _1 in self))

        return sympify(f"({self}) + ({__other})")
    
    def __radd__(self, __other): return self + __other

    def __sub__(self, __other):
        if isinstance(__other, _Point):
            return _Point(*tuple(simplify(f"({_1}) - ({_2})") for _1, _2 in zip_longest(self, __other, fillvalue=0)))
        elif isinstance(__other, _Vector):
            return _Vector(end=(__other), start=(self))
        elif isinstance(__other, (int, float)):
            return _Point(*tuple(simplify(f"({_1}) - ({__other})") for _1 in self))
        
        return sympify(f"({self}) - ({__other})")
    
    def __rsub__(self, __other): return self - __other
    def __neg__(self): return _Point(*tuple(simplify(f"-({_1})") for _1 in self))

    def __mul__(self, __other):
        if isinstance(__other, _Point):
            return simplify(' + '.join(f"(({_1}) * ({_2}))" for _1, _2 in zip_longest(self, __other, fillvalue=0)))
        
        return _Point(*tuple(simplify(f"({_1}) * ({__other})") for _1 in self))

    def __rmul__(self, __other): return self * __other


class Origin(_Point):
    def __init__(self, shape: int):
        super().__init__(*tuple(0 for _ in range(shape)))


@tools.alias(names=["Vector", "vector", "Vec", "vec"], globalsDict=globals())
class _Vector:
    def __init__(self, *vec, start: Iterable = None, end: Iterable = None):
        self.shape = len(end if end else vec)
        
        """
        # print(_Point(*start))
        # print(*tuple(start))

        if str(type(start)) in ("point"):
            print("start is a point") 
            print(start + 2)
        """

        self.start = _Point(*start) if start else Origin(self.shape)
        self.end = _Point(*end) if end else (_Point(*vec) + self.start)
        self.vec = tuple(self.end - self.start)
    
        self.magnitude = abs(self)
    

    # * Attributes
    def __str__(self): return f"Vec{self.vec}"
    # def __str__(self): return f'Vec{str(self.vec)[:-1]}, start=({self.start}))'
    # def __str__(self): return f'Vec{str(self.vec)[:-1]}, **{{"start": {self.start}}})'
    def __repr__(self): return f"Vector{self.shape}D{self.vec}  (start: {self.start}, end: {self.end})"
    def __name__(self): return f"_Vector"
    def __iter__(self): return iter(self.vec)    
    def __len__(self) -> int: return self.shape
    def _sympy_(self): return self


    # * Comparison
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, _Vector):
            return all(_1 == _2 for _1, _2 in zip_longest(self, __value, fillvalue=0))
        
        return False
    
    def __ne__(self, __value: object) -> bool: return not self == __value

    def isinverse(self, __other: object) -> bool: 
        if isinstance(__other, _Vector):
            return abs(self + __other) == 0
        
        raise TypeError(f"Expected a Vector, got {type(__other)}")
        
    def isparallel(self, __other: object) -> bool:
        if isinstance(__other, _Vector):
            solutions = solve(eval(f"{self} - ({__other} *  Symbol('scalar'))"))
            return not (False == len(solutions))
        
        raise TypeError(f"Expected a Vector, got {type(__other)}")
    
    def isorthogonal(self, __other: object) -> bool:
        if isinstance(__other, _Vector):
            return self * __other == 0
        
        raise TypeError(f"Expected a Vector, got {type(__other)}")
    

    # * Arithmetic
    # Translation
    def __add__(self, __other):
        if isinstance(__other, (_Vector, _Point)):
            return _Vector(*tuple(simplify(f"({_1}) + ({_2})") for _1, _2 in zip_longest(self, __other, fillvalue=0)), start=self.start)
        elif isinstance(__other, (int, float)):
            # return _Vector(*tuple(simplify(f"({_1}) + ({__other})") for _1 in self))
            return _Vector(start=self.start, end=tuple(simplify(f"({_1}) + ({__other})") for _1 in self))
        
        return sympify(f"({self}) + ({__other})")

    def __radd__(self, __other): return self + __other
    

    # Displacement
    def __sub__(self, __other):
        if isinstance(__other, (_Vector, _Point)):
            return _Vector(*tuple(simplify(f"({_1}) - ({_2})") for _1, _2 in zip_longest(self, __other, fillvalue=0)), start=self.start)
        elif isinstance(__other, (int, float)):        
            # return _Vector(*tuple(simplify(f"({_1}) - ({__other})") for _1 in self))
            return _Vector(start=self.start, end=tuple(simplify(f"({_1}) - ({__other})") for _1 in self))

        return sympify(f"({self}) - ({__other})")
 
    def __rsub__(self, __other): return self - __other
    
    
    # Scaling & Projection
    def __mul__(self, __other):
        if isinstance(__other, _Vector):
            # return tuple(simplify(f"({_1}) * ({_2})") for _1, _2 in zip_longest(self, __other, fillvalue=0))
            return simplify(' + '.join(f"(({_1}) * ({_2}))" for _1, _2 in zip_longest(self, __other, fillvalue=0)))
        
        return _Vector(*tuple(simplify(f"({_1}) * ({__other})") for _1 in self))

    def __rmul__(self, __other): return self * __other


    # Magnitude
    def __abs__(self): return simplify(f"sqrt({'+'.join(f'({_})**2' for _ in self)})")
    
    # Inversion
    def __neg__(self): return _Vector(*tuple(simplify(f"-({_1})") for _1 in self))


class NullVector(_Vector):
    def __init__(self, shape: int):
        super().__init__(*(0 for _ in range(shape)))


# ! Deprecated
# * Dot product
@tools.alias(names=["Dot", "scalar", "Scalar"], globalsDict=globals())
def __dot(vectorV: _Vector, vectorU: _Vector, angle: float = None, radians: bool = False):
    """
    Deprecated
    """
    if angle:
        cosineValue = (f"cos({angle})" if radians else f"cos({angle} * pi / 180)")

        return simplify(f"({abs(vectorV)}) * ({abs(vectorU)}) * ({cosineValue})")
    
    return tuple(simplify(f"({_1}) * ({_2})") for _1, _2 in zip_longest(vectorV, vectorU, fillvalue=0))



if __name__ == "__main__":
    v = _Vector((1, 2, 3), (0, 0, 0))