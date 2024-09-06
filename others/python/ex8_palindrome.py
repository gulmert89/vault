# "A palindrome is a word, number, phrase, or other sequence of characters
# which reads the same backward as forward, such as 'madam', 'racecar' or 'Was it a car or a cat I saw'." - Wiki
# So, the question is whether your input is a palidrome or not.

palindrome_str = (input("Checking whether your input is a palindrome or not: ").replace(" ","")).lower()

# I wanted to make sure that there would be no space between the letters! So the .replace() module is introduced.
# Also knowing that "A" == "a" is False, all the characters should be lowercase.
# After completing this Exercise-6 of PracticePython.org, I saw similar palindrome codes on the net but most of them
# didn't have this "fail-safe" modules. For example, "Murder for a jar of red rum" failed on those codes.
# Mine prevailed! Muhahaha!

palindrome = list(palindrome_str)

palindrome_back = palindrome[::-1]    # [1]
print(palindrome_str, end="\n")

if palindrome==palindrome_back:
    print("Your input is a palindrome.")
else:
    print("Your input is not a palindrome.")
    
# Note to myself:
# [1]: I was trying to match the words letter by letter but after spending 4 hours, I gave up and cheated this time :(
# I don't know why I was trying the hard way but I still want to make it work and write it as another solution, "Solution 2" perhaps.
# I'll revisit it later but let me put my old code here. It doesn't work for some of the words though.
# Update: Yes, I "revisited" the code and it seems to work now. At that time, I didn't know case-sensitivity was in my way.

# Solution 2
pal = input("Checking whether your input is a palindrome or not: ")
pal = pal.lower()            # let's eliminate case-sensitivity
pal = pal.replace(" ","")    # and any white spaces from the sentence.

list1 = []
list2 = []
for i in range(0,(len(pal)-1)//2):
    list1.append(pal[i])
    list2.append(pal[len(pal)-1-i])
if list1 == list2:
    print("Your input is a palindrom!")
else:
    print("Your input is not a palindrom.")
# these two examples are working fine right now: "Murder for a jar of red rum", "Was it a car or a cat I saw"
# if you find a word or a sentence that doesn't work on my code, please let me know. That would be a good practice for me.
