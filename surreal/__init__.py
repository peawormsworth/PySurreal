import unittest
import random
from math import log
from fractions import Fraction
from random import choice

class Surreal ():

    def __init__ (self,lesser=[],greater=[]):
        self.lesser  = lesser
        self.greater = greater

    def __add__ (x,y):
        if x.is_zero() : return y
        if y.is_zero() : return x
        return Surreal(
            [ xl+y for xl in x.lesser  ] + [ x+yl for yl in y.lesser  ],
            [ xg+y for xg in x.greater ] + [ x+yg for yg in y.greater ]
        )

    def __neg__ (self):
        return Surreal(
            [ -greater for greater in self.greater ],
            [ -lesser  for lesser  in self.lesser  ]
        )

    def __le__ (a,b):
        return True if a is b else all(
            [ (not b <= lesser ) for lesser  in a.lesser  ] +
            [ (not greater <= a) for greater in b.greater ]
        )
            
    def __ge__  (a,b) : return not a <= b or b <= a
    def __gt__  (a,b) : return not a <= b
    def __eq__  (a,b) : return a <= b and b <= a
    def __lt__  (a,b) : return a <= b and not b <= a
    def __sub__ (a,b) : return a + (-b)
    def __truediv__ (a,b) : return a * ~b

    def is_zero(self)    : return self == self.zero()
    def is_one(self)     : return self == self.one()
    def is_neg_one(self) : return self == self.neg_one()

    def __invert__ (x):
        zero = x.zero()
        one  = x.one()
        if   x == zero : raise ZeroDivisionError
        elif x <= zero : print("LESSSSSSSS THAN XERO");return -(~(-x))
        elif x == one  : return x
        else:
            xl = [ n for n in x.lesser if n >= zero ]
            xg = x.greater
            return Surreal(
                [ zero                                               ]+
                [ (one + (xxg - x) * ~xxl) * ~xxg for xxl in xl for xxg in xg ]+
                [ (one + (xxl - x) * ~xxg) * ~xxl for xxl in xl for xxg in xg ],
                [ (one + (xxl - x) * ~xxl) * ~xxl for xxl in xl ]+
                [ (one + (xxg - x) * ~xxg) * ~xxg for xxg in xg ]
            )

    def __mul__ (x,y):
        if x.is_zero()    : return  x
        if y.is_zero()    : return  y
        if x.is_one()     : return  y
        if y.is_one()     : return  x
        if x.is_neg_one() : return -y
        if y.is_neg_one() : return -x
        xl = x.lesser
        yl = y.lesser
        xg = x.greater
        yg = y.greater
        return Surreal(
            [ xxl*y + x*yyl - xxl*yyl for xxl in xl for yyl in yl ]+
            [ xxg*y + x*yyg - xxg*yyg for xxg in xg for yyg in yg ],
            [ xxl*y + x*yyg - xxl*yyg for xxl in xl for yyg in yg ]+
            [ x*yyl + xxg*y - xxg*yyl for yyl in yl for xxg in xg ]
        )

    def one (self):
        if not hasattr(self,'_one'):
            self._one = type(self)(lesser=[self.zero()])
        return self._one

    def zero (self): 
        if not hasattr(self,'_zero'):
            self._zero = type(self)()
        return self._zero

    def neg_one (self): 
        if not hasattr(self,'_neg_one'):
            self._neg_one = type(self)(greater=[self.zero()])
        return self._neg_one

    def equivelence_in (self,surreals={}):
        for label in surreals:
            if self == surreals[label]: 
                return label
        return None

    def name_in (self,s):
        return self.equivelence_in(s)

    #def __repr__ (self):
        #return "{}({})".format(type(self).__name__, self.__str__())

    def __str__ (self):
        lesser  = ','.join(str(l) for l in self.lesser )
        greater = ','.join(str(l) for l in self.greater)
        return '{}{}|{}{}'.format('{',lesser,greater,'}')



