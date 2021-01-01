# importing os module 
import os 
from random import randrange
import argparse


def generate (parent_dir):
    # Parent Directory path 
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    
    # sub Directory 1 
    i = 0
    f = os.path.join(parent_dir, '0000')
    while os.path.exists(f):
        i += 1
        f = os.path.join(parent_dir, str(i).rjust(4, '0'))    
    os.makedirs(f) # create 0000 files

    for index in range(0, 100):
        #os.makedirs(os.path.join(f, str(index).rjust(2,'0')))
        name = os.path.join(f, str(index).rjust(2, '0'))
        f1, f2, f3 = name+'p.txt', name+'c.txt', name+'s.txt'
        
        f_1 = open(f1, "a")
        f_2 = open(f2, "a")
        f_3 = open(f3, "a")
        for n in range(0,48):
            f_1.write(bin(randrange(255))[2:].rjust(8, '0'))
            f_3.write(bin(randrange(255))[2:].rjust(8, '0'))
        for n in range(0,2000):   
            f_2.write(bin(randrange(255))[2:].rjust(8, '0'))
        f_1.close()
        f_2.close()
        f_3.close()
    return parent_dir, f


def available_pads_in (dir):
    ps = os.path.join(dir, '0000')
    a = 0
    b= 0
    while not os.path.exists(ps):
        a += 1
        ps = os.path.join(dir, str(a).rjust(4, '0'))
    p = os.path.join(ps, '00c.txt') # first pads file available    
    while not os.path.exists(p): 
        b += 1
        p = os.path.join(ps, str(b).rjust(2, '0')+'c.txt') # first pad available
    prefix = os.path.join(ps, str(b).rjust(2, '0')+'p.txt') # first pad available
    suffix = os.path.join(ps, str(b).rjust(2, '0')+'s.txt') # first pad available
    return p, prefix, suffix

def send (data, pad_available, prefix_available, suffix_available):
    # read pad prefix and suffix
    f_pad = open(pad_available, "r")
    pad = f_pad.read()
    f_pref = open(prefix_available, "r")
    prefix = f_pref.read()
    f_suff = open(suffix_available, "r")
    suffix = f_suff.read()

    # binary convert then applicate (data XOR pad) 
    bin_data = ''.join((bin( ord(c) )[2:].rjust(8, '0')) for c in data)
    print('- ',pad)
    print('- ',bin_data)
    cipher = '{0:b}'.format(int(bin_data, 2) ^ int(pad, 2)) # binary xor

    # Path of the resulat file
    pad_path = pad_available.split(os.sep)
    cipher_path = '' + pad_path[0] + '-' + pad_path[1] + '-' + pad_path[2]
    
    # create the new file (prefix + c + suffix)
    f_ = open(cipher_path, "w")
    f_.write(prefix + cipher +suffix)


################## Main Function ##################
if __name__ == "__main__":
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", '--generate', action='store_true', help='mode generte')
    parser.add_argument("-s", '--send', action='store_true', help='mode send ')
    parser.add_argument("-r", '--receive', action='store_true', help='mode receive')
    parser.add_argument("-f", '--file', help='file to send')
    parser.add_argument("-t", '--text', help='text to send')
    parser.add_argument('dir', help=' directory to store the pads')
    args = parser.parse_args()
    
    if (args.send):
        print('mode s')
    elif (args.receive):
        print('mode r')
    else:
        print('mode g')
        parent_dir, subfolder = generate(args.dir)
        print(subfolder)

    


    # sent mode
    if args.file:
        data = args.file
        with open(args.file, 'r') as file:
            data = file.read().replace('\n', '')
        # sent(data)
    elif args.text:
        data = args.text
        # sent(data) 
    else:
        data = input("Enter your text: ")
        # sent(data) 
    if(len(data) > 2000):
        print("Data too long to send !")

    # Get the first pad available path    
    pad_available, prefix_available, suffix_available = available_pads_in (args.dir)
    print('pad available is: ',pad_available)

    # funcition encode (data, pad) (bin then xor)
    send(data, pad_available, prefix_available, suffix_available)