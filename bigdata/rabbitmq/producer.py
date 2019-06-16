
from py_rabbit import Rabbit_Producer

producer=Rabbit_Producer()
producer.set_exchange()
for i in range(10):
    message="11111111"
    print('send '+message)
    producer.send_message(message)    #

producer.close()