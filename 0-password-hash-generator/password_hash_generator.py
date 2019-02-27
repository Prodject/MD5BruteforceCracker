#!/usr/bin/env python3

#Auteur : Jean-Baptiste Gaeng

import string
import random
import argparse
import hashlib

def password_generator(size=5, charset=string.ascii_letters + string.punctuation + string.digits):
    """
    Générateur de string aléatoires de taille donné dans un domaine de caractère donné (charset)
    """
    return ''.join(random.choice(charset) for _ in range(size))

def main():
    #Parsing des arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-nb", "--nombre_mdp", help="Nombre de mots de passe a generer", type=int, default="5")
    parser.add_argument("-l", "--longueur_mdp", help="Longueur des mots de passe", type=int, default="5")
    parser.add_argument("-ch", "--charset", help="Ensemble des caracteres composant les mots de passe", default = string.ascii_letters + string.punctuation + string.digits)
    args = parser.parse_args()

    encoding = "ascii"
    file = open("passwords.txt","x")
    file2 = open("hashs.txt", "x")

    #Génération des mdps et des hashs MD5 correspondants
    for _ in range (args.nombre_mdp):
        password = password_generator(args.longueur_mdp, args.charset)
        hash = (hashlib.md5(password.encode(encoding))).hexdigest()
        file.write(password + "\n")
        file2.write(hash + "\n")

if __name__ == "__main__":
    main()
