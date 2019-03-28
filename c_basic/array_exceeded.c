#include <stdio.h>
#include <string.h>
/*
 * 数组越界访问的测试，定义固定长度的数组，若访问长度之外的单位也是可以的，不会报错，但有限制范围。
 * 通过gdb调试，超过一定范围后会提示超出范围了。
 * c语言直接操作内存的好处带来了高效性，但是也容易出访问越界的bug
 * */



int main() {
    int c[4] = {0, 1, 2, 3};
    printf("size of c is %d\n", (int)sizeof(c));
    for(int i=0;i< 10; i++){
        // 即使越界也能访问而且能赋值
        printf("c[%d] is %d\n", i, c[i]);
        c[i] = i;
        printf("after assigned, c[%d] is %d\n", i, c[i]);
    }

    //sizeof是计算内存的占用空间，不会以\0为边界， strlen是计算字符串的长度
    char d[] = "abcdef";
    printf("size of d is %d\n", (int)sizeof(d));
    printf("strlen of d is %d\n", (int)strlen(d));
    d[3] = '\0';
    printf("new d is %s\n", d);   //输出的时候也会以\0分割
    printf("new size of d is %d\n", (int)sizeof(d));
    printf("new strlen of d is %d\n", (int)strlen(d));

    return 0;
}