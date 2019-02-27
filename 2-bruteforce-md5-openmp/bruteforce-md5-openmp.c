//Auteurs : Alexandre GAENG, Jean-Baptiste GAENG

// $ gcc -o bruteforce-md5-openmp bruteforce-md5-openmp.c -fopenmp -lssl -lcrypto
// $ export OMP_NUM_THREADS=4
// $ ./bruteforce-md5-openmp

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include <openssl/sha.h>
#include <openssl/md5.h>
#include <time.h>

typedef unsigned char byte;
#define NB_CHARACTERS 4 // Nombre de caractères du mdp
int NB_ATTEMPTS = 0;

int matches(byte *a, byte* b) {
	for (int i = 0; i < 16; i++)
		if (a[i] != b[i])
			return 0;
	return 1;
}

byte* StringHashToByteArray(const char* s) {
	byte* hash = (byte*) malloc(16);
	char two[3];
	two[2] = 0;
	for (int i = 0; i < 16; i++) {
		two[0] = s[i * 2];
		two[1] = s[i * 2 + 1];
		hash[i] = (byte)strtol(two, 0, 16);
	}
	return hash;
}

void printResult(byte* password, byte* hash) {
	char sPass[NB_CHARACTERS+1];
	memcpy(sPass, password, NB_CHARACTERS);
	sPass[NB_CHARACTERS] = 0;
	printf("%s => ", sPass);
	for (int i = 0; i < MD5_DIGEST_LENGTH; i++)
		printf("%02x", hash[i]);
	printf("\n");
	printf("Nombres de tentatives : %i \n", NB_ATTEMPTS);
}

void computeCombination(int p, byte* password, byte* hashByteArray, int k){

	if(p==2){
		for(password[1] = 33; password[1] < 127; password[1]++){
			byte *hash = MD5(password, k, 0);
			NB_ATTEMPTS = NB_ATTEMPTS + 1;

			if (matches(hashByteArray, hash)){
					printResult(password, hash);

			}
		}
	}

	if(p>2){
		for(password[p-1] = 33; password[p-1] < 127; password[p-1]++){
			computeCombination(p-1, password, hashByteArray, k);
		}
	}

}

int main(int argc, char **argv)
{

#pragma omp parallel
	{

#pragma omp for
		for (int a = 0; a < 94; a++)
		{
			byte password[NB_CHARACTERS] = {33 + a};
			byte* hashByteArray =   StringHashToByteArray("f71dbe52628a3f83a77ab494817525c6"); // Le hash correspond à "toto"
			computeCombination(NB_CHARACTERS,password,hashByteArray,NB_CHARACTERS);
			free(hashByteArray);
	}
}
return 0;
}
