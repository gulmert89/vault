### PracticePython.org - Exercise 12: List Ends ###
# http://www.practicepython.org/exercise/2014/04/25/12-list-ends.html #

# The question is: Write a program that takes a list of numbers (for example, a = [5, 10, 15, 20, 25]) and
# makes a new list of only the first and last elements of the given list. For practice, write this code inside a function.

def myList(elements):
    list1 = elements.split(" ")    # split() already gives me a list. Nice!
    list2 = [list1[0], list1[-1]]    # but the elements are not integers. They are still strings. I don't like it.
    list2 = list(map(int, list2))    # ask Google the right questions and the answers shall appear. Now we have integers!
    print(list2)
    
yourInput= input("Enter a list of numbers divided by space: ")
myList(yourInput)

# For some time now, I was wondering how one can give multiple inputs divided by spaces, i.e 1 3 12 150 42.
    # I came up with .split() module to do that and it fit to this problem nicely. Maybe there exists a 
    # different input() for providing multiple inputs. I won't use my Googling skills at once.
# Note to myself:
# 1) I know what map() does but knowing something is different than internalising it. That was an exciting usage of map()!
# 2) I saw a few tricks to reduce the number of lines but as it's said: "Readability counts."
