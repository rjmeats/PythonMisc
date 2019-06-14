# New Scientist puzzle
#
# Lowest score not achievable with three darts, two darts, one dart

def setUpPossibleSingleDartScores() :
    s = set()
    for d in range(0, 20+1) :
        s.add(d)
        s.add(d*2)      # Doubles
        s.add(d*3)      # Trebles
    s.add(25)           
    s.add(50)           # Bullseye
    return list(s)

# Scores which can finish a game - doubles and bulls-eye
def setUpPossibleFinishingDartScores() :
    s = set()
    for d in range(0, 20+1) :
        s.add(d*2)      # Doubles
    s.add(50)           # Bullseye
    return list(s)

def setupList(high) :
    a = []
    for i in range(0, high+1) :
        t = (i, 0, 0)
        a.append(t)

    return a

if __name__ == "__main__" :
    print("hi")

    singleDartScores = setUpPossibleSingleDartScores()
    finishingDartScores = setUpPossibleFinishingDartScores()

    # List of tuples for recording possible 1-dart, 2-dart and 3-dart scores
    # Each tuple has three elements:
    # - score
    # - number of ways of achieving this score
    # - an example way of achieving this score
    # - can this be scored using a finishing dart (double)

    a1 = setupList(60)
    a2 = setupList(120)
    a3 = setupList(180)
    a3Finish = setupList(180)

    for d1 in singleDartScores :
        d1total = d1
        a1[d1total] = (d1total, a1[d1total][1]+1, d1)
        for d2 in singleDartScores :
            d2total = d1 + d2
            a2[d2total] = (d2total, a2[d2total][1]+1, (d1, d2))
            for d3 in singleDartScores :
                d3total = d1 + d2 + d3
                a3[d3total] = (d3total, a3[d3total][1]+1, (d1, d2, d3))
                if d1 in finishingDartScores or d2 in finishingDartScores or d3 in finishingDartScores :
                    a3Finish[d3total] = (d3total, a3Finish[d3total][1]+1, (d1, d2, d3))
        
    #print(singleDartScores)
    print()
    #print(a1)
    for i in range(60+1) :
        cases = a1[i][1]
        if cases == 0 :
            print("*** 1 dart lowest non-gettable score:", i)
            break
    print()
    #print(a2)
    for i in range(60*2+1) :
        cases = a2[i][1]
        if cases == 0 :
            print("*** 2 darts lowest non-gettable score:", i)
            break
    print()
    #print(a3)
    for i in range(60*3+1) :
        cases = a3[i][1]
        if cases == 0 :
            print("*** 3 darts lowest non-gettable score:", i)
            break

    print()
    #print(a3Finish)
    for i in range(60*3+1) :
        cases = a3Finish[i][1]
        if cases == 0 :
            print("*** 3 darts finish lowest non-gettable score:", i)
            break

    # Sort by number of ways of achieving a score, reversed 
    # For single dart case, all have one way, not interesting
    s2 = sorted(a2, key=lambda tup: tup[1], reverse=True)
    #print()
    #print(s2)

    s3 = sorted(a3, key=lambda tup: tup[1], reverse=True)
    #print()
    #print(s3)