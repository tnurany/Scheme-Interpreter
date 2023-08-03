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

def test_call3():
    assert interpret("(begin (define (sub1 x) (- x 1)) (sub1 5))") == '4'    