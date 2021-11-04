
table=[27, 128, 105, 153, 231, 42, 147, 187, 20, 224, 154, 202, 39, 8, 7, 226, 46, 109, 35, 229, 104, 116, 0, 99, 121, 125, 122, 38, 5, 55, 160, 23, 30, 240, 157, 146, 102, 115, 189, 86, 158, 82, 176, 95, 2, 126, 124, 239, 103, 106, 54, 72, 123, 43, 241, 230, 161, 171, 73, 249, 3, 61, 78, 221, 223, 44, 174, 181, 156, 19, 74, 225, 214, 69, 197, 204, 71, 162, 219, 234, 4, 247, 248, 98, 66, 186, 205, 101, 93, 151, 75, 193, 167, 179, 208, 194, 94, 40, 235, 77, 62, 144, 76, 32, 100, 119, 152, 237, 107, 33, 142, 18, 88, 172, 163, 182, 227, 58, 199, 250, 50, 165, 228, 253, 24, 14, 45, 139, 64, 140, 213, 245, 215, 164, 97, 236, 89, 243, 159, 12, 168, 84, 37, 173, 141, 180, 177, 192, 134, 90, 110, 222, 191, 255, 129, 232, 188, 118, 87, 57, 21, 196, 242, 49, 47, 155, 195, 148, 92, 149, 15, 11, 96, 132, 170, 131, 1, 203, 135, 207, 127, 210, 178, 190, 51, 67, 220, 63, 211, 79, 185, 217, 13, 85, 68, 120, 34, 206, 22, 9, 201, 150, 56, 212, 29, 60, 183, 130, 200, 113, 36, 81, 218, 233, 244, 41, 26, 91, 216, 83, 112, 111, 48, 65, 25, 10, 108, 246, 136, 28, 133, 166, 145, 70, 117, 80, 31, 137, 251, 175, 209, 17, 6, 169, 184, 53, 114, 254, 138, 198, 16, 252, 238, 59, 143, 52]


def hashN(message: str, nBytes: int) -> str:
    """ Return the Pearson Hash of a given message, with the given number of bytes.

    Arguments:

      message -- the sting to be hashed

      nBytes -- the number of bytes the hash should have
    """
    retval=0

    for j in range(nBytes):
        #Change the first byte
        h = table[(ord(message[j]) + j) % 256];
        for i in message[1:]:
             
            h = table[h ^ ord(i)];
        
        retval = ((retval << 8) | h)

    b=retval.to_bytes(2,"big")
    return b

   

def asHex(v):
    """ Return a string containing formatted hex digit pairs (bytes) such as "1C F2".

    Arguments:
      v -- sequence of bytes to be formatted
    """
    return " ".join("{:02x}".format(c) for c in v).upper()


if __name__=="__main__":
    nBytes=2
    tests=["6fxzw","This is a Test", "yes", "no", "maybe", "Chowder for the kitten. Mellow yellow lemon."]
    for i in tests:
        print(f"The {nBytes*8}-bit hash of '{i}' is {asHex(hashN(i,nBytes))}")
    print(asHex(b'P\xcb' ))
