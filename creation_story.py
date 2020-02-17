#!/usr/bin/python3
from surreal import Surreal, canal
import unittest

preach = True
speech = False

symbols = '''
    ☀ ★ ☆ ☇ ☈ ☉ ☊ ☋ ☌ ☓ ☡ ☩ ☼ ☿ ♀ ♁
    ♂ ♃ ♄ ♇ ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♓ ♮
    ♯ ♰ ♱ ⚊ ⚋ ⚌ ⚍ ⚎ ⚏ ⚘ ⚙ ⚚ ⚛ ⚜ ⚞ ⚟
    ⚡ ⚨ ⚩ ⚪ ⚫ ⚬ ⚭ ⚰ ⚱ ⚲ ⚳ ⚴ ⚵ ⚶ ⚷ ⚸
'''.split()

sorted_symbols = {}
for symbol in symbols:
    sorted_symbols[symbol] = len(sorted_symbols)

def canals ():
   return (i for i in symbols)

class TestCreation (unittest.TestCase):

    def test_creation(self):

        if speech: print('\nUsing a squence of symbols\n{}'.format(' '.join(symbols)))
        if speech: print('...as labels for number as I discover them')
       

        days = 6

        day = None
        if speech: print('\n=== Morning {}'.format(day))

        if preach: print('\nThe beginning was infinite void')
        s = {}
        if speech: print('\n\n=== On day "{}" the universe was {}'.format(day,('populated' if s else 'empty')))

        # Day Zero: creation

        day  = 0
        zero = Surreal()
        if speech: print('\n=== Morning {}'.format(day))
        if preach: print('\nBorn of void, nothing separated it')
        
        birth = canal()
        name  = next(birth)
        s[name] = zero

        # I think...
        cardinality = 2 ** (days+1) - 1

        while day < days:
            todlers = []
            #names = list(sorted(list(s.keys()), key=lambda symbol: sorted_symbols[symbol]))
            names = list(sorted(float(i) for i in list(s.keys())))

            if speech or preach: print('\n\n=== On day "{}", the universe contained:\n\n  {}'.format(day,', '.join(str(i) for i in names)))
            cnt = 0
            for smaller in [None] + names:
                for bigger in names + [None]:
                    cnt += 1
                    if speech: print('\n> Test Surreal formation')
                    if speech: print('  form :  ({}|{})'.format(smaller,bigger))
                    if bigger is smaller:
                        if speech: print('\nThis form is symmetric')
                        if speech: print('  so this form is not a valid Surreal number')
                    elif bigger is not None and smaller is not None \
                        and s[bigger] < s[smaller]:

                        if speech: print('\n{} is bigger than {}'.format(smaller,bigger))
                        if speech: print('  so this form not a valid Surreal number')
                    else:
                        lesser  = [] if smaller is None else [s[smaller]]
                        greater = [] if bigger  is None else [s[bigger ]]

                        form = Surreal(lesser,greater)
                        if speech: print('  shape: ', form)

                        equivelence = form.equivelence_in(s)
                        if equivelence is None:
                            name = next(birth)
                            if speech: print('\nHappy birthday "{}"'.format(form))
                            if speech: print('  Your name is : "{}"'.format(name))
                            s[name] = form
                            #names = list(sorted(float(i) for i in list(s.keys())))
                        else:
                            if speech: print('\nThere is an equivelent name: ', equivelence)
                            eq_form = s[equivelence]
                            swap = False
                            try:
                                if eq_form.lesser < form.lesser:
                                    swap = True
                            except TypeError:
                                pass
                            try:
                                if eq_form.greater > form.greater:
                                    swap = True
                            except TypeError:
                                pass
                            if swap:
                                if speech: print('\nThis form is more ideal.')
                                if speech: print('  swapping set form entry with this one')
                                if speech: print('  (not actually doing it now)')
                                #s[equivelence] = form
                            else:
                                if speech: print('  and this is less ideal.')

                            if speech: print(' and looks like : ', eq_form)
                            if speech: print('I already have a number like this called "{}"'.format(equivelence))
            names = list(sorted(float(i) for i in list(s.keys())))
            if speech: print('count of loops is:',cnt)
            day = day + 1


        print('\n\n=== On day "{}", the universe contains:\n\n  {}'.format(day,', '.join(str(i) for i in names)))
        print('\n\nAfter day {}, the cardinality of the surreal universe is {}\n'.format(day, len(s)))
        if preach: print('...and it was {}\n'.format('good' if len(s) == cardinality else 'BAD'))


if __name__ == '__main__':

    unittest.main(verbosity=2)
    #unittest.main()

