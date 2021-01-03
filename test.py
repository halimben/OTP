

# Transforme text to binary
def textToBin(text):
    b = ''
    b = b.join([(bin( ord(c) )[2:].rjust(8, '0')) for c in text])
    print(len(b))

textToBin('hello')