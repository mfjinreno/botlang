from botlang_interpreter import run as bl_run

text = '''
def func1(arg):
    print(arg)
    if _FRONT_NEIGHBOR == "ENEMY":
        print("HELLO")
        return $ATTACK
    else:
        print("WORLD")
        return $MOVE
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

