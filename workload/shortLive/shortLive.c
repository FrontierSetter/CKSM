#include <unistd.h>  
#include <stdio.h>  
// #include <delay.h>
#include <stdlib.h>
#include <sys/mman.h>

int main (int argc,char *argv[])   
{   

    int page_num = atoi(argv[1]);
    int wait_time = atoi(argv[2]);
    int round_max = atoi(argv[3]);

    int tem;
    int* result;

    for(;round_max > 0; --round_max){

        // 4KB * 10240 = 40MB
        result = (int*)malloc(1024*page_num*sizeof(int));

        memset(result, 128, 1024*page_num*sizeof(int));

        // for(int i = 0; i < 1024*page_num; ++i){
        //     result[i] = 65536;
        // }

        for(int j = 0; j < wait_time; ++j){   
            for(int i = 0; i < 1024*page_num; ++i){
                int tem = result[i];
                // mdelay(2);
            }
        }

    }



    return 0;  
}  