### The Luggage ###
# This should have been a simple "element search" exercise taken from PracticePython.org
# but it turned out to be a short story. It became kind of a text-based game.
# The link to the original example: http://www.practicepython.org/exercise/2014/11/11/20-element-search.html
# Please read it first to grasp the main point in the "solutions" here.

print("""> Now, listen to me!
> I want you to give me the list and the luggage's number.\n> If the number \"cashes\" the list, I'll let ya live.
> If not, you've got to ask yourself one question: Do I feel lucky?\n""")
list_input = input("> Don't make me wait! Write the god damn numbers in the list: ")
int_input = int(input("> Hand me the number! Come on: "))
print("> Nicely done, punk. You want the \"solution1\" or \"solution2\"?")
print("\t> solution1 simply takes your list and looks for the number inside it like a cop checking on everone's face one by one.")
print("\t> solution2 does it by a binary search. It checks your number and splits the list into two and keep... Nevermind!\n")
select_input = input("> So, which one do you want? solution1 or solution2? Tell me: ")

def solution1(l_i=list_input, i_i=int_input):
    l_i = sorted(list(map(int,(l_i.split(" ")))), reverse=False)    # from inside to outside: input numbers are filtered, turned to int by map function, converted to list, sorted.
    if i_i in l_i:
        print(f"\n> Well... The luggage #{(i_i)} seems to be in the list \"{(l_i)}\".")
        print("> It was your lucky day, kiddo. And don't take it personal. It's just business!")
    else:
        print(f"\n> Sorry. The luggage #{(i_i)} is not in the list \"{(l_i)}\".")
        print("> It's time to say goodbye!")

def solution2(l_i=list_input, i_i=int_input):
    l_i = backup_list = sorted(list(map(int,(l_i.split(" ")))), reverse=False)    # same as the above. backup_list is crated for f-string section down below.
    
    while len(l_i) > 1:
        if i_i < l_i[len(l_i)//2]:
            l_i = l_i[:(len(l_i)//2)]
        else:
            l_i = l_i[(len(l_i)//2):]
    if i_i in l_i:
        print(f"\n> Well... The number {(i_i)} you have entered IS in the list \"{(backup_list)}\".")    #I wanted to keep the original list since the while loop was keep updating l_i
        print("> It was your lucky day, kiddo. And don't take it personal. It's just business!")
    else:
        print(f"\n> Sorry. The number {(i_i)} you have entered is not in the list \"{(backup_list)}\".")
        print("> It's time to say goodbye!")

if select_input == "solution1":
    solution1()
elif select_input == "solution2":
    solution2()
else:
    print("> Wrong answer, punk!")
    print("> It's time to say goodbye!")

# I'm not sure why the game ended up being such a thriller.
# March 3, 2020:
    # Can you make the code leaner/more readable?
    # I want to add "Wanna play again, scumbag? (Yes/No)" to the end and "<Press 'Space' to continue>"
    # for a decent reading experience but not now. I'll revisit and study the code later.
    # Maybe I'll add some new features as well. It's fun!
# I introduced f-strings to myself here.
