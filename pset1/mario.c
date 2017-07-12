#include <stdio.h>
#include <cs50.h>

int main(void){
    printf("Height: ");
    int n;
    do{
        n = get_int();
        if(n<0 || n>23){
            printf("Wrong Input. Enter a number in the range of [0,23]\n Height: " );
        }
    }while(n<0 || n>23);
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= n-i; j++){
            printf(" ");
        }
        for(int j = n-i+1; j<=n; j++){
            printf("#");
        }
        for(int j=1; j<=2; j++){
            printf(" ");
        }
        for(int j=1; j<=i; j++){
            printf("#");
        }
        printf("\n");
    }
    return 0;
}