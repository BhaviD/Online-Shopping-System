BLACK=30
RED=31
GREEN=32
BLUE=34
PURPLE=35

MAX_ADMIN_COUNT=2

def cursor_move(x, y):
    print ("\033[{0};{1}H".format(x, y))

def screen_clear():
    print (chr(27) + "[2J")
    cursor_move(0, 0)

def ErrorPrint(msg):
    print ("\033[1;{0}m{1}\033[0m".format(RED, msg), end='', flush=True)

def SuccessPrint(msg):
    print ("\033[1;{0}m{1}\033[0m".format(GREEN, msg), end='')

def ColorTextPrint(color, msg):
    print ("\033[1;{0}m{1}\033[0m".format(color, msg), end='')

def BoldPrint(msg):
    print ("\033[1;{0}m{1}\033[0m".format(BLACK, msg), end='')

def YesNoGet(question):
    r = input("{0} (y/n) ? ".format(question))
    while(r != "y" and r != "n"):
        ErrorPrint("Invalid Input!!\n")
        r = input("{0} (y/n) ? ".format(question))
    return r

def FloatingPointInputGet(msg):
    f=0.0
    while True:
        try:
            ff = input(msg)
            if ff == "":
                break
            f = float(ff)
            break
        except ValueError:
            ErrorPrint("Only Floating Point values accepted... please try again!!\n")
    return f
