class boolBrute:
        def __init__(self, ranges, verbose=False):
            self.ranges = ranges
            self.verbose = verbose 

            self.setup()

        def setup(self):
            # Set up checking the first range
            self.rangeindex = 0
            self.setInputRange()

            self.foundrange = False         # Have we found a valid range to test within?
            self.notFound = False           # Have we exausted all options and found nothing?
            self.checkedUpperSet = False    # Are we checking the upper set?
            self.singles = False            # Are we working with single characters?

        def reset(self):
            # Just an alias so that it makes a bit more sense
            self.setup()
        
        def verbosePrint(self, msg):
            if self.verbose:
                print(">BoolBrute< " + msg)

        # Set what input range we are currently dealing with
        def setInputRange(self):
            try:
                splitarray = self.ranges[self.rangeindex].split('-')
            except IndexError:
                # All of the arrays have been checked, none of them contain the right answer
                self.verbosePrint("Value is in none of the ranges supplied!")
                self.notFound = True
                return False

            # Convert each one to character code, makes it easier to find a midpoint 
            self.lower = ord(splitarray[0])
            self.higher = ord(splitarray[1])
            
            # If the range is the incorrect way around, switch it around
            if(self.lower > self.higher):
                temp = self.lower
                self.lower = self.higher
                self.higher = temp
            
            # Calculate the middle point
            self.middle = self.getMidpoint() 

            self.verbosePrint(("New Input Range - Lower: {0}/{1}, Higher {2}/{3}, middle {4}/{5}").format(self.lower, chr(self.lower), self.higher, chr(self.higher), self.middle, chr(self.middle)))

        # Return the middle character between the character codes of lower/higher
        def getMidpoint(self):
            return int(round((self.lower+self.higher)/2))

        # If the result was not in this range
        def checkResult(self, resultInput):
            if resultInput:
                # If result was in the range
                if self.singles:
                    # We have found the correct character, return true to the parent program so they can add to list.
                    return True
                else:
                    if not self.foundrange:
                        self.foundrange = True
                    else:
                        # Set the new upper/lower value
                        if self.checkedUpperSet:
                            # It was the top half
                            self.lower = self.middle
                            self.middle = self.getMidpoint()
                        else:
                            # It we the bottom half
                            self.higher = self.middle
                            self.middle = self.getMidpoint()
                    
                        # Reset state 
                        self.checkedUpperSet = False 
                return False
            else:
                if not self.foundrange:
                    # if the initial input range is incorrect, change it.
                    self.rangeindex = self.rangeindex + 1
                    self.setInputRange()
                else:
                    # We assume that we have checked lower first, check if we have done upper yet
                    if not self.checkedUpperSet:
                        self.checkedUpperSet = True
                    else: 
                        # Neither the lower set or upper set match
                        # Theres been a problem! Fail out, reset then set up a False return in getCurrentRange
                        self.reset()
                        self.notFound = True
                        self.verbosePrint("Didn't find anything in the range of > [lower: {0}, higher: {1}]".format(chr(self.lower), chr(self.higher)))
        
        # Create range syntax for parent program
        def rangeSyntax(self, one, two):
            if one == two:
                self.verbosePrint("setting Singles for one: {0}, two: {1}".format(chr(one), chr(two)))
                self.singles = True
                return chr(one)
            else:
                self.singles = False
                return "[" + chr(one) + "-" + chr(two) + "]" 
        
        # Get the current range the parent program needs to test.
        def getCurrentRange(self):
            if self.notFound:
                # If we didn't find anything, return false and let the parent deal with it.
                return False

            if not self.foundrange:
                # If we haven't found the top range, return full range 
                return self.rangeSyntax(self.lower, self.higher)
            elif self.singles:
                # If we are working with single characters
                if not self.checkedUpperSet:
                    return chr(self.lower)
                else:
                    return chr(self.higher)
            else:
                # Working with ranges
                if not self.checkedUpperSet:
                    # Return the lower set
                    return self.rangeSyntax(self.lower, self.middle)
                else:
                    # Return the upper set
                    return self.rangeSyntax(self.middle, self.higher)