def canal (r=[Fraction(0)]):
    yield r[0]
    while 1:
        yield r[0] - 1
        rn = [r[0]]
        for n in r[1:]:
            mid = (rn[-1]+n)/2
            yield mid
            rn.append(mid)
            rn.append(n)
        yield rn[-1]+1
        r = [rn[0]-1] + rn + [rn[-1]+1]


def creation (days=7):
    birth = canal()
    next(birth)
    labels = []
    numbers = {}
    numbers = {0 : Surreal() }
    for generations in range(1,days):
        ll = sorted(numbers.keys())
        for n in range(len(ll)+1):
            v = next(birth)
            lesser, greater = [],[]
            if n > 0:
                lesser = [numbers[ll[n-1]]]
            if n < len(ll):
                greater = [numbers[ll[n]]]

            numbers[v] = Surreal(lesser,greater)
            labels.append(v)
    return numbers


class SurrealTests(unittest.TestCase):
    verbose = 1

    
    def test_common_name(self):
        s = creation(days=7)
        birth = canal()
        numbers = []
        order   = []
        for i in range (len(s)):
            label = next(birth)
            order.append(str(s[label]))
            numbers.append(str(label))
        for i in range(len(order)):
            for j in range(i+1,len(order)):
                order[j] = order[j].replace(str(order[i]),numbers[i])
        for number in range(len(numbers)):
            #if self.verbose: print('check {} {} has a common form {}'.format(numbers[number],s[numbers[number]],self.common_format[numbers[number]]))
            #print(s)
            if self.verbose: print('check {} has a common form {}'.format(numbers[number],order[number]))
            self.assertEqual(order[number], self.common_format[numbers[number]], 
                msg='Error {}: thought {}, but got {}'.format(numbers[number], self.common_format[numbers[number]], order[number])
            )
        

    # 7 days = 30s
    def test_comparative(self):
        s = creation(days=7)
        print('\ncompare {}×{} numbers in 6 ways for {} comparisons.'.format(len(s),len(s),6*len(s)**2))
        for i in s:
            for j in s:
                if self.verbose: print('check < <= == => > relations between {} and {}'.format(i,j))
                self.assertIs( i< j, s[i]< s[j], msg='Error: {} <  {} ≠ {}'.format(i,j,s[i]< s[j]) )
                self.assertIs( i<=j, s[i]<=s[j], msg='Error: {} <= {} ≠ {}'.format(i,j,s[i]<=s[j]) )
                self.assertIs( i==j, s[i]==s[j], msg='Error: {} == {} ≠ {}'.format(i,j,s[i]==s[j]) )
                self.assertIs( i>=j, s[i]>=s[j], msg='Error: {} >= {} ≠ {}'.format(i,j,s[i]>=s[j]) )
                self.assertIs( i> j, s[i]> s[j], msg='Error: {} >  {} ≠ {}'.format(i,j,s[i]> s[j]) )
        print('\ndone.\n\ncomparison success: these numbers operate according to their given labels.')


    # 11 days = 30s
    def test_negation(self):
        "Negation Tests"
        s = creation(days=11)
        print('\ncompare {} negated numbers with their negated label.'.format(len(s)))
        for i in s:
            if self.verbose: print('check -({:8}) = {:8}'.format(str(i),str(-i)))
            assert -s[i] == s[-i], '  calc: {}'.format(-s[i] == s[-i])
        print('\ndone.\n\nnegation success: these numbers operate according to their given labels.')


    # 6 days = 30s
    def test_addition(self):
        s = creation(days=6)
        print('\nSum {}×{} numbers with each other where the solution is also a label.'.format(len(s),len(s)))
        for i in s:
            for j in s:
                if i+j in s:
                    if self.verbose: print('check {:>6} + {:>6} = {:>6}'.format(str(i),str(j),str(i+j)))
                    self.assertEqual(s[i+j], s[i]+s[j], msg='incorrect calculation: {:>6} + {:>6} = {:>6}'.format(str([i]),str(s[j]),str(s[i]+s[j])))
        print('\ndone.\n\naddition success: these numbers operate according to their given labels.')


    # 6 days = 30s
    def test_subtraction(self):
        s = creation(days=6)
        print('\nSubtract {}×{} numbers with each other where the solution is also a label.'.format(len(s),len(s)))
        for i in s:
            for j in s:
                if i-j in s:
                    if self.verbose: print('check {:>6} - {:>6} = {:>6}'.format(str(i),str(j),str(i-j)))
                    assert s[i-j] == s[i]-s[j], 'incorrect calculation: {:>6} - {:>6} = {:>6}'.format(str(s[i]),str(s[j]),str(s[i]-s[j]))
        print('\ndone.\n\nsubtraction success: these numbers operate according to their given labels.')


    # 4 days = 30s
    def test_multiplication(self):
        s = creation(days=3)
        print('\nMultiply {} labels from each other where the solution is also a label.'.format(len(s)))
        for i in s:
            for j in s:
                if i*j in s:
                    if self.verbose: print('multiply {:>6} *{:>6} ={:>6}'.format(str(i),str(j),str(i*j)))
                    assert s[i*j] == s[i]*s[j], 'incorrect calculation: {} * {} = {}'.format(s[i],s[j],s[i]*s[j])
        print('\ndone.\n\nmultiplication success: these surreal numbers operate according to their given labels.')


    common_format = {
         '0' : '{|}'          ,
        '-1' : '{|0}'         ,
         '1' : '{0|}'         ,
        '-2' : '{|-1}'        ,
      '-1/2' : '{-1|0}'       ,
       '1/2' : '{0|1}'        ,
         '2' : '{1|}'         ,
        '-3' : '{|-2}'        ,
      '-3/2' : '{-2|-1}'      ,
      '-3/4' : '{-1|-1/2}'    ,
      '-1/4' : '{-1/2|0}'     ,
       '1/4' : '{0|1/2}'      ,
       '3/4' : '{1/2|1}'      ,
       '3/2' : '{1|2}'        ,
         '3' : '{2|}'         ,
        '-4' : '{|-3}'        ,
      '-5/2' : '{-3|-2}'      ,
      '-7/4' : '{-2|-3/2}'    ,
      '-5/4' : '{-3/2|-1}'    ,
      '-7/8' : '{-1|-3/4}'    ,
      '-5/8' : '{-3/4|-1/2}'  ,
      '-3/8' : '{-1/2|-1/4}'  ,
      '-1/8' : '{-1/4|0}'     ,
       '1/8' : '{0|1/4}'      ,
       '3/8' : '{1/4|1/2}'    ,
       '5/8' : '{1/2|3/4}'    ,
       '7/8' : '{3/4|1}'      ,
       '5/4' : '{1|3/2}'      ,
       '7/4' : '{3/2|2}'      ,
       '5/2' : '{2|3}'        ,
         '4' : '{3|}'         ,
        '-5' : '{|-4}'        ,
      '-7/2' : '{-4|-3}'      ,
     '-11/4' : '{-3|-5/2}'    ,
      '-9/4' : '{-5/2|-2}'    ,
     '-15/8' : '{-2|-7/4}'    ,
     '-13/8' : '{-7/4|-3/2}'  ,
     '-11/8' : '{-3/2|-5/4}'  ,
      '-9/8' : '{-5/4|-1}'    ,
    '-15/16' : '{-1|-7/8}'    ,
    '-13/16' : '{-7/8|-3/4}'  ,
    '-11/16' : '{-3/4|-5/8}'  ,
     '-9/16' : '{-5/8|-1/2}'  ,
     '-7/16' : '{-1/2|-3/8}'  ,
     '-5/16' : '{-3/8|-1/4}'  ,
     '-3/16' : '{-1/4|-1/8}'  ,
     '-1/16' : '{-1/8|0}'     ,
      '1/16' : '{0|1/8}'      ,
      '3/16' : '{1/8|1/4}'    ,
      '5/16' : '{1/4|3/8}'    ,
      '7/16' : '{3/8|1/2}'    ,
      '9/16' : '{1/2|5/8}'    ,
     '11/16' : '{5/8|3/4}'    ,
     '13/16' : '{3/4|7/8}'    ,
     '15/16' : '{7/8|1}'      ,
       '9/8' : '{1|5/4}'      ,
      '11/8' : '{5/4|3/2}'    ,
      '13/8' : '{3/2|7/4}'    ,
      '15/8' : '{7/4|2}'      ,
       '9/4' : '{2|5/2}'      ,
      '11/4' : '{5/2|3}'      ,
       '7/2' : '{3|4}'        ,
         '5' : '{4|}'         ,
        '-6' : '{|-5}'        ,
      '-9/2' : '{-5|-4}'      ,
     '-15/4' : '{-4|-7/2}'    ,
     '-13/4' : '{-7/2|-3}'    ,
     '-23/8' : '{-3|-11/4}'   ,
     '-21/8' : '{-11/4|-5/2}' ,
     '-19/8' : '{-5/2|-9/4}'  ,
     '-17/8' : '{-9/4|-2}'    ,
    '-31/16' : '{-2|-15/8}'   ,
    '-29/16' : '{-15/8|-7/4}' ,
    '-27/16' : '{-7/4|-13/8}' ,
    '-25/16' : '{-13/8|-3/2}' ,
    '-23/16' : '{-3/2|-11/8}' ,
    '-21/16' : '{-11/8|-5/4}' ,
    '-19/16' : '{-5/4|-9/8}'  ,
    '-17/16' : '{-9/8|-1}'    ,
    '-31/32' : '{-1|-15/16}'  ,
    '-29/32' : '{-15/16|-7/8}',
    '-27/32' : '{-7/8|-13/16}',
    '-25/32' : '{-13/16|-3/4}',
    '-23/32' : '{-3/4|-11/16}',
    '-21/32' : '{-11/16|-5/8}',
    '-19/32' : '{-5/8|-9/16}' ,
    '-17/32' : '{-9/16|-1/2}' ,
    '-15/32' : '{-1/2|-7/16}' ,
    '-13/32' : '{-7/16|-3/8}' ,
    '-11/32' : '{-3/8|-5/16}' ,
     '-9/32' : '{-5/16|-1/4}' ,
     '-7/32' : '{-1/4|-3/16}' ,
     '-5/32' : '{-3/16|-1/8}' ,
     '-3/32' : '{-1/8|-1/16}' ,
     '-1/32' : '{-1/16|0}'    ,
      '1/32' : '{0|1/16}'     ,
      '3/32' : '{1/16|1/8}'   ,
      '5/32' : '{1/8|3/16}'   ,
      '7/32' : '{3/16|1/4}'   ,
      '9/32' : '{1/4|5/16}'   ,
     '11/32' : '{5/16|3/8}'   ,
     '13/32' : '{3/8|7/16}'   ,
     '15/32' : '{7/16|1/2}'   ,
     '17/32' : '{1/2|9/16}'   ,
     '19/32' : '{9/16|5/8}'   ,
     '21/32' : '{5/8|11/16}'  ,
     '23/32' : '{11/16|3/4}'  ,
     '25/32' : '{3/4|13/16}'  ,
     '27/32' : '{13/16|7/8}'  ,
     '29/32' : '{7/8|15/16}'  ,
     '31/32' : '{15/16|1}'    ,
     '17/16' : '{1|9/8}'      ,
     '19/16' : '{9/8|5/4}'    ,
     '21/16' : '{5/4|11/8}'   ,
     '23/16' : '{11/8|3/2}'   ,
     '25/16' : '{3/2|13/8}'   ,
     '27/16' : '{13/8|7/4}'   ,
     '29/16' : '{7/4|15/8}'   ,
     '31/16' : '{15/8|2}'     ,
      '17/8' : '{2|9/4}'      ,
      '19/8' : '{9/4|5/2}'    ,
      '21/8' : '{5/2|11/4}'   ,
      '23/8' : '{11/4|3}'     ,
      '13/4' : '{3|7/2}'      ,
      '15/4' : '{7/2|4}'      ,
       '9/2' : '{4|5}'        ,
         '6' : '{5|}'
}


if __name__ == '__main__':

    # TODO: show command to run tests with/out verbosity
    unittest.main(verbosity=2)

