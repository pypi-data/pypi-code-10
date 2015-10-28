movies=["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
               ["Graham Chapman",["Michael Palin","John Cleese",
                                  "Terry Gilliam","Eric Idle","Terry Jones"]]]

def print_lol(the_list):
    for each_thing in the_list:
        if isinstance(each_thing,list):
            print_lol(each_thing)
        else:
            print(each_thing)

print_lol(movies)


"""This is my first Python Program."""
