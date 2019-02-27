#!/usr/bin/env python3

#Auteur : Jean-Baptiste Gaeng

from hashlib import md5
from time import time
from string import printable
from itertools import product, count
from binascii import unhexlify

def passwords(encoding):
    """
    Iterateur sur tous les mdp possibles
    """
    chars = [c.encode(encoding) for c in printable]
    for length in count(start=1):
        for pwd in product(chars, repeat=length):
            yield b''.join(pwd)

#Itere sur tous les mdp possibles, et compare son hash apres application

def crack(search_hash, encoding):
    """
    Itere sur tous les mdp possibles, et compare son hash MD5 au hash à cracker
    """
    for pwd in passwords(encoding):
        if md5(pwd).digest() == search_hash:
            return pwd.decode(encoding)

def main():
    encoding = 'ascii'  # utf-8 pour support unicode

    #Ouverture du fichier contenant les hashs à cracker
    #Format des hashs dans le fichier : hexadecimal
    f = open("hashs.txt", "r")
    lines = f.readlines()
    lines = [line.rstrip("\n") for line in lines]
    f.close()

    total_time = 0
    mean_cracked_time = 0

    #Parcourt des hashs
    for hex_password_hash in lines:

        #Conversion des hashs de l'hexadecimal au binaire
        binary_password_hash = unhexlify(hex_password_hash)

        #Crackage
        start = time()
        cracked = crack(binary_password_hash, encoding)
        end = time()
        total_time = total_time + end-start
        print(f"Mot de passe cracké : {cracked}")
        print(f"Temps: {end - start} secondes.")

    mean_cracked_time = total_time / len(lines)
    print(f"Temps total : {total_time}")
    print(f"Temps moyen par mdp cracké : {mean_cracked_time}")

if __name__ == "__main__":
    main()
