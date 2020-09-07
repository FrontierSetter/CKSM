#include <unistd.h>  
#include <stdio.h>  
// #include <delay.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>

int main (int argc,char *argv[])   
{   

    int page_num = atoi(argv[1]);
    int fork_time = atoi(argv[2]);
    int group_idx = atoi(argv[3]);

    // 4KB * 10240 = 40MB
    int* result = (int*)malloc(1024*page_num*sizeof(int));
    // int* result = mmap(NULL,1024*page_num*sizeof(int),PROT_READ | PROT_WRITE,MAP_ANONYMOUS | MAP_PRIVATE,-1,0);
    int tem;
    int fpid;

    // int rc = madvise(result, 1024*page_num*sizeof(int), MADV_MERGEABLE );


    memset(result, 128, 1024*page_num*sizeof(int));


    // if(rc == -1){
    //     printf("madvise error\n");
    // }

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

    while(true){   
        for(int i = 0; i < 1024*page_num; ++i){
            int tem = result[i];
            // mdelay(2);
        }
    }

    return 0;  
}  