#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/types.h>
#include <fcntl.h>

#define MAXBUF 1024

/*********************************************************************
* 演示accept返回的socket是阻塞还是非阻塞，如果listenfd是阻塞，返回的就是阻塞，如果listenfd是非阻塞，返回的是非阻塞
* ./server 7838
*********************************************************************/

int main(int argc, char **argv)
{
    int if_block = 1;
    int sockfd, new_fd;
    socklen_t len;
    struct sockaddr_in my_addr, their_addr;

    unsigned int myport, lisnum;
    char buf[MAXBUF + 1];

    fd_set rfds;
    struct timeval tv;

    int retval, maxfd = -1;

    if (argv[1])
        myport = atoi(argv[1]);
    else
        myport = 7838;

    if (argv[2])
        lisnum = atoi(argv[2]);
    else
        lisnum = 2;

    // create an new socket
    if ((sockfd = socket(PF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket");
        exit(1);
    }

    //将侦听socket设置为非阻塞的
    if (if_block)
    {
        int oldSocketFlag = fcntl(sockfd, F_GETFL, 0);
        int newSocketFlag = oldSocketFlag | O_NONBLOCK;
        if (fcntl(sockfd, F_SETFL,  newSocketFlag) == -1)
        {
            close(sockfd);
            printf("set listenfd to nonblock error.");
            return -1;
        }
    }


    //设置地址和端口
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(myport);
    my_addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sockfd, (struct sockaddr *) &my_addr, sizeof(struct sockaddr)) == -1)
    {
        perror("bind");
        exit(1);
    }

    if (listen(sockfd, lisnum) == -1)
    {
        perror("listen");
        exit(1);
    }

    len = sizeof(struct sockaddr);

    if(if_block)
    {
        printf("listenfd is nonblock\n");
        while (true)
        {
            int clientfd = accept(sockfd, (struct sockaddr *) &their_addr, &len);
            if (clientfd != -1)
            {
                printf("%d\n", clientfd);
                int flags;
                flags = fcntl(new_fd, F_GETFL, 0);   //返回的状态竟然不固定，32270和-1
                printf("stat is %d\n", flags);
                if(flags & O_NONBLOCK)
                    printf("non block\n");
                else
                    printf("block\n");
                printf("server: got connection from %s, port %d, socket %d\n", inet_ntoa(their_addr.sin_addr), ntohs(their_addr.sin_port), clientfd);
                close(clientfd);
                close(sockfd);
                return 0;
            }
        }

    }
    else
    {
        printf("listenfd is block\n");
        if ((new_fd = accept(sockfd, (struct sockaddr *) &their_addr, &len)) == -1)
        {
            close(sockfd);
            perror("accept");
            exit(errno);
        }
        else
        {
            int flags;
            flags = fcntl(new_fd, F_GETFL, 0);
            printf("stat is %d\n", flags);
            if(flags & O_NONBLOCK)
                printf("non block\n");
            else
                printf("block\n");

            printf("server: got connection from %s, port %d, socket %d\n", inet_ntoa(their_addr.sin_addr), ntohs(their_addr.sin_port), new_fd);
        }

        close(new_fd);
        close(sockfd);
    }


    return 0;
}