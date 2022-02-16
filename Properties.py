def __init__():
    global dictionary
    if not globals().get("dictionary"):
        dictionary = {}

def __set__(arg,value):
    dictionary[arg] = value

def __get__(arg):
    return dictionary[arg]