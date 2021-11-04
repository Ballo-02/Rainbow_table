import pearson
import random

defaultCharset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def targetHashFunction(value):
    """ A wrapper around the actual hash function so we can make some measurements about what has been done. """
    nBytes=2
    h=pearson.hashN(value,nBytes)
    try:
        targetHashFunction.counter += 1
        if not h in targetHashFunction.seen:
            targetHashFunction.seen.append(h)
        else:
            targetHashFunction.collisions+=1
    except AttributeError:
        targetHashFunction.counter = 1
        targetHashFunction.seen=[]
        targetHashFunction.collisions=0
    return h


def makeGuess(value, i, minLen,maxLen,charset, debug=False):
    """ Given a value and an index, return a new valid input.

    Arguments:
      value -- a hash value to be turned into a new guess
      i -- the number of steps along the chain we are
      minLen -- minimum length of a new guess
      maxLen -- maximum length of a new guess
      charset -- string containing the valid characters for a guess
      debug -- set to True for copious output, useful for debugging
    """
    
    #Use value as seed, i as offset
    random.seed(value)

    #Move along the pseudo-random sequence by i*maxLen steps
    #Prevents situations where the random length + random selection means i has no impact on output
    for x in range(i*maxLen):
        random.random()

        #Determine a length of the guess
    l=random.randint(minLen,maxLen)
    guess="".join(random.choices(charset, k=l))
    
    if debug: print(f"Making guess from [{value}], with offset {i}, minLen {minLen}, maxLen {maxLen} and charset {charset}: {guess}")

    return guess



def queryTable(hashValue,table, chainLength, hashFunc=targetHashFunction, guessFunc=makeGuess, minLen=3, maxLen=6, charset=defaultCharset, debug=False):
    """find a chain that contains an input value that results in the
    given hash, in the given table.  chainLength limits the search since
    there is no point building test chains longer than the ones in the
    table

    Arguments:
      hashValue -- value being searched
      table -- the table to search
      hashFunc -- the hash function being used. Should accept a string parameter.
      guessFunc -- the function to be used to generate new guesses. Should accept a byte string and an index
      minLen -- minimum length of potential guesses
      maxLen -- maximum length of potential guesses
      charset -- string of valid characters for guesses
      debug -- set to True for lots of debug output

    """
    # Start with the easy case. Is it the end of a chain, and therefore recorded already?
    if hashValue in table:
        if debug: print(f"Found hash in chain at final position, beginning with {table[hashValue]}")
        attempt= rebuildChain(table[hashValue],hashValue,hashFunc,guessFunc,chainLength,minLen,maxLen,charset)
        if attempt!=None:
            return attempt

    #If not, we try recreating chains from each position to see if we find a match.
    for i in range(chainLength-1,-1,-1):
        if debug: print(f"Trying at chain point {i}")
        h=hashValue
        g=None
        out=""
        for j in range(i,chainLength):
            g=guessFunc(h,j-1, minLen=minLen, maxLen=maxLen, charset=charset)
            h=hashFunc(g)
            if debug: out+=f"({g}->{h}) "
        if debug: print(out)
        if h in table:
            if debug: print(f"Found hash in chain at position {i}, beginning with {table[h]}")
            attempt= rebuildChain(table[h],hashValue, hashFunc, guessFunc, chainLength,minLen, maxLen, charset, debug=False)
            if attempt!=None:
                return attempt
    if debug: print("No matches found")
    return None



def rebuildChain(chain,targetHash, hashFunc, guessFunc, chainLength,minLen, maxLen, charset, debug=False):
    """ Recreates a single chain, looking for a target hash.

    Arguments:
      chain -- the starting value for the chain
      targetHash -- the hash we are looking for
      hashFunc -- the hash function being used. Should accept a string parameter.
      guessFunc -- the function to be used to generate new guesses. Should accept a byte string and an index
      minLen -- minimum length of potential guesses
      maxLen -- maximum length of potential guesses
      charset -- string of valid characters for guesses
      debug -- set to True for lots of debug output
    """
    v=chain
    h=hashFunc(v)
    if debug: print(f"Searching for {targetHash} in the chain beginning with {chain}")
    for i in range(chainLength):
        if debug: print(f"Current value is {v} (hash: {h}) at position {i}")
        if hashFunc(v)==targetHash:
            if debug: print(f"Dehashed as {v}")
            return v
        v=guessFunc(h,i,minLen=minLen, maxLen=maxLen, charset=charset)
        h=hashFunc(v)
    if debug: print("Failed to recreate :/")
    return None
        
