//
// Created by zhg on 19-3-28.
// 倒数第k个节点
//

#include <stdio.h>
#include <stdlib.h>

typedef struct listNode{
    int val;
    struct listNode * next;
}listNode;

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

// 最后一个为倒数第1个
listNode * kthNode(listNode * head, int k)
{
    if(head==NULL || k<1)
        return NULL;

    listNode *fast=head;
    listNode *slow=head;
    // 正常的情况，结束后fast要走k-1步，用for直接一些
    while(k>0 && fast->next)
    {
        fast = fast->next;
        k--;
    }


    if(k > 1 || fast == NULL)
        return NULL;

    while(fast->next)
    {
        fast = fast->next;
        slow = slow->next;
    }

    return slow;

}


int main()
{
    printf("the first sample: multi items\n");
    int arr[10] = {1, 2 , 3, 4, 5, 7, 8, 9, 10};
    listNode * p = initList(arr, 10);
    listNode * q = kthNode(p, 6);
    if(q==NULL)
        printf("return is null\n");
    else
        printf("%d", q->val);
    free(p);
    p = NULL;

}