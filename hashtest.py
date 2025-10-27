import hashlib as hasher

def typechecker(inputs:any,typeneeded:type) -> bool: #takes an any and a type and sees if theyre the same will make validation easier
    if typeneeded == type(inputs):
        return True
    else:
        return False
    
#https://docs.python.org/3/library/hashlib.html
#takes string, encodes as a b'' string, ascii only, hashes it securely with sha256, and outputs it 
def hashtext(inputtext:str) -> str:
    inputtext = inputtext.encode('ascii')
    outputText = hasher.sha256(inputtext)
    outputText = outputText.hexdigest()
    return str(outputText)



#print(hashtext(input()))
if __name__ == '__main__':
    print(typechecker('hello',str))