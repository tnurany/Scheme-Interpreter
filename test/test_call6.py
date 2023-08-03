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

def test_call6():
    assert interpret("(begin (define (index a L n) (if (null? L) -1 (if (eq? a (first L)) n (index a (rest L) (+ n 1))))) (index (quote d) (quote (a b c d e)) 0))") == '3'    