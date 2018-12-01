from boolBrute import boolBrute 
import re
letter = "uabc86zq"
addchar = False
start = "^"

bb = boolBrute(["a-z", "0-9"], True)
while 1:
    curRange = bb.getCurrentRange()
    if curRange == False:
        print("char is not in range")
        break

    print(start + curRange)
    addchar = bb.checkResult(re.match(start + curRange, letter))

    if addchar:
        addchar = False
        res = bb.getCurrentRange()
        print("FOUND:" +  res)
        start = start + res
        bb.reset()
        #print("FOUND!:" +  bb.getCurrentRange())
