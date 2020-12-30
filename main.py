# importing os module 
import os 
from random import randrange
import argparse

'''# Parent Directory path 
parent_dir = "Dir"
if not os.path.exists(parent_dir):
    os.makedirs(parent_dir)
  
# sub Directory 1 
i = 0
f = os.path.join('Dir', '0000')
while os.path.exists(f):
    i += 1
    f = os.path.join('Dir', str(i).rjust(4, '0'))    
os.makedirs(f) # create 0000 files

for index in range(0, 100):
    #os.makedirs(os.path.join(f, str(index).rjust(2,'0')))
    name = os.path.join(f, str(index).rjust(2, '0'))
    f1 = name+'p.txt'
    f2 = name+'c.txt'
    f3 = name+'s.txt'
    f_1 = open(f1, "a")
    f_2 = open(f2, "a")
    f_3 = open(f3, "a")
    for n in range(0,48):
        f_1.write(str(randrange(10)))
        f_3.write(str(randrange(10)))
    for n in range(0,2000):
        f_2.write(str(randrange(10)))
    f_1.close()
    f_2.close()
    f_3.close()'''

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
        f1 = name+'p.txt'
        f2 = name+'c.txt'
        f3 = name+'s.txt'
        f_1 = open(f1, "a")
        f_2 = open(f2, "a")
        f_3 = open(f3, "a")
        for n in range(0,48):
            f_1.write(str(randrange(10)))
            f_3.write(str(randrange(10)))
        for n in range(0,2000):
            f_2.write(str(randrange(10)))
        f_1.close()
        f_2.close()
        f_3.close()
################## Main Function ##################
if __name__ == "__main__":
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file', help='image path')
    parser.add_argument("-t", '--text', help='text to encode')
    args = parser.parse_args()
    


    if args.file and args.text:
        file = args.file
        text = args.text
    elif args.file:
        text = input("Enter your text: ") 
        file = args.file
    else:
        file = input("Enter your file(key): ")
        text = args.text 

    # generate pads    
    #generate(file)
    f_2 = open('dir/0000/00c.txt', "r")
    pad = f_2.read()
    if(len(pad) < len(text)):
        print("short key")
exit()
