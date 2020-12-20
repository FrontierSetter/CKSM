#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char *argv[])
{
	if(argc!=4)
	{
		printf("error args\n");
		return -1;
	}

    int map_length = atoi(argv[2]);
    int wait_time = atoi(argv[3]);
    int tem = 0;

	int fd;
	fd=open(argv[1],O_RDWR);

	if(-1==fd)
	{
		printf("open\n");
		return -1;
	}


	char *pstart;
	pstart=(char*)mmap(NULL,map_length*4096,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);

    if((char*)-1==pstart)
	{
		printf("mmap\n");
		return -1;
	}

    int* buff_anonymous = (int*)malloc(1024*56*sizeof(int));
	memset(buff_anonymous, 128, 1024*56*sizeof(int));


	printf("start\n");

	for(;wait_time > 0; --wait_time){
        for(int i = 0; i < map_length*4096; ++i){
            tem ^= (int)(*(pstart+i));
        }
		printf("middle\n");


		for(int i = 0; i < 1024*56; ++i){
            int tem = buff_anonymous[i];
        }
		printf("round\n");

    }

	printf("finish\n");
    

	int ret=munmap(pstart,map_length*4096);
	if(-1==ret)
	{
		perror("munmap");
		return -1;
	}
	return 0;
}