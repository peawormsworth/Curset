from fractions import Fraction

# precision limits the accuracy (size) of numbers generated 
precision     = 1/2**16
#precision     = 1/2**20

# limit the recursion depth 
max_recursion = 30

# useful surreal representations used throughout
nan    = []
nil    = [[],[]]
one    = [[],[]]
neg    = [[],[]]
nan[:] = nan,nan
nil[:] = nan,nan
one[:] = nil,nan
neg[:] = nan,nil


# note that as variation of the Van Der Corpus sequence, there may be a more
# efficient or consice routine for this.
def canal (r=[Fraction(0,1)]):
    """yeilds fractions according to their birthday ordering.

    0,-1,1,-2,-1/2,1/2,2,-3... 
    """

    yield r[0]
    while 1:
        yield r[0] - 1
        rn = [r[0]]
        for n in r[1:]:
            m = (rn[-1]+n)/2
            yield m
            rn.extend((m,n))
        yield rn[-1]+1
        r = [rn[0]-1] + rn + [rn[-1]+1]


def cleave (nucleus=[nil]):
    "yeilds linked lists according to their birthday ordering"

    l = nucleus
    yield l[-1]
    while 1:
        cnt = 0
        nl  = []
        for s in l:
            for n in [(s[0],s),(s,s[1])]:
                yield n
                nl = nl + [n]
        l = nl


def creation (days=7):
    """
    returns a dictionary of surreal labels and linked tuple representations.

    Parameters
    ----------
    days : limits the list to numbers born with this range
    """

    birth    = canal()
    sprout   = cleave()
    universe = {}
    for i in range(2**days-1):
        universe[next(birth)] = Curset(next(sprout))
    return universe


def construct (num,precision=precision):
    """
    given a number, generate the surreal number up to a precision 

    Parameters
    ----------
    precision : a number less than 1. ie: 1% precision would be 0.01
    """

    form  = nil
    scale = 1
    lone  = None
    while precision <= abs(num):
        if abs(num) <= 1: 
            lone = True
        if num <= 0:
            form = (form[0],form)
            num += scale
            lone = 0 <= num or lone
        else:
            form = (form,form[1])
            num -= scale
            lone = num <= 0 or lone
        if lone:
            scale /= 2 
    return form


def distill (s):
    "return the numeric value of this surreal representation as a float"

    form  = nil
    scale = 1
    lone  = False
    num   = Fraction(0/1)
    while not eq(s,form):
        if not lone and within(s,form,one):
            lone = True
        if le(form,s):
            form = (form,form[1])
            num += scale
            lone = lone or le(s,form)
        else:
            form = (form[0],form)
            num -= scale
            lone = lone or le(form,s)
        if lone:
            scale /= 2 
    return num


def least (s):
    "returns the surreal number with lowest numeric value from a list"

    if s is nan:
        return nan
    l = s[0]
    for n in s[1:]: 
        if le(n,l): l = n
    return l


def greatest (s):
    "returns the surreal number with greatest numeric value from a list"

    if s is nan:
        return nan
    g = s[0]
    for n in s[1:]: 
        if le(g,n): g = n
    return g


def reduce (x):
    "returns the reduced equilent form of any valid surreal representation"

    y = nil
    while not eq(y,x): 
        y = (y[0],y) if le(x,y) else (y,y[1])
    return y


def consolidate (x):
    "reduce a surreal with multiply left and or right surreals to the ideal form with only one value linked to each side"

    return (greatest(x[0]), least(x[1]))


def negate(x): 
    "return the negation of the given sureal representation"

    return (negate(x[1]), negate(x[0])) if x is not nan else x


def absolute (x): 
    "return the absolute value of a surreal as a surreal"

    return negate(x) if le(x,nil) else x


def sub (x,y):
    "subtract two surreals in the order given"

    return add(x,negate(y))


def eq (x,y):
    "compare two surreal numbers and return True if they are equivelent forms"

    return le(x,y) and le(y,x)


def ne (x,y):
    "not equal comparison of two surreals"

    return not le(x,y) and not le(y,x)


def gt (x,y):
    "greater than comparison of two surreals"

    return not le(x,y)


def lt (x,y):
    "less than comparison of two surreals"

    return not le(y,x)


def ge (x,y):
    "greater or equal comparison of two surreals"

    return le(y,x)


def within (a,b,c):
    "return True if a and b are less than c apart"

    return lt(absolute(sub(a,b)),c)


def le (x,y,n=0): 
    "less or equal comparison of two surreals"

    return x is y or not (x[0] is not nan and le(y,x[0]) or y[1] is not nan and le(y[1],x))


