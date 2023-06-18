from botlang_lexer import Lexer
from botlang_parser import Parser
from botlang_interpreter import run as bl_run
import json

text = '''
def func1(arg):
    PRINT(arg)
    if arg == 1:
        PRINT("HELLO")
        return 1
    else:
        PRINT("WORLD")
        return arg
    END
END

func1(2)
'''

result, error = bl_run("<stdin>", text)

if error:
    print(error.as_string())
elif result:
    if len(result.elements) == 1:
        print(repr(result.elements[0]))
    else:
        print(result)

