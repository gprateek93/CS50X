#include <stdio.h>
#include <cs50.h>

int main(void){
    printf("minutes: ");
    int minutes = get_int();
    if(minutes==-1)
        printf("Wrong Input");
    int bottles = 12*minutes;
    printf("bottles: %d",bottles);
    return 0;
}