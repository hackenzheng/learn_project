//goroutine的实现

package main

import (
    "fmt"
    "runtime"
)

func say(s string) {
    for i := 0; i < 5; i++ {
        runtime.Gosched()
        fmt.Println(s)
    }
}

func main() {
    go say("world") //开一个新的Goroutines执行， 如果这行放在下面，只会输出hello，也是因为主goroutine直接退出了
    say("hello") //当前Goroutines执行，如果这里也有go关键词，将不会有任何输出，因为主goroutine是空的，直接退出

}