#include <stdio.h>
#include <string.h>
/*
 * */



int main() {
    union {
        int a;
        float b;
        char c;
    } ut;
    ut.a = 25;
    ut.b = 3.14;
    ut.c = 'x';
    printf("size of union is %d\n", sizeof(ut));
    printf("size of 0 is %d\n", sizeof(0));
    printf("%d %f %c\n", ut.a, ut.b, ut.c);  // 只有ut.c的值是正确的，其他两个有输出，但是数值不对
    return 0;
}