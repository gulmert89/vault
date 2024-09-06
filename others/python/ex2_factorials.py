### Factorial of which number we would like to calculate? ###

x = int(input("Enter the integer of which the factorial is to be calculated: "))

def fact(x):
    if x==0:    #you know, factorial of 0 is 1
        return 1
    return x * fact(x-1)  #putting a recursion practice here  would be nice 

if x>=0:
    print("The factorial of",x,"is",fact(x),end=".")
else:
    print("Please avoid negative numbers.")
    # raise ValueError("Please avoid negative numbers.")
    # ^this is an alternative answer to entering a negative number but i just like to see a simple string instead of a scary "ValueError!!"