def limit_le (x,y,n=0): 
    """"a limited recurssion version for testing

    use parameter 'n' to set a limit otherwise it is unlimited.
    note that: import sys; sys.setrecursionlimit(n) is also useful in debugging recursion problems.
    """

    return n < max_recursion and x is y or not (x[0] is not nan and le(y,x[0],n+1) or y[1] is not nan and le(y[1],x,n+1))


def add (x,y):
    """add two surreal numbers"""

    if x == nil : return y
    if y == nil : return x
    if x == nil : return y
    if y == nil : return x
    left, right = nan, nan
    if len(x) > 0 and x[0] is not nan :  left = add(x[0],y)
    if len(x) > 1 and x[1] is not nan : right = add(x[1],y)
    if len(y) > 0 and y[0] is not nan : 
        under = add(x,y[0]) 
        if left is nan or  le(left, under): left = under
    if len(y) > 1 and y[1] is not nan:
        over  = add(x,y[1])
        if right is nan or le(over, right): right = over
    return (left, right)


def mult (x,y):
    """multiply two surreal numbers"""

    if x  == nil : return nil
    if y  == nil : return nil
    if x  == one : return y
    if y  == one : return x
    if x  == neg : return negate(y)
    if y  == neg : return negate(x)
    xl,xr,yl,yr = nan,nan,nan,nan
    if x  is not nan and x[0] : xl = x[0]
    if x  is not nan and x[1] : xr = x[1]
    if y  is not nan and y[0] : yl = y[0]
    if y  is not nan and y[1] : yr = y[1]
    if xl is not nan : xly = mult(xl,y)
    if yl is not nan : xyl = mult(x,yl)
    if xr is not nan : xry = mult(xr,y)
    if yr is not nan : xyr = mult(x,yr)
    l,r = nan,nan
    if xl is not nan and yl is not nan: 
        l = sub(add(xly,xyl),mult(xl,yl))
    if xr is not nan and yr is not nan: 
        o = sub(add(xry,xyr),mult(xr,yr))
        if l  is nan or le(l,o): l = o
    if xl is not nan and yr is not nan:
        r = sub(add(xly,xyr),mult(xl,yr))
    if xr is not nan and yl is not nan:
        o = sub(add(xyl,xry),mult(xr,yl))
        if r  is nan or le(o,r): r = o
    return reduce((l,r))


class Curset ():
    """
    Represent numbers as linked tuples.

    Each tuple contains two objects. Representing the left and right side of 
    the linked number. The number zero is identified as the list containing 
    the empty set on both the right and left side. From here the numbers are 
    built up from zero according to the right left pattern associated with 
    linked number location identification.

    This module provides procedural and object oriented interfaces.

    from surreal import construct, Curset
    procedure_surreal = construct(5/2)
    object_surreal = Curset(5/2)

    # then this is true:
    procedure_surreal = object_surreal.form()

    Object comparison and manipulation:

    neg_two = Curset(-2)
    quarter = Curset(1/4)
    result = neg_two * quarter

    # result will now be -1.0

    Consult the test file for further examples.
    """

    def __init__ (self, form):
        if type(form) in [tuple,list]:
            assert len(form) == 2, 'tuple input must have 2 elements'
            self.left, self.right = form[:]
        elif type(form) in [int, float, Fraction]:
            self.left, self.right = (construct(form))[:]

    def __len__          (x) : return len(x.form())
    def __le__      (self,o) : return le(self.form(), o.form())
    def __ge__      (self,o) : return     o <= self
    def __lt__      (self,o) : return not o <= self
    def __eq__      (self,o) : return     o <= self and self <= o
    def __gt__      (self,o) : return               not self <= o
    def __truediv__ (self,o) : return self * ~o
    def __sub__     (self,o) : return self + (-o)
    def __abs__     (self)   : return -self if le(self.form(), nil) else self
    def   form      (self)   : return (self.left,self.right)
    def __neg__     (self)   : return type(self)(negate(self.form()))
    def __float__   (self)   : return float(self.fraction())
    def __int__     (self)   : return int(float(self))
    def fraction    (self)   : return distill(self.form())


    def __mul__ (self,o):
        return type(self)(reduce(mult(
            self.form(),
            o.form() if type(o) is type(self) else o )))


    def __add__ (self,o):
        return type(self)(reduce(add(
            self.form(),
            o.form() if type(o) is type(self) else o )))


    def __getitem__ (self,i):
        if i == 0: return self.left
        if i == 1: return self.right
        else: raise TypeError(
            msg="'{}' only has index 0 (left) and 1 (right)".format(
                type(self).__name__ ) )


    def __repr__ (self):
        return '{}(({!r},{!r}))'.format(
            type(self).__name__   , 
            self.left, self.right )


    def __str__ (self):
        return '(({}),({}))'.format(
            ','.join(str(l) for l in self.left ) ,
            ','.join(str(l) for l in self.right) )


    def __invert__ (self):
        return type(self)(reduce(invert(self.form())))


