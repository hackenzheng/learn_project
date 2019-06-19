// 变量的声明与使用
//:=是简短声明,它只能用在函数内部,无需var和type关键词；在函数外部使用则会无法编译通过，所以一般用var方式来定义全局变量。
//:=是声明或者声明的时候初始化，=是赋值

package main
import "fmt"


//变量声明方式var xxx type
var frenchHello string       // 全局变量声明
var emptyString = "hello"  //  忽略类型的声明并初始化
func test() {
    no, yes := "no", "yes"  // 简短声明，同时声明多个变量
    japaneseHello := "Konichiwa"  // 简短声明
    frenchHello = "Bonjour"       // 常规赋值
    fmt.Printf("%s\n", frenchHello)
    fmt.Printf("%s\n", emptyString)
    fmt.Printf("%s\n", japaneseHello)
    fmt.Printf("%s\n", no)
    fmt.Printf("%s\n", yes)
}

const(
    WHITE = iota
    BLACK
    BLUE
    RED
    YELLOW
)

func main() {
    test()
    fmt.Printf("%d\n", WHITE)
    fmt.Printf("%d\n", YELLOW)
}
