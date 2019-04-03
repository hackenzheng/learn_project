#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/*
 * */

char * GetMemory(int num){
    char *p = (char *)malloc(sizeof(char)*num);
    return p;
}

int main() {
    char *t = GetMemory(10);
    printf("%s", t);
    t[0] = 'a';
    t[1] = 'b';
    t[2] = '\0';
    printf("%s", t);   //正常输出，但没有释放内存

//    char *a;    //这么写会有段错误，因为指针没有指向到内存就赋值，即没有初始化就使用，没有初始化是指向随机的地址
//    *a='h';     // 如果是全局变量，初始化为NULL，然后赋值也会出错
//    printf("%c", *a);

    return 0;
}