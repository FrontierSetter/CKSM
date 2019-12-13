/* 
 *  fork_test.c 
 *  version 1 
 *  Created on: 2010-5-29 
 *      Author: wangth 
 */  
#include <unistd.h>  
#include <stdio.h>  
#include <delay.h>
#include <stdlib.h>
#include <sys/mman.h>

int main (int argc,char *argv[])   
{   

    int page_num = atoi(argv[1]);
    int wait_time = atoi(argv[2]);
    int fork_time = atoi(argv[3]);
    int group_idx = atoi(argv[4]);

    int* result = (int*)malloc(1024*page_num*sizeof(int));
    int tem;

    for(int i = 0; i < 1024*page_num; ++i){
        result[i] = 65536;
    }

    printf("group %d start\n", group_idx);

    for(int i = 0; i < fork_time; ++i){
        fpid=fork();
        if (fpid < 0)   
            printf("error in fork!");   
        else if (fpid == 0) {  
            printf("\tgroup %d son\n", group_idx);
            break;
        }  
    }

    for(int j < 0; j < wait_time; ++j){   
        for(int i = 0; i < 1024*page_num; ++i){
            int tem = result[i];
            mdelay(2);
        }
    }



    return 0;  
}  