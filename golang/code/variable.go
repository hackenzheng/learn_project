// 变量的声明与使用
//:=这个符号直接取代了var和type,这种形式叫做简短声明,它只能用在函数内部；在函数外部使用则会无法编译通过，所以一般用var方式来定义全局变量。
//:=是声明或者声明的时候初始化，=是赋值

package main
import 'fmt'


//变量声明方式var xxx type
var isActive bool                    // 全局变量声明
var enabled, disabled = true, false  // 忽略类型的声明
func test1() {
    var available bool  // 一般声明
    valid := false      // 简短声明
    available = true    // 赋值操作
    fmt.Printf("%s\n", valid)
}



var frenchHello string       // 声明变量为字符串的一般方法
var emptyString string = ""  // 声明了一个字符串变量，初始化为空字符串
func test2() {
    no, yes, maybe := "no", "yes", "maybe"  // 简短声明，同时声明多个变量
    japaneseHello := "Konichiwa"  // 同上
    frenchHello = "Bonjour"  // 常规赋值
    fmt.Printf("%s\n", valid)
}