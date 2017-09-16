#!/usr/bin/python
"""This module is intended for creating symmetric keys, encrypting passwords and providing
a safe mechanism for grabbing credentials when running scripts."""

import cryptography.fernet
import io
import sys
import getpass



def create_key():
    """Creates a symmetric key file."""
    
    keyfile = raw_input('Enter the name of the symmetric key file you wish to create and make sure it ends with .key : ')
    

    ## Generates a bytes string that can be used to encrypt files
    symmetrickey = cryptography.fernet.Fernet.generate_key()
    print "Your symmetric key has been generated..." #, symmetrickey
    f = open(keyfile, 'w')
    f.write(symmetrickey + '\n')
    f.close() 

def encrypt_login(symmetric_key):
    """This function will encrypt your passowrd using the symmetric key provided.  Output is a 
    a file named creds.
    """
    user_password = ""
    encrypted_file = ""
    while user_password == "": 
        user_password = getpass.getpass(prompt='Enter the password to be encrypted: ')
        #encrypted_file = raw_input('Enter the file name to store the password: ')
        if user_password == "":
            print "\nYou didn't enter a password, lets try one more time...."
    with io.open(symmetric_key, 'rb') as k:
        var_symmetric_key = k.read()
        e_symmetrickey = cryptography.fernet.Fernet(var_symmetric_key)
        encrypted_data = e_symmetrickey.encrypt(user_password)
        f = open(symmetric_key, 'a')
        f.write(encrypted_data + '\n')
        f.close() 
        print ("Information has been stored in " + symmetric_key)
        
    # print "Encrypted data:" , str(encrypted_data)
    # print "Decrypted:" , e_symmetrickey.decrypt(encrypted_data)


def decrypt_login(symmetric_key):
    """Expecting a string for the name of the symmetric key."""
    #Read the key file then setup a list.
    f = open(symmetric_key, 'r')
    x = f.readlines()
    #First item in the list is the key, then the encrypted data.
    var_symmetric_key = x[0]
    e_symmetrickey = cryptography.fernet.Fernet(var_symmetric_key)
    #print e_symmetrickey.decrypt(x[1])

    return e_symmetrickey.decrypt(x[1])



def main():
    """
    encrypts, decrypts login information
    """
 
# Start program
if __name__ == "__main__":
   main()