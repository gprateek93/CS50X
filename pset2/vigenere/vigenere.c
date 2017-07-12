#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <string.h>

int main(int argc,string argv[]){
    if(argc!=2){
        printf("Error:");
        return 1;
    }
    string k = argv[1];
    for(int i = 0; i< strlen(k); i++){
        if(!isalpha(k[i])){
            printf("Error:");
            return 1;
        }
    }
    printf("plaintext: ");
    string p = get_string();
    int size = strlen(p);
    char c[size];
    int j = 0;
    int key;
    for(int i = 0; i<size; i++){
        j = j%strlen(k);
        if(isalpha(p[i])){
            if(isupper(k[j])){
                key = k[j]-'A';
            }
            else{
                key = k[j] - 'a';
             }
            if(isupper(p[i])){
                c[i] = (p[i]-'A'+key)%26 + 'A';
            }
            else{
                c[i] = (p[i]-'a'+key)%26 + 'a';
            }
            j++;
        }
        else{
            c[i] = p[i];
        }
    }
    printf("ciphertext: ");
    for(int i = 0; i<size; i++){
        printf("%c",c[i]);
    }
    printf("\n");
    return 0;
}