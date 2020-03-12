#!/usr/bin/python3
from surreal import *
from math   import log
from random import random
import unittest
import sys

class SurealTests(unittest.TestCase):
    verbose = 1

    def test_floating_point(self):
        loops = 200
        depth = 14
        precision = 1/2**depth
        for i in range(loops):
            n = random()
            s = Sureal(construct(n,precision=precision))
            fs = float(s)
            diff = abs(n - fs)

            if self.verbose: print('''
         random float: {}
float->surreal->float: {}
           difference: {}
     log 2 difference: {}
 the log 2 difference should be > {}
'''.format(n,fs,diff,log(diff,1/2),depth))

    
    # 7 days = 30s
    def test_comparative(self):
        s = creation(days=7)
        if self.verbose: print('\ncompare {}×{} numbers in 6 ways for {} comparisons.'.format(len(s),len(s),6*len(s)**2))

        for i in s:
            for j in s:
                if self.verbose: print('check < <= == => > relations between {} and {}'.format(i,j))
                self.assertIs(s[i]< s[j], i< j, msg='Error: {} <  {} ≠ {}'.format(i,j,s[i]< s[j]) )
                self.assertIs(s[i]<=s[j], i<=j, msg='Error: {} <= {} ≠ {}'.format(i,j,s[i]<=s[j]) )
                self.assertIs(s[i]==s[j], i==j, msg='Error: {} == {} ≠ {}'.format(i,j,s[i]==s[j]) )
                self.assertIs(s[i]>=s[j], i>=j, msg='Error: {} >= {} ≠ {}'.format(i,j,s[i]>=s[j]) )
                self.assertIs(s[i]> s[j], i> j, msg='Error: {} >  {} ≠ {}'.format(i,j,s[i]> s[j]) )
        print('\ndone.\n\ncomparison success: these numbers operate according to their given labels.')


    def Xtest_negation(self):
        "Negation Tests"
        s = creation(days=11)
        print('\ncompare {} negated numbers with their negated label.'.format(len(s)))

        for i in s:
            if self.verbose: print('check -({:10}) = {:10}'.format(str(i),str(-i)))
            assert -s[i] == s[-i] #'  calc: {}'.format(-s[i] == s[-i]))
        print('\ndone.\n\nnegation success: these numbers operate according to their given labels.')


    def test_addition(self):
        day = 6
        s = creation(days=day)
        print('\nSum {}×{} numbers with each other where the solution is also a label.'.format(len(s),len(s)))

        sorted_s = sorted(s)
        for i in sorted_s:
            for j in sorted_s:
                if i+j in s:
                    try:
                        sum = s[i]+s[j]
                        if self.verbose: print('check {:>6} + {:>6} = {:>6}'.format(str(i),str(j),str(i+j)))
                        self.assertEqual(s[i+j], sum, msg='incorrect calculation: {:>6} + {:>6} = {:>6}'.format(str([i]),str(s[j]),str(sum)))
                    except KeyError as e:
                        if str(e) == "'surreal number is not in the universe'":
                            print('  skip: surreal outside universe')
                        else:
                            raise

        print('\ndone.\n\naddition success: these numbers operate according to their given labels.')


    def test_subtraction(self):
        days=6
        s = creation(days=days)
        print('\nSubtract {}×{} numbers with each other where the solution is also a label.'.format(len(s),len(s)))

        for i in s:
            for j in s:
                if i-j in s:
                    difference = s[i]-s[j]
                    if self.verbose: print('check {:>6} - {:>6} = {:>6}'.format(str(i),str(j),str(i-j)))
                    assert difference == s[i-j], 'incorrect calculation: {:>6} - {:>6} = {:>6}'.format(str(s[i]),str(s[j]),str(difference))
                    assert difference == s[i-j], 'incorrect calculation: {:>6} - {:>6} = {:>6}'.format(str(s[i]),str(s[j]),str(difference))
        print('\ndone.\n\nsubtraction success: these numbers operate according to their given labels.')


    def test_multiplication(self):
        days = 5
        s = creation(days=days)
        print('\nMultiply {} labels with each other where the solution is also a label.'.format(len(s)))

        for i in sorted(s):
            for j in sorted(s):
                if i*j in s:
                    if self.verbose: print('check : {:>5} × {:4} = {}'.format(str(i),str(j),str(i*j)))
                    product = s[i]*s[j]
                    assert s[i*j] == product, 'incorrect calculation: {} * {} = {}'.format(s[i],s[j],str(product))
        print('\ndone.\n\nmultiplication success: these surreal numbers operate according to their given labels.')

    def Xtest_inversion(self):
        days = 5
        s = creation(days=days)
        print('\nInvert {} labels'.format(len(s)))

        for i in sorted(s):
            if i == 0: continue
            try:
                print(i)
                if self.verbose: print('check : 1/({:>5}) = {}'.format(str(i),~s[i]))
            except:
                print(sys.exc_info())
        print('\ndone.\n\ninversion success: these surreal numbers operate according to their given labels.')


if __name__ == '__main__':
    unittest.main(verbosity=2)

