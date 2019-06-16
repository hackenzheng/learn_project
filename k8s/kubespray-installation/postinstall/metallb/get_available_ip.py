import os
ip = open("ip.txt", "a+")
cnt = 0
for i in range(2,254):
   host = "192.168.2."+str(i)
   resp = os.system("ping -c 1 " + host)
   if resp != 0:
       cnt += 1
       ip.write(host + "\n")
       if cnt == 10:
          ip.write("\n")
          cnt = 0
   else:
       cnt = 0
ip.close()
