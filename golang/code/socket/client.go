package main

import (
    "fmt"
    "io/ioutil"
    "net"
    "os"
)

func main() {
    if len(os.Args) != 2 {
        fmt.Fprintf(os.Stderr, "Usage: %s host:port ", os.Args[0])
        os.Exit(1)
    }

    service := os.Args[1]
    tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
    fmt.Println(tcpAddr)
    checkError(err)

    fmt.Printf("start to dail tcp\n")
    conn, err := net.DialTCP("tcp", nil, tcpAddr)
    checkError(err)

    fmt.Printf("start to send data\n")
    _, err = conn.Write([]byte("HEAD / HTTP/1.0\r\n\r\n"))
    checkError(err)

    fmt.Printf("start to read data\n")
    result, err := ioutil.ReadAll(conn)
    checkError(err)

    fmt.Println(string(result))
    os.Exit(0)
}

func checkError(err error) {
    if err != nil {
        fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
        os.Exit(1)
    }
}