def generateTable(chainStarts, hashFunc, guessFunc, chainLength, minLen=3,maxLen=6,charset=defaultCharset):
    """ Create a rainbow table for the given hash function

    Arguments:
      chainStarts -- a list of starting values. The length of this list determines how many chains will be constructed.
      hashFunc -- a hash function to be used in the hashing step.
      guessFunc -- a function that can produce valid inputs to the hash function. The function should accept a value and the keyword arguments `minLen` (minimum guess length) `maxLen` (maximum guess length) and `charset` (a string containing all valid characters to be used in the table). These will be passed directly from the arguments of the same names given to this funciton.
      chainLength -- length of each chain
      minLen -- minimum length of values to be hashed
      maxLen -- maximum length of values to be hashed
      charset -- string containing all valid characters for values being hashed
    
"""
    dicttable={}
    for x in range (len(chainStarts)):
        for i in range (chainLength):
            if (i == 0):
                findword=chainStarts[x]
                currentword=chainStarts[x]
            hashedword=hashFunc(currentword)
            currentword=guessFunc(hashedword,(i),minLen,maxLen,charset)
        dicttable[hashedword]= findword
    return dicttable

    #### These lines are here so I can run my own answer. Replace the next two lines with your code
    



if __name__=="__main__":

    rows=3
    columns=3
    starts=[]
    i=0
    while len(starts)<rows:
        g=makeGuess(i,0, minLen=3, maxLen=6, charset=defaultCharset)
        if not g in starts:
            starts.append(g)
        else:
            print("collision on start")
        i+=1


    hf=targetHashFunction 

    
    table=generateTable(starts,hf,makeGuess,columns)

    

    print("-"*20)
    print(table)
    print("-"*20)
    print(f"Generated a total of {targetHashFunction.counter} hashes, reduced to a table of {len(table)} rows. During calculation, {targetHashFunction.collisions} collisions were encountered.")
    
    target= b'\x85r'
    answer=queryTable(target,table,columns, hashFunc=hf)
    print(f"Looking for reversal of {target} and found {answer}")







## Ignore this:

# joiIjmiPg4vcbp6Ius9thojGzWeLhID9e4ufmt0jyoWP3WesmIDNI8qKm8t8maubwGzGzY3GboODosthjZmGgi+HhIDiaoTBg893poiAgmyCjJzdap7E1KQvys3OymqImImTSYuBncsFys3OjmaMzYrLbZ+K1I5riIrT9VLgzc6OL56MjMJq15aTpC/Kzc7IYJjNh45mhM2cz2GNiMbCaoTFjcZug4O92m6YmZ2HJtDnzo4vys3Oji+Di87KaoiYiZQvmKmLzHqN0MyMBcrNzo4vys3O3m6Dn9+TJ4mFj8dhuZmP3HuZtofzI4KMncZJn4ONhmyCjIfAXJ6MnNp8sYSzhybgzc6OL8rNzo5sn5+cy2GevY/Hfdedj8d92+fOji/Kzc6OL4OLzspqiJiJlC+YqYvMeo3G0917mMWN232YiIDaX4uEnIcFys3Oji/Kzc7IYJjNhI5mhM2cz2GNiMbNZ4uEgOJqhIqaxibQ586OL8rNzo4vys3OjmGPlZrpeo+enZNon4id3Umfg42GbJ+fnMthnr2Px32x3LOCZcbNg8dhpoiAk2KDg6LLYcbNg893poiAk2KLlaLLYcbNjcZumJ6L2jKJhY/cfI+Zx6Qvys3Oji/Kzc6OL8qOm9x9j4Oa/m6Dn9OGYY+Vmul6j56dgmeLnoboeoSOxsBqkpmp22qZnseHBcrNzo4vys3Oji/KzYfIL46IjNto0M2c6mqImImFMpmZnIZsn5+cy2GevY/HfcPnzo4vys3Oji+Di87KaoiYiZQvjo+JgG6anYvAa8Kfqsttn4rHpC/Kzc6OL8rNms9thoi1zXqYn4vAe7qMh9xU27Czk3+LhJyfVNqw5I4vys2HyC+OiIzbaNDNntxmhJnGjFOEz8DEYIODxsptjcTHpC/Kzc7cap6YnMAnnoyMwmrD5w==
