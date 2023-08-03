import sys
import numbers
import functools

# Global Variables to define some constant values
BASE_ENV_ID = 0


#
# Read an sexpr line by line from the a file
#
# f - a file
#
def read_sexpr(f):
    slist = ''
    for line in f:
        slist += line
    f.close()
    return slist


#
# Turn a string into a list of tokens that are separated by a space
#
# char - a string of characters
#
def tokenize(chars: str):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


#
# Turn a string representation of an sexpr into a python list representation
#
# program - an sexpr in a string
#
def parse(program: str):
    return read_from_tokens(tokenize(program))


#
# Turn a string of tokens into a python list
#
# tokens - a string of tokens
#
def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


#
# Convert a string token into a number or leave as a string
#
# token - a sequence of characters
#
def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


#
# Convert a python list as a string representation of a scheme list
#
# l - a python list
#
def sexpr_to_str(l):
    return str(l).replace('[', '(').replace(']', ')').replace(',', '').replace('\'', '')


#
# Return a builtin function representation
#
# func - a Python function
#
def makebuiltin(func):
    return [">builtin", func]


#
# Return true if parameter is a builtin function representation
#
# l - anything
#
def isbuiltin(l):
    return isinstance(l, list) and len(l) > 0 and l[0] == ">builtin"


def makeclosure(formals, body, parent_env_id):
    return [">closure", formals, body, parent_env_id]


def isclosure(l):
    return isinstance(l, list) and len(l) > 0 and l[0] == ">closure"


#
# Add a list of numbers
#
# args - a list of numbers
#
def plus(args):
    if len(args) > 0:
        if all(map(lambda a: isinstance(a, numbers.Number), args)):
            return functools.reduce(lambda a, b: a + b, args)
        else:
            raise RuntimeError("+ applied to non-number: ", sexpr_to_str(args))
    else:
        raise RuntimeError("+ must have at least one argument: (+)")


#
# Function for minus
#
def minus(args):
    if len(args) > 0:
        if all(map(lambda a: isinstance(a, numbers.Number), args)):
            return functools.reduce(lambda a, b: a - b, args)
        else:
            raise RuntimeError("- applied to non-number: ", sexpr_to_str(args))
    else:
        raise RuntimeError("- must have at least one argument: (-)")


#
# Multiply a list of numbers
# args - a list of numbers
#
def multiply(args):
    if len(args) > 0:
        if all(map(lambda a: isinstance(a, numbers.Number), args)):
            return functools.reduce(lambda a, b: a * b, args)
        else:
            raise RuntimeError("* applied to non-number: ", sexpr_to_str(args))
    else:
        raise RuntimeError("* must have at least one argument: (*)")


#
# Return the first element of a list
#
# args - a list of arguments to a call to first
#
def first(args):
    if len(args) == 1:
        arg = args[0]
        if (isinstance(arg, list) and len(arg) > 0):
            return arg[0]
        else:
            raise RuntimeError("first must be applied to a non-null list: ", sexpr_to_str(arg))
    else:
        raise RuntimeError("first must have exactly one argument: ", sexpr_to_str(args))


#
# Return the a list of all but the first element of a list
#
# args - a list of arguments to a call to rest
#

def rest(args):
    if len(args) == 1:
        arg = args[0]
        if isinstance(arg, list) and len(arg) > 0:
            return arg[1:]
        else:
            raise RuntimeError("rest must be applied to a list: ", sexpr_to_str(arg))
    else:
        raise RuntimeError("rest must have exactly one argument: ", sexpr_to_str(args))


def cons(args):
    if len(args) == 2:
        return [args[0]] + args[1]
    else:
        raise RuntimeError("cons must have exactly two arguments: ", sexpr_to_str(args))


def null(args):
    if len(args) == 1:
        arg = args[0]
        return arg == []
    else:
        raise RuntimeError("null? must have exactly one argument: ", sexpr_to_str(args))


#
# Function for =
#
def equals(args):
    if len(args) > 1:
        if all(map(lambda a: isinstance(a, numbers.Number), args)):
            return all(map(lambda a: a == args[0], args))
        else:
            raise RuntimeError("= applied to non-number: ", sexpr_to_str(args))
    else:
        raise RuntimeError("= must have at least two arguments: (=)")


def eq(args):
    if len(args) == 2:
        if isinstance(args[0], list):
            return False
        else:
            return args[0] == args[1]
    else:
        raise RuntimeError("eq? must have exactly two arguments: ", sexpr_to_str(args))


#
# Add a name, value pair to the base dictionary
#
# n - name
# v - value
#
def addbaseenv(n, v):
    base[n] = v


def addToEnv(key, value, env_id=BASE_ENV_ID):
    globalenv[env_id][key] = value


#
# Create the base environment
#
# names - base names
# vals - base values
#
def makebase(names, vals):
    if (names):
        base[names[0]] = vals[0]
        return makebase(names[1:len(names)], vals[1:len(vals)])
    else:
        return base


base = {}  # base environment dictionary
basenames = [">parent_env", "#t", "#f", "first", "+", "rest", "cons",
             "null?", "=", "-", "*", "eq?"]  # names in base environment
