// func和defer的使用

package main
import "fmt"

func add_value(input int) int {
    //参数传值
    input += 1
    return input
}

func add_refer(input *int) int{
    //参数传引用
    *input = *input +1
    return *input
}

func multi_return(a , b int) (int, int){
    //返回多个值, 多个返回值需要()
    return a+b, a*b
}

func defer_use(){
    for i:=0; i<5; i++ {
        defer fmt.Printf("%d ", i)
    }
    fmt.Printf("\n")
}

func main(){
    a := 1
    b := add_value(a)
    fmt.Printf("%d\n", a)
    fmt.Printf("%d\n", b)

    c := add_refer(&a)  //得传指针，不然编译不通过
    fmt.Printf("%d\n", a)
    fmt.Printf("%d\n", c)

    sum, product := multi_return(a,b)
    fmt.Printf("%d\n", sum)
    fmt.Printf("%d\n", product)

    defer_use()
}