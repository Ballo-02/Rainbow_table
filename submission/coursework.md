# 5062CEM Coursework 1

 - Student ID: 10185533
 
 
## Task 1: Passwords and Hashes (10%)

    If the hashes produced are all 2 bytes, how many possible hash values are there? Explain how you calculate this value.
	
	
The default charset in the table is "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" meaning it involves 62 unique characters. 1 Bytes is 8 digits therefore 2 bytes would be 16 so to work out you need to see how many characters are available (62) then to the power of spaces available (8) which we have 2 (times by 2) creating 62^8x2=4.36680211×10^14 


    With minimum password length of 3 and maximum of 6, and possible characters being all upper and lowercase letters and digits (ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789) how many possible passwords are in our "search space"? Explain how you calculate this value.
	
	
Again there is 62 different character combinations so we can use the same equation but 4 times as the amount of available spaces change each time creating more combinations so all we need to do is add these 4 equations together as shown (62^3)+(62^4)+(62^5)+(62^6)=5.77313831×10^10


    One of these numbers is larger than the other. What implications does this have for security if this hash function is used in storing passwords?  What implications does this have for our rainbow table?

This would simply mean that the smaller value would be easier to crack as their would be less combinations to go through, if the password was brute forced showing less security. This allows the rainbow table to have a better chance of finding these passwords as less combinations are needed to be searched   
	
## Task 2: Implementing the table (30%)

Include your `generateTable` function below. The three back-ticks before and after the code tell Markdown that the text between should be marked-up as code.


``` python

def generateTable(chainStarts, hashFunc, guessFunc, chainLength, minLen=3,maxLen=6,charset=defaultCharset):
    """ Create a rainbow table for the given hash function

    Arguments:
      chainStarts -- a list of starting values. The length of this list determines how many chains will be constructed.
      hashFunc -- a hash function to be used in the hashing step.
      guessFunc -- a function that can produce valid inputs to the hash function. The function should accept a value and the keyword arguments `minLen` (minimum guess length) `maxLen` (maximum guess length) and `charset` (a string containing all valid characters to be used in the table). These will be passed directly from the arguments of the same names given to this function.
      chainLength -- length of each chain
      minLen -- minimum length of values to be hashed
      maxLen -- maximum length of values to be hashed
      charset -- string containing all valid characters for values being hashed
    
"""

	dicttable={}
    for x in range (len(chainStarts)):
        for i in range ((chainLength-1)):
            if (i == 0):
                findword=chainStarts[x]
            hashedword=hashFunc(currentword)
            currentword=guessFunc(hashedword,(i),minLen,maxLen,charset)
        dicttable[hashedword]= findword
    return dicttable

```
 
## Task 3: Parameters (10%)
 
    Discuss how to select the best parameters for generating a rainbow table.

generateTable(chainStarts, hashFunc, guessFunc , chainLength , minLen ,maxLen ,charset)

"chainStarts" allows any list of starting values to be given. Different lengths of chosen words now can be used therefore bigger rainbow tables can be created (or smaller) but will cause the table to generate slower as more calculations are needed. Can also become very handy if a word list is generated based on the target from possible previous reconnaissance. This also changes the size of the table in memory and how long values will take to be searched.

"hashFunc" gives us a hash function we can use to hash our given words. Using this we can create custom hash algorithms to use due to not all passwords using the same such as MD5 and SHA256.

"guessFunc" a function to be passed that creates a guess from the given hash using set parameters such as max/min length and index to reduce collisions. This gives us a chance to use different indexing algorithms as this can effect number of collisions massively. Less collisions also means faster searching 
time and less wasted memory space.

"chainLength" is a way to specify how long we want out chains to be, as this can change how long it takes for the rainbow table to be created and rebuild chains/search for hashes. This also changes how long it'll take when a hash is found as the chain will need to be rebuilt.

"minLen" and "maxLen" gives the guess function parameters to work with as maybe the possible length of the password is known or a certain amount of characters have to be met. This means unnecessary hashes aren’t created and makes the program more efficient for the hash needing to be cracked. THis overall saves memory space and time.
Some hints:

"charset" which is crucial for the function to know which characters are possibly being used in the password as this can change dramatically.

  - You can change the number of chains and the length of each chain
  - What effect does changing each of these have on:
    - How well the table works, as in how many hashes it can break?
    - How long it takes to create?
	- How much space it takes up?
    - How long it takes to search the chains for hashes?
	
	
## Task 4: Reversing Hashes (10%)

    What are possible passwords that produce the following hashes?

 - BA FF = uBg
 - BE 21 = 050
 - 12 34 = 6UvNfx
 - 9A 2E = zAZbpd
 


## Task 5: Improving Guess Generation Efficiency (20%)

    The function that currently produces guesses is not as efficient as it could be.

    Discuss how the time it takes is related to the index argument and propose a solution that makes it independant of this value.


In the code where the function is "makeGuess(value, i, minLen,maxLen,charset, debug=False)" 

1)There is a loop "for x in range(maxLen*i):" which takes in two arguments to make sure there is enough values to be used to randomly select characters in the charset. However, "maxLen*i" portion creates an unnecessary amount of numbers to be used where you can just use the "maxLen" parameter, as this is the maximum characters needed therefore reducing the amount of times the loop is called making the program more efficient.

2)There is a section that generates a seed to allow more accurate random values when indexing (to reduce the number of collisions). This seed command has no parameters sent to it just itself meaning the size by default is a huge number which only a very small portion is needed (decided by the minimum and maximum length). This means an excessive number is generated when it’s not needed making the program inefficient. However, the seed parameters via length can't be changed currently so no example for this second method was produced only concept.


How do you solve this problem? 

Change the arguments passed to the range loop to just "maxLen" as this is only needed

``` python

#Use value as seed, i as offset
    random.seed(value)

    #Move along the pseudo-random sequence by i*maxLen steps
    #Prevents situations where the random length + random selection means i has no impact on output
    for x in range(maxLen):
        random.random()

        #Determine a length of the guess
    l=random.randint(minLen,maxLen)
    guess="".join(random.choices(charset, k=l))
    
    if debug: print(f"Making guess from [{value}], with offset {i}, minLen {minLen}, maxLen {maxLen} and charset {charset}: {guess}")

    return guess
## Challenge: Web service compromise (20%)

```

The docker container `cueh/pears_tree:latest` uses unsalted 2-byte pearson hashes for checking passwords.  See if you can steal the password list and find passwords that result in the hashes.

To run the container: `docker run -it cueh/pears_tree:latest`. The container should tell you which IP and port to use. If it's the only running container, it will probably be: `http://172.17.0.2:80`.

If you're doing it on a chromebook, use this instead: `docker run -p 8000:80 -it cueh/pears_tree:latest` and browse to `http://penguin.linux.test:8000`

You should submit the usernames you found, along with matching
passwords that will work on the site.

I ran a a dirbuster scan using "gobuster dir -u "http://172.17.0.2" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt" that showed me a 
/static page could be found with a 200 code (meaning successfully loaded). I then went onto the browser and searched this in the url which then gave me a file with password and hex hash to be decoded in. I inputted the new hex of each password into the rainbow table with a 1000 length and 1000 chain (estimated values used to crack the found hashes). This gave me decrypted passwords. I then went onto typing into the website the new password with the same hash and the associated username what brought me to a successful login appeared. 
	
	List the hashes you found and passwords that can be used for the found usernames.

Username  :  Hash  :  Decrypted hash
Root      :  5B1B  :  r9X 
Sally     :  FF4A  :  e2gn97
Duncan    :  50CB  :  x8q



