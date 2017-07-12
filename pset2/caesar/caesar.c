#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <string.h>

int main(int argc, string argv[]){
    if(argc!=2){
        printf("Error\n");
        return 1;
    }
    int k = atoi(argv[1]);
    printf("plaintext: ");
    string p = get_string();
    int size = strlen(p);
    char c[size];
    for(int i = 0; i < size; i++){
        if(isalpha(p[i])){
            if(isupper(p[i]))
                c[i] = (p[i]-'A'+k)%26 + 'A';
            else
                c[i] = (p[i]-'a'+k)%26 + 'a';
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