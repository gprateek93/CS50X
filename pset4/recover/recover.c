#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover filename\n");
        return 1;
    }

    // remember filenames
    char *filename = argv[1];

    // open the file 
    FILE *fptr = fopen(filename, "r");
    if (fptr == NULL)
    {
        fprintf(stderr, "Could not open the file %s.\n", filename);
        return 2;
    }
    
    uint8_t block[512];
    int ctr = 0, started = 0;
    int returned = 512;
    FILE *img;
    while(returned == 512)
    {
        returned = fread(&block, sizeof(int8_t), 512, fptr);
        if(block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
            if(started == 1)
            {
                fclose(img);
            }
            started = 1;
            char *jpeg = (char *) malloc(4);
            int n = sprintf(jpeg, "%03d.jpg", ctr);
            if(n < 0)
                fprintf(stderr,"Error while writing\n");
            img = fopen(jpeg, "w");
            if(img == NULL)
            {
                fprintf(stderr, "Could not create the file %s.\n", jpeg);
                return 1;
            }
            free(jpeg);
            ctr++;
        }
        if(started == 1 && returned == 512)
                fwrite(&block, sizeof(int8_t), 512, img);
    }
    fclose(img);
    fclose(fptr);
    return 0;
}