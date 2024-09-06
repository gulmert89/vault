### My Fibonacci Obsession ###

# So, what's happening here?
# First input  : Create a series of Fibonacci numbers up to a point
# Second input : Gives that nth Fibonacci number

fibo_input1 = int(input("Up to which number will the Fibonacci series be listed: "))

fibo_series = [0]
former, latter = 0, 1

while latter <= fibo_input1:
    fibo_series.append(latter)
    former, latter = latter, (former+latter)
print("Here the series is:\n", fibo_series)

while True:
    fibo_input2 = int(input("\nCurious about the nth Fibonacci element? Enter a number to find out: "))
    if fibo_input2 != "":
        if fibo_input2 > 0:
            while len(fibo_series) <= fibo_input2:
                fibo_series.append(latter)
                former, latter = latter, (former+latter)
            print("Your Fibonacci number is:", fibo_series[fibo_input2-1])
        else:
            print("Why don't you enter a positive integer?")

# Note to myself: Please make the second part (or the code itself) lighter. It's recalculating the list needlessly, imo.
# This is the first time I've ever used these looping input stuff. I didn't know how to do that and the answer was just so simple.
