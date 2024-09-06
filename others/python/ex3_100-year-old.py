### The Year When I am 100 years old ###
# taken from http://www.practicepython.org/exercise/2014/01/29/01-character-input.html #

import datetime as dt

rightNow = dt.datetime.now().year
age = int(input("Enter your age: "))
name = input("And your name, please: ")

print("Hello", name+".", "In the year of", str(rightNow+(100-age)) + ",", "you are going to be 100 years old.")

# I was going to skip this example because it seemed too easy for my arrogant brain but I didn't.
# And that was how I learned how to use "datetime" module from a user's comment
# Note to myself: “You're not a beautiful and unique snowflake. You're the same decaying organic matter as everything else."
