#include <stdio.h>
#include <cs50.h>
#include <math.h>

int countDig(long long n){
    int dig = 0;
    while(n){
        dig++;
        n/=10;
    }
    return dig;
}

bool checksum(long long n){
    int counte = 0, counto = 0;
    int i = 1;
    while(n){
        int p = n%10;
        if(i%2==0){
            int q = p*2;
            while(q){
                counte+=q%10;
                q=q/10;
            }
        }
        else 
            counto +=p;
        n/=10;
        i++;
        
    }
    int tot = counte + counto;
    if(tot%10==0)
        return true;
    else
        return false;
}

int checkType(long long n, int dig){
    int f = n/pow(10,dig-1);
    int s = n/pow(10,dig-2);
    if(dig == 15 && (s == 34 || s == 37))
        return 1;
    else if(dig == 16 && s>=51 && s<=55)
        return 2;
    else if((dig == 13 || dig == 16) && f == 4)
        return 3;
    else
        return -1;
}

int main(void){
    long long n;
    printf("Number: ");
    n = get_long_long();
    int dig = countDig(n);
    if(checksum(n)){
        int a = checkType(n,dig);
        if(a==1)
            printf("AMEX\n");
        else if(a==2)
            printf("MASTERCARD\n");
        else if(a==3)
            printf("VISA\n");
        else
            printf("INVALID\n");
    }
    else{
        printf("INVALID\n");
    }
    return 0;
}