basevals = [None, True, False, makebuiltin(first), makebuiltin(plus), makebuiltin(rest), makebuiltin(cons),
            makebuiltin(null), makebuiltin(equals), makebuiltin(minus), makebuiltin(multiply),
            makebuiltin(eq)]  # corresponding values

# environment containing Scheme functions
globalenv = [makebase(basenames, basevals)]  # the global environment


#
# Lookup an id in an environment
#
# env - a stack of dictionaries
# id - a program id
#
def lookup(env, id):
    if (not env):
        raise RuntimeError("undefined variable reference: ", id)
    else:
        rec = env[0]
        val = rec.get(id)
        if (val == None):
            return lookup(env[1:len(env)], id)
        else:
            return val


def lookup_value(key, env):
    if env is None:
        raise RuntimeError("undefined reference: ", key)
    else:
        val = env.get(key)
        if val is not None:
            return val
        else:
            return lookup_value(key, env[">parent_env"])


#
# Interpret a Scheme expression in an environment
#
# exp - an sexpr
# env - a stack of dictionaries
#
def interp(exp, env_id=BASE_ENV_ID):
    if isinstance(exp, numbers.Number):
        return exp
    elif isinstance(exp, str):
        return lookup_value(exp, globalenv[env_id])
    elif isinstance(exp, list):
        if exp[0] == "quote":
            return exp[1]
        elif exp[0] == "if":
            if interp(exp[1], env_id):
                return interp(exp[2], env_id)
            else:
                return interp(exp[3], env_id)

        elif exp[0] == "begin":
            for _ in range(1, len(exp) - 1):
                interp(exp[_], env_id)
            return interp(exp[len(exp) - 1], env_id)

        elif exp[0] == "define":
            # Define variable
            if not isinstance(exp[1], list):
                name = exp[1]
                value = interp(exp[2], env_id)
                addToEnv(name, value, env_id)

            elif (isinstance(exp[1], list)) and (len(exp[1]) == 1):
                name = exp[1][0]
                value = interp(exp[2], env_id)
                addToEnv(name, value, env_id)

            else:
                # Define function
                func_name = exp[1][0]
                func_args = exp[1][1:]
                for arg in func_args:
                    if not isinstance(arg, str):
                        raise RuntimeError("Argument must be symbol: ", arg)
                    elif arg in func_args[func_args.index(arg) + 1:]:
                        raise RuntimeError("Argument must be unique: ", arg)
                    elif arg == func_name:
                        raise RuntimeError("Argument must be different from function name: ", arg)
                func_body = exp[2]
                func = makeclosure([func_name, func_args], func_body, env_id)
                addToEnv(func_name, func, env_id)

        elif exp[0] == "let":
            # Let Expression
            new_env = {">parent_env": globalenv[env_id]}
            globalenv.append(new_env)
            new_env_id = len(globalenv) - 1

            variables = exp[1]

            variable_names = list(map(lambda x: x[0], variables))

            # Mapping the variable
            for variable in variables:
                name = variable[0]
                if not isinstance(name, str):
                    raise RuntimeError("var name must be in let: ", name)
                elif name in variable_names[variable_names.index(name) + 1:]:
                    raise RuntimeError("var name must be unique: ", name)
                value = interp(variable[1], new_env_id)
                addToEnv(name, value, new_env_id)

            # Interpret the body
            return interp(exp[2], new_env_id)
        else:
            mfunc = interp(exp[0], env_id)
            if isbuiltin(mfunc):
                args = exp[1:len(exp)]
                margs = list(map(lambda e: interp(e, env_id), args))
                return mfunc[1](margs)
            elif isclosure(mfunc):
                # User Defined Function calls are
                func = mfunc[1][0]
                func_parameters = mfunc[1][1]
                func_body = mfunc[2]

                # a new environment
                new_env = {">parent_env": globalenv[env_id]}
                globalenv.append(new_env)
                new_env_id = len(globalenv) - 1

                # Mapping the parameter
                for parameter in func_parameters:
                    try:
                        arg = exp[1]
                        new_env[parameter] = interp(arg, new_env_id)
                        exp = exp[1:]
                    except IndexError:
                        raise RuntimeError("Not enough arguments: ", func)

                # Interpret the function
                return interp(func_body, new_env_id)
            else:
                if len(exp) == 1:
                    if isinstance(exp[0], int):
                        raise RuntimeError("Invalid Func call:", exp[0])
                    return mfunc
                else:
                    raise RuntimeError("Invalid function call: ", exp[0])

    else:
        raise RuntimeError("Invalid scheme syntax: ", sexpr_to_str(exp))


#
# Interpret an expression in the global environment
# This is the interface to the intpreter when passing the code in a string
#
# exp - an sexpr in string form
#
def interpret(exp):
    return sexpr_to_str(interp(parse(exp)))


#
# Interface to the interpreter when read the program from a file
#
# argv - the name of the file
#
def main(argv):
    f = open(argv[1], "r")
    # f = open("test.txt", "r")
    slist = read_sexpr(f)
    print(interpret(slist))


if __name__ == '__main__':
    main(sys.argv)
