# Pearson Rainbow Table Generator

## Pearson Hash Function

The chosen hash function can create hashes of arbitrary length. Here,
we're using just two bytes to limit the size of tables required, but
the same methods would apply for larger hashes. You just need more
time and space.

## What's in the files?

### `src/pearson.py`

Here there are just two functions, and the only one of interest is
`hashN`.

This function, given a string (the argument called `message`) and a
target number of bytes (`nBytes`), creates a hash of that string that
will be exactly `nBytes` long.

You can use `asHex` if you want to turn bytes into nicely printable
hex pairs.

There's also a list of numbers.  This is used to pseudo-randomise
bytes.  The list is 256 items long, so if you take a byte and swap it
for the byte with value N you find in the list at location N, you have
somehting that looks random. By swaping bytes and including an ofset,
the apparent randomisation is increased because the same byte with a
different offset is not replaced with the same new value. [^1]

### `src/rMenu.py`

This is a simple menu system so you can use and test your work.

You're welcome to read it, but I don't recommend looking for good rpactice here. It's nothing more than a way to quickly access the rainbow table generation and querying funcitons.

It also lets you save and load tables, so you can save regenerating them constantly.

### `src/rainbow_generator.py`

This is the key file for the project.

Most of the work is done. The functions provided are:

 - `targetHashFunction(value)` takes a value and returns the hash. It wraps the `hashN` function and adds some counting so we can later see how many times it was called and how many collisions[^2] were encountered.

 - `makeGuess(...)` takes a hash value and creates a new input guess. It uses the pseudorandom number generator to select from the digits we have set as valid. It also limits the length of any guess between a given minimum and maximum.  This is also sometimes called a reduction function.
 
 - `queryTable(...)` will take care of finding out if a hash can be found in one of the chains that make up the table. It needs to be provided with the hash to be hunted, and the table to hunt through. It also needs to know which hash funciton to use, which guess-generating function, minimum and maximum guess length, etc.  This is because it has to recreate the table in pieces and any difference in these parameters will mean deviation from the original table and incorrect results. For information on the format of the table, see below. This function works **in reverse** - it first looks to see if the target hash is at the end of any chain. If not, it tries assuming the target hash is one step away from the end, making a new guess from it, hashing the guess and then seeing if this new has is at the end of any chain. If not, go back another step, and so on.
 
 - `rebuildChain(...)` is used by `queryTable`. This function is used to rebuild a chain to find the hash.  The `queryTable` function can only tell if the hash of the guess produced from the target hash appears in the table. To actually find the guess that created the target hash, you have to start at the beginning of the chain and rebuild.
 
 - `generateTable(...)` is empty, but needs to build the table.  Info below!
 
## Rainbow Table Format

The end-result of generating a table is a dictionary in which each key is a hash from the end of a chain (as a byte string) and each value is the starting message/guess that began the chain.

To create a table of 100 rows (or chains) we need to begin with 100 possible inputs to the hash function. This could be hard-coded, could be drawn from a list of common passwords, or generated from the set of viable characters.

For each of these starting guesses, the target hash function is used to produce a hash. This hash is then turned into a new possible guess. Note that this isn't the reverse of the hash, just some funciton that produces a valid guess.  This is hashed to create another hash, which is used to create another guess, and so on.

When the chain is of the desired length, the final hash is used as a key in the dictionary, with the initial guess as the value.  The chain can always be reproduced from that initial value, and the algorithm for querying rainbow tables can identify which chain is likely to contain a target hash using the final hash in the chain.

In order to prevent chains from landing on identical values and converging (uselessly just repeating a sequence of guesses and hashes that has already been done), the function that makes new guesses has a second parameter. This extra parameter changes as we progress along the chain. At first it is 0, then 1, then 2 and so on. The same has with the same index always gives the same result, but a different has *or* different index will produce a different guess.  Now, we still might find a hash along a chain that has already been seen in another chain, but unless it is in the same position, it won't lead to the same next guess, and so our chain is still useful. If you imagine each index being a different colour, the table would look like a rainbow[^3]. 

## Links

 - https://www.ionos.co.uk/digitalguide/server/security/rainbow-tables/
 - https://en.wikipedia.org/wiki/Rainbow_table

## Footnotes

[^1]: That was a very basic explanation. The Cryptography module will get into this stuff more. Like, ensuring this "confusion", and how this kind of shuffling (effectively an [S-box](https://en.wikipedia.org/wiki/S-box) is used in more cryptosystems.

[^2]: How many times we produce a hash that has already been seen. Each time we have a collision, we are at a point where we add no value to the chain, since we already have a way to reverse this hash. Note that the values that produce the hash might not be the same (what we usually mean by a hash collision) but in a rainbow table, could be produced by accidentally generating the same guess twice in the table.

[^3]: Sort of, if you squint and really want to have a cool name for the algorithm.
