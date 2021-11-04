
from simple_term_menu import TerminalMenu
import rainbow_generator
import pickle
import sys
from pathlib import Path
import os

class RTState:
    def __init__(self,table=None,chainLength=None,numChains=None):
        self.table=table
        self.chainLength=chainLength
        self.numchains=numChains
    def __str__(self):
        out=""
        if self.table==None:
            out+="Table not generated. "
        else:
            out+="Table ready. "
        if self.chainLength!=None and self.numChains!=None:
            out+=f"Table parameters set to chain length={self.chainLength}, number of chains={self.numChains}"
        else:
            out+="Table parameters are not set"
        return out

    def __repr__(self):
        return f"RTState({self.table},{self.chainLength},{self.numChains})"

    def pickle(self):
        return pickle.dumps(self)
    
def setParams(rts):
    l=None
    n=None
    try:
        l=int(input("Enter length of chains: "))
        if l<=1:
            print("\nChains must be at least length 1\n")
            return
        n=int(input("Enter number of chains: "))
        if n<1:
            print("\nThere must be at least one chain\n")
            return
    except:
        print("\nYou can only enter positive integers for these values\n")
        return
    if rts.chainLength!=l or rts.numChains!=n:
        rts.table=None
    rts.chainLength=l
    rts.numChains=n
def generateTable(rts):
    print("Generating rainbow table")
    if rts.chainLength==None or rts.numChains==None:
        print("\nYou must set the chain length and number of chains, first\n")
        return
    starts=[rainbow_generator.makeGuess(i,0, minLen=3, maxLen=6, charset=rainbow_generator.defaultCharset) for i in range(rts.numChains)]
    print(starts)
    rainbow_generator.targetHashFunction.counter=0
    del(rainbow_generator.targetHashFunction.counter) #Reset counting
    rts.table=rainbow_generator.generateTable(starts,rainbow_generator.targetHashFunction,rainbow_generator.makeGuess,rts.chainLength)
#    print(f"Generated a total of {rainbow_generator.targetHashFunction.counter} hashes, reduced to a table of {len(rts.table)} rows. During calculation, {rainbow_generator.targetHashFunction.collisions} collisions were encountered.")
    print(f"Generated a total of {rainbow_generator.targetHashFunction.counter} hashes, reduced to a table of error rows. During calculation, {rainbow_generator.targetHashFunction.collisions} collisions were encountered.")


def exportTable(rts):
    if rts.table==None:
        print("There is no valid table to export")
        return
    print("Export")
    fn=input("Enter filename: ")
    fnp = Path(fn)
    if fnp.is_file():
        print("File exists.")
        yn=input("Overwrite? (Y/y to overwrite)")
        if yn.strip().upper()!="Y":
            return
    with open(fnp,"wb") as f:
        f.write(rts.pickle())
                 

def importTable(rts):
    print("Import")

    directory="."
    files= [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    tm = TerminalMenu(files) #, preview_command="hexdump -C {}", preview_size=0.25)
    idx = tm.show()
    if idx==None: return
    with open(files[idx], "rb") as f:
        nrts=pickle.loads(f.read())
        rts.table=nrts.table
        rts.chainLength=nrts.chainLength
        rts.numChains=nrts.numChains
        
def searchTable(rts):
    print("Search")

    h=input("Enter two-byte hash as hex (eg FF22): ")
    h=h.strip()

    if len(h)!=4:
        print("Only enter 4 characters, representing two hex bytes. e.g. AB12")
        return
    try:
        bytes=int(h,base=16).to_bytes(2,"big")
        print(f"Hash of {bytes} accepted")
        result=rainbow_generator.queryTable(bytes,rts.table,rts.chainLength, hashFunc=rainbow_generator.targetHashFunction)
        if result!=None:
            print(f"The potential input found to produce that hash is: {result}")
        else:
            print("Unfortunately no potential input was found to produce that hash")
                
    except:
         print("Invalid hex")

def quit(rts):
    print("Quitting")
    sys.exit(0)
    
if __name__ == "__main__":
    
    rts=RTState()

    options = [("[p] Set Table Parameters",setParams),("[g] Generate Rainbow Table",generateTable), ("[e] Export Rainbow Table",exportTable), ("[i] Import Rainbow Table",importTable), ("[s] Search Rainbow Table",searchTable),("[q] Quit",quit)]

    tm = TerminalMenu([i[0] for i in options])

    while True:
        print()
        print(rts)
        print()
        menuIndex = tm.show()
        if menuIndex!=None:
            options[menuIndex][1](rts)

