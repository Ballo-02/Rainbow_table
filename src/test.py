import random
minLen=3
maxLen=6
value=b'\x86r'
i=2
charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
random.seed(value)

#Move along the pseudo-random sequence by i*maxLen steps
#Prevents situations where the random length + random selection means i has no impact on output
#for x in range(i*maxLen):
for x in range(maxLen):
    random.random()

#Determine a length of the guess
l=random.randint(minLen,maxLen)
guess="".join(random.choices(charset, k=l))

print(guess)