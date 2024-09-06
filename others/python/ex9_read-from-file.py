### Read From File ###
## This is a basic file reading exercise about scraping names from the files.
## You can open nameslist.txt and Training_01.txt files (of which the links are given below) to see what is inside them.

import urllib.request as url
## I feel like I was playing in single player mode up to this point but now I have just seen how a multiplayer mode looks like.
## It's nice to import something from the net.

def sol_1():    # my solution for "PracticePython.org - Exercise 22"
    print("--- Solution 1 ---")

    ppText = url.urlopen("http://www.practicepython.org/assets/nameslist.txt").read()    # This line says: "Alright, hold my beer. I'm gonna get the file and read what's inside it."
    ppText = ppText.decode("utf-8")    # So what's it? I'm not quite sure but I couldn't get the names out of the text since they are bytes literals. So this conversion was needed. Not sure why they were not usual strings but "bytes literals" in the first place.
    ppList = ppText.split()    # Let's put the names in a list. It will easier to play with.
    ppDict = {}

    for i in ("Darth","Lea","Luke"):
        ppDict[i] = ppList.count(i)    # What I say here: "Find the name in the list, count how many times it appears and match the number to related name."

    print(ppDict)
    print("Total number of names is:",len(ppList), end="\n")


def sol_ext():  # my solution for the "Extra" part of the exercise
    print("\n--- Extra Solution ---")

    ppText_ext = url.urlopen("http://www.practicepython.org/assets/Training_01.txt").read()
    ppText_ext = ppText_ext.decode("utf-8")
    ppList_ext = ppText_ext.split()
    ppSet_category = set()
    
    for i in range(len(ppList_ext)):
    # It's always -for me anyway- fun to ponder over these for loops a few hours and keep the sanity at the end.
    # So the main idea here is finding the words between two slashes, e.g .../library/...    
        find_NextSlash = ppList_ext[i].index("/",3,(len(ppList_ext)-1))    # [1]
        each_category = ppList_ext[i][3:find_NextSlash]                    # [2]
        ppSet_category.add(each_category)                                  # [3]

    print("The total number of images is:", len(ppList_ext))
    print("The total number of categories is:", len(ppSet_category), end="\n")

sol_1()
sol_ext()

## Comments:
# [1]: All the lines has a slash at 2nd index. Thus we can check the words between the indices 3 and big-enough number, e.g ~length of that line. So this line of code tells us this: "Find me the next '/' after the 3rd index and do it for each line."
# [2]: "Nice! Now let's pull the words out of these slashes' hands.
# [3]: "Okay. Add the words into this set so it doesn't repeat again."

## Note to myself:
# Please read something about "bytes literals" and see what happens when we change it to string literals. What are the cons & pros?
# Here is the link to this example: http://www.practicepython.org/exercise/2014/12/06/22-read-from-file.html
