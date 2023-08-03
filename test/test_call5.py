import os
import sys
import pytest
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.

sys.path.append(parent)
 
# now we can import the module in the parent
# directory.

from interp import interpret

def test_call5():
    assert interpret("(begin (define (duple n a) (if (= n 0) (quote ()) (cons a (duple (- n 1) a)))) (duple 5 (quote x)))") == '(x x x x x)'    