#include <iostream>
#include <cstring>
#include <event.h>
#include <event2/thread.h>
#include <unistd.h>

// 使用libevent的方式，但是编译不通过

using namespace std;
#if 0
void on_time(evutil_socket_t fd, short event, void *data) {
    (void) fd;
    (void) event;
    (void) data;

    time_t raw_time = time(NULL);
    cout << "[" << pthread_self() << "]"
         << "定时事件: " << ctime(&raw_time);
}

void *time_thread(void *arg) {
    (void) arg;

    struct event_base *base = event_base_new();
    if (base == NULL) {
        cout << "event base new FAILED" << endl;
        return NULL;
    }

    struct event time_event;
    memset(&time_event, 0, sizeof(time_event));
    event_set(&time_event, -1, EV_PERSIST, on_time, NULL);
    event_base_set(base, &time_event);

    struct timeval tv;
    memset(&tv, 0, sizeof(tv));
    tv.tv_sec = 2;
    tv.tv_usec = 0;
    evtimer_add(&time_event, &tv);

    event_base_dispatch(base);

    event_base_free(base);

    return NULL;
}

#define THREAD_MAX_NUM 2

void create_threads() {
    pthread_t threads[THREAD_MAX_NUM];
    memset(threads, 0, sizeof(threads));

    for (int i = 0; i < THREAD_MAX_NUM; ++i) {
        (void) pthread_create(&threads[i], NULL, time_thread, NULL);
    }

    for (int i = 0; i < THREAD_MAX_NUM; ++i) {
        (void) pthread_join(threads[i], NULL);
    }
}
#endif

void on_read(struct bufferevent *buffer_event, void *ctx) {
    (void) ctx;

    char buffer[128];
    buffer[0] = '\0';
    bufferevent_read(buffer_event, buffer, sizeof(buffer));
    cout << "[" << pthread_self() << "]"
         << "on read  \"" << buffer << "\"" << endl;
}

#define WRITE_STRING "hello world"

void on_write(struct bufferevent *buffer_event, void *ctx) {
    (void) ctx;

    bufferevent_write(buffer_event, WRITE_STRING, sizeof(WRITE_STRING));
    cout << "[" << pthread_self() << "]"
         << "on write " << "\"" << WRITE_STRING << "\"" << endl;
}


void on_error(struct bufferevent *buffer_event, short what, void *ctx) {
    (void) buffer_event;
    (void) what;
    (void) ctx;

    cout << "[" << pthread_self() << "]"
         << "on error " << what << endl;
}

int main() {

    struct event_base *base = event_base_new();
    if (base == NULL) {
        cout << "event base new FAILED" << endl;
        return -1;
    }

    evutil_socket_t socket_pair[2] = {0};
    if (evutil_socketpair(AF_UNIX, SOCK_STREAM, 0, socket_pair) != 0) {
        cout << "evutil_socketpair FAILED" << endl;
        event_base_free(base);
        return -1;
    }
    evutil_socket_t read_socket = socket_pair[0];
    evutil_socket_t write_socket = socket_pair[1];

    evutil_make_listen_socket_reuseable(read_socket);
    evutil_make_listen_socket_reuseable(write_socket);

    struct bufferevent *read_buffer = bufferevent_new(read_socket, on_read, NULL, on_error, NULL);
    if (read_buffer == NULL) {
        cout << "bufferevent_new FAILED" << endl;
        event_base_free(base);
        close(read_socket);
        close(write_socket);
        return -1;
    }

    struct bufferevent *write_buffer = bufferevent_new(write_socket, NULL, on_write, on_error, NULL);
    if (write_buffer == NULL) {
        cout << "bufferevent_new FAILED" << endl;
        event_base_free(base);
        close(read_socket);
        close(write_socket);
        bufferevent_free(read_buffer);
        return -1;
    }

    bufferevent_base_set(base, read_buffer);
    bufferevent_enable(read_buffer, EV_READ | EV_PERSIST);

    bufferevent_base_set(base, write_buffer);
    bufferevent_enable(write_buffer, EV_WRITE | EV_PERSIST);

    event_base_dispatch(base);

    event_base_free(base);
    close(read_socket);
    close(write_socket);
    bufferevent_free(read_buffer);
    bufferevent_free(write_buffer);

    return 0;
}