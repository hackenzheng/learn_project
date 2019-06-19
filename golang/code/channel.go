//channel使用

package main

import "fmt"
import "httplib"

func sum(a []int, c chan int, num int) {
    fmt.Println(num)

    total := 0
    for _, v := range a {
        total += v
    }
    c <- total  // send total to c

}


func main() {
    a := []int{7, 2, 8, -9, 4, 0}

    c := make(chan int)
    go sum(a[:len(a)/2], c, 0)
    go sum(a[len(a)/2:], c, 1)    //因为是无缓冲channel，如果两个都不加go就会出现死锁

    fmt.Printf("read to x\n")
    x := <-c   //读取出来的有可能是后半部分的数据，先后顺序是随机的

    fmt.Printf("read to y\n")
    y := <-c  // receive from c

    fmt.Println(x, y, x + y)
}