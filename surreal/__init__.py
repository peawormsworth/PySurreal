import unittest
import random
from math import log
from fractions import Fraction

VERBOSE = 0

class Surreal ():
    def __init__ (self,lesser,greater):
        self.lesser  = lesser
        self.greater = greater

    def find_equivelence (self,s):
        #for label in s.keys():
        for label in s:
            if self == s[label]: 
                return label
        return None

    def __repr__ (self):
        return "{}({})".format(type(self).__name__,self.__str__())

    def __str__ (self):
        d = '[]'
        lesser = self.lesser
        if lesser is None:
            lesser = d
        greater = self.greater
        if greater is None:
            greater = d
        return '{}{},{}{}'.format(d[0],lesser,greater,d[1])

    def __neg__ (self):
        try:
            greater = -self.lesser
        except:
            greater = None
        try:
            lesser = -self.greater
        except:
            lesser = None
        return Surreal(lesser,greater)

    def __le__ (a,b):
        if a is b:
           return True
        try:
            return not (b <= a.lesser) and not (b.greater <= a)
        except (AttributeError, TypeError) as e:
            return False

    def __ge__ (a,b):
        if b:
           return not a <= b or b <= a
        return False

    def __gt__ (a,b):
        return not a <= b

    def __eq__ (a,b):
        return a <= b and b <= a

    def __lt__ (a,b):
        return a <= b and not b <= a

    def __add__ (a,b):
        if b is None:
            return a

        if b.lesser is None and b.greater is None:
            #return a
            return a

        if a.lesser is None and a.greater is None:
            #return b
            return b

        if a.lesser is None:
            lesser = None
        else:
            lesser = a.lesser + b

        if b.lesser is None:
            b_lesser = None
        else:
            b_lesser = a + b.lesser

        if lesser is None or lesser <= b_lesser:
            lesser = b_lesser

        if a.greater:
            greater = a.greater + b
        else:
            greater = None

        if b.greater:
            b_greater = a + b.greater
        else:
            b_greater = None

        if greater is None or b_greater <= greater:
            greater = b_greater

        #print('making: {}|{}'.format(lesser,greater))
        return Surreal(lesser,greater)


def canal (r=[Fraction(0)]):
    yield r[0]
    while 1:
        yield r[0]-1
        rn = [r[0]]
        for n in r[1:]:
            mid = (rn[-1]+n)/2
            yield mid
            rn.append(mid)
            rn.append(n)
        yield rn[-1]+1
        rn = [rn[0]-1] + rn + [rn[-1]+1]
        r = rn

def creation (days=7):
    birth = canal()
    next(birth)
    labels = []
    numbers = {}
    numbers = {0 : Surreal(None,None) }
    for generations in range(1,days):
        ll = sorted(numbers.keys())
        for n in range(len(ll)+1):
            v = next(birth)
            if n == 0:
                lesser = None
            else:
                lesser = numbers[ll[n-1]]
            try:
                greater = numbers[ll[n]]
            except IndexError as e:
                greater = None

            numbers[v] = Surreal(lesser,greater)
            labels.append(v)
    return numbers


class SurrealTests(unittest.TestCase):

    s = creation(days=7)

    def test_compare(self):
        "compare equalities of random surreals with known labels"
        s = self.s
        
        labels = list(s.keys())
        for i in range(2000):
            i = random.choice(labels)
            j = random.choice(labels)
            if VERBOSE: print('check {} >  {} is {}'.format(i,j,i>j))
            #print('it {}'.format('is' if (s[i]>s[j])==(i>j) else 'IS NOT'))
            self.assertEqual(s[i]> s[j],i> j)
            if VERBOSE: print('check {} >= {} is {}'.format(i,j,i>=j))
            self.assertEqual(s[i]>=s[j],i>=j)
            if VERBOSE: print('check {} == {} is {}'.format(i,j,i==j))
            self.assertEqual(s[i]==s[j],i==j)
            if VERBOSE: print('check {} <= {} is {}'.format(i,j,i<=j))
            self.assertEqual(s[i]<=s[j],i<=j)
            if VERBOSE: print('check {} <  {} is {}'.format(i,j,i< j))
            self.assertEqual(s[i]< s[j],i< j)


    def test_known_equivelence_class (self):
        "known equivelence tests"
        s = self.s
        data = (
            (-1    ,      1, s[ 0]),
            ( 2.5  ,    4.5, s[ 3]),
            ( 1.125,      5, s[ 2]),
            (-2.125, -1.875, s[-2]),
        )
        for lesser,greater,equivelent in data:
            number = Surreal(s[lesser],s[greater])
            self.assertEqual(number,equivelent)

     
    def test_random_equivelence_class (self):
        "random equivelence tests"
        s = self.s
        labels = list(s.keys())
        for r in range(6):
            i = random.choice(labels)
            j = random.choice(labels)
            if j < i:
                i,j = j,i
            number = Surreal(s[i],s[j])
            print('\n{} check if Surreal({},{}) already has a label'.format(r,i,j))
            e = number.find_equivelence(s)
            print(' {}. Found label: {}'.format('No' if e is None else 'Yes',e))
            self.assertIsNotNone(number.find_equivelence(s))


    def test_negation(self):
        "negation"
        s = self.s
        #for i in s.keys():
        labels = list(s.keys())
        for c in range(300):
            i = random.choice(labels)
            if VERBOSE: print('verify -s[{}] == s[-{}], {} == {}'.format(i,i,-s[i],s[-i]))
            self.assertEqual(-s[i], s[-i])



if __name__ == '__main__':
    s = creation(days=14)

    # run tests...
    unittest.main(verbosity=2)


