import this

#some commit


def enter_name():
    name = raw_input("Enter your name: ")
    if name:
        return name
    else:
        print "Sorry, try again, enter your name."
        return enter_name()
