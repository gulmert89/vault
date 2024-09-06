# This is actually a useful code to turn TEXT based numbers to ACTUAL numbers.
# ...and it's a 'kata' from codewars.com and -of course- has a much simpler
# and shorter solution but I'll stick to mine for now.
# PS: It took me a day to come up with a working solution.

# There is actually 1 rule: Use a dash between two-digit numbers > 19
# i.e, "forty-five", "twenty-one" etc.

def parse_int(string):
    # Let's define 'some' numbers
    zero_to_nineteen = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen"
    twenty_to_hundred = "twenty thirty forty fifty sixty seventy eighty ninety hundred"
    hundred_to_decillion = "thousand million billion trillion quadrillion quintillion sextillion septillion octillion nonillion decillion"

    # ...and put them to a dictionary.
    numbers = {word: numero for numero, word in enumerate(zero_to_nineteen.split())}
    numbers.update({word: 10 * numero for numero, word in enumerate(twenty_to_hundred.split(), 2)})
    numbers.update({word: 1000 ** numero for numero, word in enumerate(hundred_to_decillion.split(), 1)})

    # Split the input string to a list.
    string = string.split(" ")
    num_list = list()

    # Convert the string elements  to numbers and append them to the num_list.
    for s in string:
        if "-" in s:
            s = s.split("-")  # for the two-digit numbers like ninety-one
            num_list.append(numbers[s[0]]+numbers[s[1]])
        elif s == "and":
            pass  # ignore the "and" between: i.e, one hundred and ninety-one
        else:
            try:
                num_list.append(numbers[s])
            except KeyError:
                pass  # pass the KeyErrors like extra spaces, tabs etc.

    # Decode the list of numbers to natural numbers.
    def decode(num_list):
        # After 100 and multiples of it,
            # 1) the function will work recursively,
            # 2) for loop will check all the big numbers. 
        for big_n in list(numbers.values())[28:][::-1]:  # 28: index of 100
            if big_n in num_list:
                left_side = num_list[0:num_list.index(big_n)]
                right_side = num_list[1+num_list.index(big_n):]
                # left_side conditions:
                if len(left_side) == 1:
                    left_side = left_side[0]
                else:
                    left_side = decode(left_side)
                # right_side conditions:
                if len(right_side) == 1:
                    right_side = right_side[0]
                elif any(right_side) is False:
                    right_side = 0
                else:
                    right_side = decode(right_side)

                return (big_n*left_side) + right_side
        else:  # if the num_list has only a <100 number:
            return num_list[0]

    return decode(num_list)

print(parse_int("one hundred and forty-nine million and three hundred and eighty-nine thousand seven hundred fifty-six"))
# Output: 149,389,756
