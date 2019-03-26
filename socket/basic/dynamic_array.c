#include <stdio.h>
// 参考 https://blog.csdn.net/panhongan_nettery/article/details/48085523
// 测试动态数组占用的空间，动态数组即在结构体的最后，定义的时候可以不初始化长度，参考redis中的sds的实现

struct sdshdr {
    
    // buf 中已占用空间的长度
    int len;

    // buf 中剩余可用空间的长度
    int free;

    // 数据空间
    int buf[1];  //当为0的时候该变量是不占空间的，即使一个指针的空间也不占
};

int main(void)
{
    char tmpbuf[10];
    printf("length %d/n", sizeof(struct sdshdr));
    printf("length %d/n", sizeof(tmpbuf));
	return 0;
}

