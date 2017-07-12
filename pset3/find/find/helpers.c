/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
 
bool searchUtil(int value, int values[], int st, int en){
    if(st<=en){
        int mid = st + (en-st)/2;
        if(values[mid] == value)
            return true;
        else if(values[mid]>value)
            return searchUtil(value,values,st,mid-1);
        else 
            return searchUtil(value,values,mid+1,en);
    }
    else
        return false;
}
 
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    return searchUtil(value,values,0,n-1); 
}

/**
 * Sorts array of n values.
 */
 
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    int max = values[0];
    for(int i = 1; i < n; i++){
        if(values[i]>max)
            max = values[i];
    }
    int count[max+1];
    for(int i = 0; i <=max; i++){
        count[i] = 0;
    }
    for(int i = 0; i<n ;i++){
        count[values[i]]++;
    }
    int j = 0;
    for(int i = 0 ; i <= max; i++){
        while(count[i]>0){
            values[j] = i;
            j++;
            count[i]--;
        }
    }
    return;
}
