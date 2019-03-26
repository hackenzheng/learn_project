//这里使用自己的日志系统，当然也可以使用SYSLOG。
#include <stdio.h>
#define LOGBUFSZ 256     /*log buffer size*/
#define LOGFILE  "/var/log/wsiod.log"  /*log filename*/
int wsio_logit(char * func, char *msg, ...)
{
        va_list args;
        char prtbuf[LOGBUFSZ];
        int save_errno;
        struct tm *tm;
        time_t current_time;
        int fd_log;
 
        save_errno = errno;
        va_start (args, msg);
        (void) time (¤t_time);            /* Get current time */
        tm = localtime (¤t_time);
        sprintf (prtbuf, "%02d/%02d %02d:%02d:%02d %s ", tm->tm_mon+1,
                    tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec, func);
        vsprintf (prtbuf+strlen(prtbuf), msg, args);
        va_end (args);
        fd_log = open (LOGFILE, O_WRONLY | O_CREAT | O_APPEND, 0664);
        write (fd_log, prtbuf, strlen(prtbuf));
        close (fd_log);
        errno = save_errno;
        return 0;
}
 
int init_daemon(void)
{
  pid_t pid;
  int i;
 
  /* parent exits , child continues */
  if((pid = fork()) < 0)
    return -1;
  else if(pid != 0)
    exit(0);
 
  setsid(); /* become session leader */
 
  for(i=0;i<= 2;++i) /* close STDOUT, STDIN, STDERR, */
    close(i);
 
  umask(0); /* clear file mode creation mask */
  return 0;
}
 
void sig_term(int signo)
{
  if(signo == SIGTERM)  /* catched signal sent by kill(1) command */
  {
     wsio_logit("", "wsiod stopped/n");
     exit(0);
　}
}
 
/* main program of daemon */
int main(void)
{
if(init_daemon() == -1){
printf("can't fork self/n");
exit(0);
  }
  wsio_logit("", "wsiod started/n");
  signal(SIGTERM, sig_term); /* arrange to catch the signal */
 
  while (1) {
    // Do what you want here
    … …
  }
  exit(0);
}
