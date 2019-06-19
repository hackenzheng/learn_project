// 编译: go build helloworld.go
// 运行: ./helloworld


/*当前文件所属的包名,包名main则告诉我们它是一个可独立运行的包，它在编译后会产生可执行文件。
除了main包之外，其它的包最后都会生成*.a文件（也就是包文件）并放置在$GOPATH/pkg/$GOOS_$GOARCH中
每一个可独立运行的Go程序，必定包含一个package main，在这个main包中必定包含一个入口函数main，而这个函数既没有参数，也没有返回值*/
package main


// 导入包fmt, 包的概念和Python中的package类似，很多用法也类似Python
import "fmt"

func main() {
    //  Go使用UTF-8字符串和标识符(因为UTF-8的发明者也就是Go的发明者之一)，所以天生支持多语言。
    fmt.Printf("Hello, world or 你好，世界 or καλημ ́ρα κóσμ or こんにちはせかい\n")
}