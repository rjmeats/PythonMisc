# #####################################################################
#
# ATH 2019 Question (from the Poster at https://www.pablosath.com/ATHNEWS.pdf)
#
# Troubled by a string of thefts from numbered Swiss bank accounts, 
# the gnomes of Zurich (no umlauts) have increased the size of their 
# account numbers to lie between 40 and 80 digits to combat the thief. 
# "This is mad," complained account holder, Baroness Bindie Diebin. 
# "It will actually weaken security, as everyone will forget their 
# number and will have to write it down. But I can reproduce mine 
# whenever I need it. If you multiply mine by nine you get the same 
# result as taking its last digit and moving it to the front.
# #####################################################################

# So we're looking for a 40-80 digit number that when multiplied by 9 gives a value 
# which is the same as the value produced my moving the last digit of the number
# to the front. (Assume no leading zeroes allowed, otherwise 00...00 would be an answer.)
#
# i.e. If the target number is abcd...wxyz, then: 
#
#      abcd...wxyz * 9 == zabcd...wxy
#
# A couple of simple observations:
# - the target number and the target number multiplied by 9 must have the same number of digits
# - so the first digit 'a' must be a '1'
# - the last digit 'z', becomes the first digit of the number multiplied by 9, and so must be a '9'
#
# So the target number is 1bcd...wxy9, with between 40 and 80 digits.
#
# Outline of producing an answer:
# - brute force approach, but limited by need to produce an answer in a reasonable time
# - Python 3 integers have unlimited size, making it straight-forward to use them for numbers with several
#   10s of digits
# - two stages:
#   - initial investigation to try to find answers to the puzzle where the target number has a much smaller numbers of digits,
#     to find patterns and insights
#   - using what as learned in the first stage to apply to target numbers with larger numbers of digits, into the range 
#     of 40-80 digits required for the correct answer, but restricting the possibilities being tried to keep processing
#     time reasonable.
# - terminology / variable names
#   - n = the number being tested to see if it is the target number
#   - n_x_9 = 9 times n
#   - n_rotated = n with its last digit rotated to become the first digit
#   - n_diff = absolute n_difference between n_x_9 and n_rotated
#     - i.e. a measure of how close n is to being a solution to the problem
#     - other measures could be used, but luckily this worked very well and is easy to calculate
#   - n_s, n_x_9_s, n_rotated_s are string versions of the above (which are integers)

for stage in [1, 2] :

    print()
    print("Stage:", stage)
    print()

    min_digits = 4
    max_digits = 10 if stage == 1 else 80

    # Keep track of the closest we come to finding a target number.
    # best[0] = n_diff value (i.e. how close ?)
    # best[1] = n, the potential target number n
    best = (-1, 0)

    for digits in range(min_digits, max_digits+1):

        # Work out the range of numbers having this many digits to check
        if stage == 1 or digits <= 8 :
            # Brute force between (e.g. for 5 digits) 10009 and 100000
            # But can stop as soon as we reach a number which when multiplied by 9
            # has more than this number of digits. So end at 100000 // 9 + 1 = 11111 + 1
            start = (10 ** (digits-1)) + 9
            end = 10 ** (digits) // 9 + 1
        else :
            # Stage 1 output shows the following sequence of 'best' values when looking at numbers with
            # 4 - 10 digits. They all produce a 'best' value within 100 of a perfect answer, and the 'best'
            # values seem to be 'converging' towards the same set of leading digits 101123...
            #
            #   digits =  4 : best-diff = 19 : best = 1009  
            #   digits =  5 : best-diff = 29 : best = 10109 
            #   digits =  6 : best-diff = 40 : best = 101119
            #   digits =  7 : best-diff = 28 : best = 1011239
            #   digits =  8 : best-diff =  4 : best = 10112359
            #   digits =  9 : best-diff = 32 : best = 101123599
            #   digits = 10 : best-diff = 36 : best = 1011235959
            #
            # The stage 1 answers are calculated using the range of all integers with a particular number of digits that end
            # with a 9 which are less than to 111..111. For 4-9 digits, the calculation is near instant, for 10 digits, the
            # calculation takes around 20 seconds, and so this approach will not be practical for numbers of digits much above
            # 10.
            #
            # Stage 2 assumes that convergence seen in stage 1 continues with larger number of digits, so that we can use the 
            # best answer for a given number of digits d to predict what the leading digits will be for d+1 digits. And so 
            # when looking for the best answer with d+1 digits, we only need to look at a small subset of numbers with 
            # d+1 digits. Based on stage 1, a fairly conservative approach is to assume that all but the last 5 digits in
            # a best answer have completely stabilised. As a result, we can determine the range of numbers to try with d+1
            # digits as follows:
            # - take the best answer found with d digits
            # - set the last five digits of this answer to 0  xxxx00000
            # - add another 0 to end to get the start of the range of numbers to check with d+1 digits xxxx000000
            # - check all the numbers with d+1 digits from xxxx000000 to xxxx999999, i.e. 1 million (10**6) numbers
            # - in fact, as before we only need to check numbers whose last digit is a 9
            #
            unstableDigits = 5
            bestLeadDigits = str(best[1])[:-unstableDigits] # Replace last few digits with 0s
            start = int(bestLeadDigits) * (10 ** (unstableDigits+1)) + 9
            end = start + (10 ** (unstableDigits+1))

        # Reset the best values. NB Do this after calculating the start/end to use, as 
        # for stage 2 we calculate start/end from the best values of the previous loop.        
        best = (-1, 0)

        # Try the different target number values in the range. Can use step 10 as we know the target ends in a 9
        for n in range(start, end, 10) :
            n_s = str(n)
            n_times_9 = n * 9
            n_times_9_s = str(n_times_9)
            n_rotated_s = (n_s[-1] + n_s)[:-1]
            n_rotated = int(n_rotated_s)
            n_diff = abs(n_times_9 - n_rotated)
            if n_diff < best[0] or best[0] == -1 :
                best = (n_diff, n)

        #print("digits = ", digits, "range = ", start, end)

        if best[0] == 0 :
            print()
        print("digits = %2d : best-diff = %2d : best = %s" % (digits, best[0], best[1]))
        if best[0] == 0 :
            print()
            print(f"{best[1]:,d}")  # With comma separators
            print()
            print()
    

# Found the answer, with 44 digits.
#
# digits = 44 : best-diff =  0 : best = 10112359550561797752808988764044943820224719
#
# 10,112,359,550,561,797,752,808,988,764,044,943,820,224,719
# 
# https://en.wikipedia.org/wiki/Parasitic_number 