# Let me write another question from the Project Euler:
### Problem 3: Largest prime factor
### The prime factors of 13195 are 5, 7, 13 and 29.
### What is the largest prime factor of the number 600851475143?

TARGET = 600851475143
factors = []
counter = 2
while counter <= TARGET:
    if TARGET % counter == 0:
        TARGET = TARGET // counter
        factors.append(counter)
    counter += 1
print("The list of prime factors:\n", factors, sep="")
print("where the max value is:", max(factors)) # Max Factor? Subliminal message!

# I know there can be only 1 prime factor greater than sqrt(TARGET) but I failed
# to get the largest p.number when I implement the sqrt solution.
# I checked other solutions and mine seems the simplest but maybe -as I stated-
# not the fastest. Nah... It's not a production code and it's quite fast enough
# to me. So... I wanna lean on the Pareto Principle for now :)