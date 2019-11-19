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
#   - using what as learned in the first stage to apply to target numbers with larger numbers of digits, into the range 40-80,
#     but restricting the possibilities being tried to keep processing time reasonable
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
            # Set last 5 digits to 0
            startHead = str(best[1])[:-5] + "00000"
            start = int(startHead) * 10 + 9
            end = start + 10 ** 6

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
    
#
#$ "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python36_64/python.exe" c:/Users/owner/Git/PythonMisc/digits.py
#Breaking at  1119
#p =  3 range =  1009 2018
#[(1009, '9081', '9100', 19), (1019, '9171', '9101', 70)]      
#Breaking at  11119
#p =  4 range =  10009 20018
#[(10109, '90981', '91010', 29), (10119, '91071', '91011', 60)]
#Breaking at  111119
#p =  5 range =  100009 200018
#[(101119, '910071', '910111', 40), (101129, '910161', '910112', 49)]
#Breaking at  1111119
#p =  6 range =  1000009 2000018
#[(1011229, '9101061', '9101122', 61), (1011239, '9101151', '9101123', 28)]
#Breaking at  11111119
#p =  7 range =  10000009 20000018
#[(10112349, '91011141', '91011234', 93), (10112359, '91011231', '91011235', 4), (10112369, '91011321', '91011236', 85)]
#Breaking at  111111119
#p =  8 range =  100000009 200000018
#[(101123589, '910112301', '910112358', 57), (101123599, '910112391', '910112359', 32)]
#Breaking at  1111111119
#p =  9 range =  1000000009 2000000018
#[(1011235949, '9101123541', '9101123594', 53), (1011235959, '9101123631', '9101123595', 36)]
#Breaking at  11111111119
#p =  10 range =  10000000009 20000000018
#[(10112359549, '91011235941', '91011235954', 13), (10112359559, '91011236031', '91011235955', 76)]
#

# Found the answer, with 44 digits.
#p =  43 range =  10112359550561797752808988764044943820000009 10112359550561797752808988764044943821000009
#***** Found a 0 ******
#best =  (0, 10112359550561797752808988764044943820224719)
# https://en.wikipedia.org/wiki/Parasitic_number 