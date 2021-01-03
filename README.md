# OTP
Python tool used to apply a One-Time Pad cipher to a given message.<br />


**1. Steps:**<br />

  Generate pads, prefixes and suffixs.<br />
  Encode the message given with the first pad available, C = Pref + (pad XOR message) + Suff.<br />
  Save the cipher text in file.<br />
  To decode we scan the directory containing the pads for the correct prefix.<br />
  Decode the (pad XOR message) part with the correspending pad.<br />
  
 <br/>

 **2. Execution and options:**
 There is always a directory specified through the positional argument. (ex: dir)
 
<br/>

 - Generate mode:
 
```console
$  python main.py dir -g                              
``` 
or

```console
$  python main.py dir                             
``` 



<br/><br />

- Send mode:

```console 
$  python main.py dir -s -t "your text here"                                       
```
or

```console 
$  python main.py dir -s -f fileToEncrypt.txt                                       
```
or

```console
$  python main.py dir -s                             
```  
      Enter your text:
      hello word_


<br/><br/>

- Recieve mode:

```console 
$  python main.py dir -r -f fileToDecrypt.txt                                       
```
 
 
 
  

