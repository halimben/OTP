# importing modules
import os 
from random import randrange
import argparse
import sys
import subprocess
from subprocess import check_output


def generate (parent_dir):
    '''
    Generate files, prefixes, suffixs and pads
            Parameters:
                    parent_dir (directory): the directory which contain pads folders (ex: dir)
            Returns:
                    none
    '''
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
        with open("/dev/urandom", 'rb') as data:
            for x in data.read(2000):
                f_2.write(bin(x)[2:].rjust(8, '0')) 
            for x in data.read(48):
                f_1.write(bin(x)[2:].rjust(8, '0'))
            for x in data.read(48):
                f_3.write(bin(x)[2:].rjust(8, '0'))
            
        f_1.close()
        f_2.close()
        f_3.close()



def check_up_interfaces():
    '''
    check if there is any up interface, if true exception will be raised
            Parameters:
                    none
            Returns:
                    non
    '''
    interfaces = check_output(["ls", "/sys/class/net"]).decode("utf-8")
    interfaces = interfaces.split("\n")

    for interface in interfaces[:-2]:
        print(interface)
        statut = check_output(["cat", "/sys/class/net/{}/operstate".format(interface)]).decode("utf-8")
        statut = statut.split("\n")
        if(statut[0] == 'up'):
            raise Exception('All network interfaces should be down')



def available_pads_in (dir):
    '''
    get the pad available to encode
            Parameters:
                    dir (directory): the directory which contain pads folders
            Returns:
                    p (path): path of pad available to encode
                    prefix (path): path of prefix available to encode
                    suffix (path): path of suffix available to encode
    '''
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
    prefix = os.path.join(ps, str(b).rjust(2, '0')+'p.txt') # first prefix available
    suffix = os.path.join(ps, str(b).rjust(2, '0')+'s.txt') # first suffix available
    return p, prefix, suffix



def send (data, pad_available, prefix_available, suffix_available):
    '''
    create a file named (ex: dir-0000-00t) next to main.py which contain data encrypted
            Parameters:
                    data (str): the message to send
                    pad_available (file): pad available to encode
                    prefix_available (file): prefix available to encode
                    suffix_available (file): suffix available to encode
            Returns:
                    none
    '''
    # read pad prefix and suffix
    f_pad = open(pad_available, "r")
    pad = f_pad.read()
    f_pref = open(prefix_available, "r")
    prefix = f_pref.read()
    f_suff = open(suffix_available, "r")
    suffix = f_suff.read()
    f_pad.close()
    f_pref.close()
    f_suff.close()

    # binary convert then applicate (data XOR pad) 
    bin_data = ''.join((bin( ord(c) )[2:].rjust(8, '0')) for c in data)
    cipher = int(bin_data, 2) ^ int(pad, 2)# binary xor
    cipher = bin(cipher)[2:].zfill(len(pad))

    # Path of the resulat file
    pad_path = pad_available.split(os.sep)
    cipher_path = '' + pad_path[0] + '-' + pad_path[1] + '-' + pad_path[2]
    
    # create the new file (prefix + c + suffix)
    f_ = open(cipher_path.replace('c','t'), "w")
    f_.write(prefix + cipher + suffix)

    # shred the pad used
    #os.remove(pad_available)
    os.system("shred -n 35 -z -u "+pad_available)



def corresponding_pad(cipher_file):
    '''
    Returns the the path of pad corresponding for decodding
            Parameters:
                    cipher_file (file): the encrypted file
            Returns:
                    corresp_pad (path): path of pad corresponding for decodding
    '''
    f = open(cipher_file)
    cipher_prefix = f.read(48*8)
    pads_file_corresponding = os.path.join(cipher_file.split('-')[0], cipher_file.split('-')[1])

    for root, dirs, files in os.walk(pads_file_corresponding):
        for filename in files: # only files
            if filename.endswith("p.txt"): # only prefixe files
                f = open(os.path.join(pads_file_corresponding, filename))
                original_pre = f.read()
                if(original_pre == cipher_prefix): # check the corresponding prefix
                    corresp_pad = os.path.join(pads_file_corresponding, filename).replace('p','c')
                    f.close()
                    break
    return corresp_pad



def recieve(cipher_file, pad_cooresp ):
    '''
    Returns the cleartext message
            Parameters:
                    cipher_file (file): the encrypted file
                    pad_cooresp (path): path of the pad which contain de pas de decrypt
            Returns:
                    clear_text (str): return the message recieved
    '''
    # read pad correspending and cipher text
    f_c = open(cipher_file)
    f_p = open(pad_cooresp)
    c = f_c.read()[48*8 : (2000+48)*8] # obtain only cipher part without prefix and suffix
    p = f_p.read()
    f_c.close()
    f_p.close()

    # Get cleartext message 
    clear_bin = bin(int(c, 2) ^ int(p, 2))[2:] # Binary message
    clear_bin = clear_bin.rjust(len(clear_bin) + (8 - len(clear_bin) % 8), '0') # ajust the binary message to obtain bits 8 by 8
    clear_text = ''.join(chr(int(clear_bin[i*8:i*8+8],2)) for i in range(len(clear_bin)//8)) # binary to string

    return clear_text



################## Main Function ##################
if __name__ == "__main__":
    # if there is up interface => excpetion
    check_up_interfaces()


    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", '--generate', action='store_true', help='mode generte')
    parser.add_argument("-s", '--send', action='store_true', help='mode send ')
    parser.add_argument("-r", '--receive', action='store_true', help='mode receive')
    parser.add_argument("-f", '--file', help='file to send' , required='-r' in sys.argv)
    parser.add_argument("-t", '--text', help='text to send')
    parser.add_argument('dir', help=' directory to store the pads')
    args = parser.parse_args()
    
    if (args.send):
        print('Mode s')
        # send mode
        if args.file:
            data = args.file
            with open(args.file, 'r') as file:
                data = file.read().replace('\n', '')
        elif args.text:
            data = args.text
        else:
            data = input("Enter your text: ")

        if(len(data) > 2000):
            print("Data too long to send !")

        # Get the first pad available path    
        pad_available, prefix_available, suffix_available = available_pads_in (args.dir)
        print('pad available is: ',pad_available)

        # funcition encode (data, pad) (bin then xor)
        send(data, pad_available, prefix_available, suffix_available)
    elif (args.receive):
        print('Mode r')
        pad_cooresp = corresponding_pad(args.file)
        print(recieve(args.file, pad_cooresp))
    else:
        # generate mode
        print('Mode g')
        generate(args.dir)
