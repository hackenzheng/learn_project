//
// Created by zhg on 19-3-28.
// 反转单链表的操作
//



#include <stdio.h>
#include <stdlib.h>

typedef struct listNode{
    int val;
    struct listNode * next;
}listNode;

listNode * reverseList(listNode * head)
{
    if(head == NULL || head->next == NULL)
        return head;
    listNode * newHead=NULL;   //直接newHead->next会出段错误
    listNode * p=head->next;

    // 假定newhead是已经反转部分的头节点，那么从这个位置开始的操作只要四部，然后就是链表的初始化。
    while(head->next)      //单个节点就不适用
    {
        head->next = newHead;
        newHead = head;
        head = p;
        p=p->next;

    }
    return newHead;
}

void listPrint(listNode * head)
{
    while(head != NULL)
    {
        printf("%d\n",head->val);
        head = head->next;
    }
}

listNode * initList(int arr[], int len)
{

    listNode * head = malloc(sizeof(listNode));
    head->val = arr[0];
    head->next = NULL;
    listNode * tmpHead = head;
    for(int i=1; i<len; i++)
    {
        listNode * tmp = malloc(sizeof(listNode));
        tmp->val = arr[i];
        tmpHead->next = tmp;
        tmpHead = tmpHead->next;
    }
    return head;

}

int main()
{
    printf("the first sample: multi items\n");
    int arr[10] = {1, 2 , 3, 4, 5, 7, 8, 9, 10};
    listNode * p = initList(arr, 10);
    listPrint(reverseList(p));
    free(p);
    p = NULL;

    printf("the second sample: one item\n");
    int arr2[1] = {1};
    p = initList(arr2, 1);
    listPrint(reverseList(p));
    free(p);
    p = NULL;

    printf("the third sample: null list\n");
    listPrint(reverseList(p));
}