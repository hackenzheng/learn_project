//时间回射服务器

package main

import (
    "fmt"
    "net"
    "os"
    "time"
    //"io/ioutil"
)

func handleClient(conn net.Conn) {
    defer conn.Close()
    daytime := time.Now().String()
    conn.Write([]byte(daytime)) // don't care about return value

    result := make([]byte, 128)

    fmt.Println("start to read")
    //result, err := ioutil.ReadAll(conn)
    //fmt.Println(err)
    read_len, err :conn.Read(result)
    fmt.Println(result)
    fmt.Println(err)

}

func checkError(err error) {
    if err != nil {
        fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
        os.Exit(1)
    }
}


func main() {
    service := "127.0.0.1:1200"
    tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
    checkError(err)
    fmt.Println(tcpAddr)


    listener, err := net.ListenTCP("tcp", tcpAddr)
    checkError(err)
    for {
        conn, err := listener.Accept()
        if err != nil {
            continue
        }
        go handleClient(conn)
    }
}

