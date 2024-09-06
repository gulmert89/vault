### A simple problem from ProjectEuler.net ###
# https://projecteuler.net/problem=1 #

# The question: "Find the sum of all the multiples of 3 or 5 below 1000."

threeFive = []
for i in range(1000):
    if i%3==0 or i%5==0:
        threeFive.append(i)
print(sum(threeFive))

# Well, I tried an empty tuple first and you know what? 'tuple' object has no attribute 'append'
# I will never understand those perfectionist people who hate mistakes. This is how you learn man! Are you crazy?

# I was about to write "Some people were able to reduce the code to 3 lines!" then I saw this:
# sum([x for x in range(1, 1000) if 0 in (x % 5, x % 3)])    *sigh*
