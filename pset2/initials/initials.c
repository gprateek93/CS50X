#include <stdio.h>
#include <ctype.h>
#include <cs50.h>

int main(){
    string p = get_string();
    int i = 1;
    if(p[0]!=' '){
        printf("%c",toupper(p[0]));
    }
    while(p[i]){
        if(p[i-1]==' '&&p[i]!=' '){
            printf("%c",toupper(p[i]));
        }
            i++;
    }
    printf("\n");
    return 0;
}