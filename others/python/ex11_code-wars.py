# Let me copy/paste the instruction from the challenge
"""
Welcome.
In this kata ("challenge" in CodeWars language) you are required to,
given a string, replace every letter with its position in the (English) alphabet.
If anything in the text isn't a letter, ignore it and don't return it.
"a" = 1, "b" = 2, etc.
"""

# Here is the link: https://www.codewars.com/kata/546f922b54af40e1e90001da/train/python

# my lengthy solution :(
def alphabet_position_sol1(text):
    import string
    text = text.lower()    # just to keep things quite 
    text_dict = dict(enumerate(string.ascii_lowercase,1))     # Always wondered how and where I can use enumerate().
    # I kinda forced myself to use enumerate() and created the code around it. 
    reverse_it = {value:key for key, value in text_dict.items()}    # Needed to reverse the dictionary mapping. stackoverflow.com came to help.
    text_list = list()
    for i in text:
        if i.isalpha():    # Non-English letters break the deal here as they are True as well.
            text_list.append(str(reverse_it[i]))    # pulled the values from the dictionary "text_dict" and added to the list
    return " ".join(text_list)    # to make sure to comply with the solution.
    
alphabet_position_sol1("The sunset sets at twelve o' clock.")
# Output should be: "20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11"


# This solution marked as both "Best Practices" & "Clever"
def alphabet_position_sol2(text):    # Here I've learned what ord() does. Not impressed. *shrug*
    return ' '.join(str(ord(c) - 96) for c in text.lower() if c.isalpha())

alphabet_position_sol2("The sunset sets at twelve o' clock.")
# Output should be: "20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11"

# Moral of the story:
# 1) There are tens of ways to solve a problem.
# 2) Eventually somebody would reduce yours to just one fancy line of goddamned code.
# 3) I still prefer readability to understand the mindset behind the solution. So I'm not jealous, really!
