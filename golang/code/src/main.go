/*
自定义包的使用：
目标：将Add(),Multi(),AddMulti()函数封装到包里面供其他模块调用
过程：
方式1.如果类似于c开发将四个文件放在同一个目录下，直接go build main.go会编译失败，Add等函数找不到
方式2.需要将除main.go的其他三个文件作为包先install，三个文件统一为package pkgexample, 并设置export GOPATH=$PWD:$GOPATH,
且目录必须在src子目录下，然后执行go install pkgexample. 此时就能在main.go里面import并使用，使用的时候必须带上包名，即pgkexample.Add()
方式3.跟c语言开发一样，放在同一个目录下,然后go run *.go或者go build *.go或者go build .
*/


package main

import "fmt"
import "pkgexample"

func main() {
    a := 3
    b := 5
    fmt.Println(pkgexample.Add(a,b))
    fmt.Println(pkgexample.Multi(a,b))
    fmt.Println(pkgexample.AddMulti(a,b))
}

