/* 
 *  fork_test.c 
 *  version 1 
 *  Created on: 2010-5-29 
 *      Author: wangth 
 */  
#include <unistd.h>  
#include <stdio.h>  
// #include <delay.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>

int main (int argc,char *argv[])   
{   

    int page_num = atoi(argv[1]);
    int wait_time = atoi(argv[2]);
    int round_cnt = atoi(argv[3]);

    // 4KB * 10240 = 40MB
    int* result;
    int tem;
    int fpid;


    for(int j = 0; j < round_cnt; ++j){

        struct timeval tv;
        gettimeofday(&tv, NULL);

        printf("second: %ld\n", tv.tv_sec); // 秒

        // result = (int*)malloc(1024*page_num*sizeof(int));
        result = (int*)mmap(NULL,1024*page_num*sizeof(int),PROT_READ | PROT_WRITE,MAP_ANONYMOUS | MAP_PRIVATE,-1,0);

        int rc = madvise(result, 1024*page_num*sizeof(int), MADV_MERGEABLE );

        if(rc == -1){
            printf("madvise error\n");
        }

        memset(result, 128, 1024*page_num*sizeof(int));

        for(int i = 0; i < 1024*page_num; ++i){
            int tem = result[i];
        }

        sleep(wait_time);

        // free(result);
        munmap(result, 1024*page_num*sizeof(int));

    }

    return 0;  
}  