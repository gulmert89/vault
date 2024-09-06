### List of prime numbers up to a user defined point ###

ep = int(input("I'm going to list the prime numbers.\nEnter the end point please: "))    #ep: end point
pl = []    #pl: prime list

for i in range(1,ep):
    for divider in range(2,i):
        if i%divider==0 and i!=2:
            break
    else:
        pl.append(i)
        
print("List of the prime numbers up to {} is:\n{}".format(ep,pl))

# Note to myself: The meaning of "else" aligned with the "for" above:
    # If none of "if" values are satisfied for all the "for" values, do the "else".
# Loved this usage of "else".
# I was a bit reluctant to use .format() while string formatting but well, it seems quite fun.
# It was quite hard to imagine how to create a "for" under a "for" to dig out the prime numbers but a simple pencil and paper helped me.
# I know it's a simple code but still, I -somehow- need to make the code simpler
    # because it divides the entire range() over and over again.
    # There was this thing about "Fermat's theorem" that states that you just need to
    # divide the number up to its square root but I don't remember what it was exactly.
