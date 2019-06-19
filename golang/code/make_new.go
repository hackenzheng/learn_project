// make和new的使用以及区别

package main
import "fmt"

func uninit_test(){
    //对引用类型没有初始化就赋值能编译通过，会有运行时错误
    var i *int
    *i = 10
    fmt.Println(*i)  // runtime error: invalid memory address or nil pointer dereference
}

func init_test(){
    //对应用类型先通过new分配内存
    var i *int
    i=new(int)
    *i = 10
    fmt.Println(*i)
}


func main(){
    init_test()
}