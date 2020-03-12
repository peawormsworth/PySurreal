from fractions import Fraction

# precision and recursion depth limits.
precision     = 2**-20
max_recursion = 30

# useful surreal representations used throughout
nan  = ()
nil  = (nan,nan)
one  = (nil,nan)
neg  = (nan,nil)



def canal (r=[Fraction(0,1)]):
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
    birth  = canal()
    sprout = cleave()
    universe = {}
    for i in range(2**days-1):
        universe[next(birth)] = Surreal(next(sprout))
    return universe


# given a number, generate the surreal number
# up to the precision number as a link of lists
def construct (num,precision=precision):
    scale = 1
    form  = nil
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


# given a surreal, return its numeric value
def distill (s):
    form  = nil
    scale = 1
    lone  = None
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
    if not s:
        return nan
    l = s[0]
    for n in s[1:]: 
        if le(n,l): l = n
    return l


def greatest (s):
    if not s:
        return nan
    l = s[0]
    for n in s[1:]: 
        if le(l,n): l = n
    return l


def reduce (x):
    y = nil
    while not eq(y,x): 
        y = (y[0],y) if le(x,y) else (y,y[1])
    return y


def limit_reduce (x,p=max_recursion):
    y = nil
    b = 0
    while not eq(y,x) and b < p: 
        y = (y[0],y) if le(x,y) else (y,y[1])
        b += 1
    return y


def consolidate (x)   : return (greatest(x[0]), least(x[1]))
def negate      (x)   : return (negate(x[1]), negate(x[0])) if x else x
def absolute    (x)   : return negate(x) if le(x,nil) else x
def sub         (x,y) : return add(x,negate(y))
def eq          (x,y) : return     le(x,y) and     le(y,x)
def ne          (x,y) : return not le(x,y) and not le(y,x)
def gt          (x,y) : return not le(x,y)
def lt          (x,y) : return                 not le(y,x)
def ge          (x,y) : return                     le(y,x)


# return True if a and b are less than c apart
def within (a,b,c): return lt(absolute(sub(a,b)),c)

def le (x,y,n=0): 
    mr = max_recursion
    return n > mr or not (x[0] and le(y,x[0],n+1) or y[1] and le(y[1],x,n+1))
    return n > max_recursion or not (x[0] and le(y,x[0],n+1) or y[1] and le(y[1],x,n+1) )


def add (x,y):
    if x == nil : return y
    if y == nil : return x
    if x == nil : return y
    if y == nil : return x
    left, right = (), ()
    if len(x) > 0 and x[0] : left  = add(x[0],y)
    if len(x) > 1 and x[1] : right = add(x[1],y)
    if len(y) > 0 and y[0] : 
        under = add(x,y[0]) 
        if not left or  le(left, under): left = under
    if len(y) > 1 and y[1] :
        over  = add(x,y[1])
        if not right or le(over, right): right = over
    return (left, right)


def mult (x,y):
    if x == nil : return nil
    if y == nil : return nil
    if x == one : return y
    if y == one : return x
    if x == neg : return negate(y)
    if y == neg : return negate(x)

    xl,xr,yl,yr = (),(),(),()

    if x and x[0]: xl = x[0]
    if x and x[1]: xr = x[1]
    if y and y[0]: yl = y[0]
    if y and y[1]: yr = y[1]

    if xl: xly = mult(xl,y)
    if yl: xyl = mult(x,yl)
    if xr: xry = mult(xr,y)
    if yr: xyr = mult(x,yr)

    left,right = (),()

    if xl and yl:
        left  = sub(add(xly,xyl),mult(xl,yl))
    if xr and yr:
        other = sub(add(xry,xyr),mult(xr,yr))
        if not left or le(left,other): left = other

    if xl and yr:
        right = sub(add(xly,xyr),mult(xl,yr))
    if xr and yl:
        other = sub(add(xyl,xry),mult(xr,yl))
        if not right or le(other,right): right = other

    return reduce((left, right))


class Surreal ():

    def __init__ (self, form):
        if type(form) is tuple:
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


