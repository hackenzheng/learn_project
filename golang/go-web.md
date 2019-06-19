## go语言基础

### 包的编译与调用
GOPATH环境变量用于设置本地源码和包路径路径,从go1.8之后不用必须设置,默认是$HOME/go。 GOPATH下分src,pkg,bin三个子目录。
若项目依赖其他package应放在src目录下，若只是单个文件测试任意路径都可以。一般的做法就是一个目录一个项目，
例如: $GOPATH/src/mymath 表示mymath这个应用包或者可执行应用，这个根据package是main还是其他来决定，main的话就是可执行应用，其他的话就是应用包。

当新建应用或者一个代码包时都是在src目录下新建一个文件夹，文件夹名称一般是代码包名称，当然也允许多级目录，例如在src下面新建了
目录$GOPATH/src/github.com/astaxie/beedb 那么这个包路径就是"github.com/astaxie/beedb"，包名称是最后一个目录beedb

编译安装方法有: 1,进入对应的应用包目录，执行go install; 2,在任意的目录执行go install mymath。
安装完之后可以在pkg/linux_amd64对应的目录下看到mymath.a文件。这个mymath.a文件就是应用包，在其他项目的源码中使用 import "mymath"即可调用。
如果mypath.a是子目录下的应用，import时也需要加上路径。

### 获取远程包
对于托管在开源社区如github、googlecode的应用包，go提供了go get工具，比如go get github.com/astaxie/beedb，
go get本质上可以理解为首先第一步是通过源码工具clone代码到src下面，然后执行go install。
在代码中如何使用远程包，很简单的就是和使用本地包一样，只要在开头import相应的路径就可以,import "github.com/astaxie/beedb"

### go命令
go install是安装，如果是xx.go源码里面不是package main，就作为应用包处理，install之后会在pkg目录生成xx.a文件。如果有package main，
则作为应用处理，install之后会在bin目录下生成xx.bin文件，同时也会在当前目录生成bin文件。go install只会到GOPATH/src目录下去找,
不在这个目录的不能被install，只能build生成临时的。

go build 默认会编译目录下所有的go文件，可以指定只编译一个文件。若是普通包，go build不会产生任何文件。如果是main包，会生成一个可执行文件。

go fmt, go强制了代码格式，不按照此格式的代码将不能编译通过，为了减少浪费在排版上的时间，go fmt命令可以帮你格式化代码文件，
开发工具里面一般都带了保存时候自动格式化功能，这个功能其实在底层就是调用了go fmt。

go env查看go设置的环境变量，其中GOROOT是golang 的安装路径，GOPATH可以理解为工作目录

### 变量定义及初始化
var variableName type 最基本的定义形式

const 定义常量，配合iota定义枚举变量

内置基础类型：Boolean，数值(整型和浮点)，字符串，错误类型error。
内置高级类型：引用(*T), array(定义长度), slice(不定义长度,动态数组), map(字典)

go里面的引用与c里面的引用是一个概念，使用方式也一样

make和new都是(堆)内存的分配：new用于各种类型的内存分配，函数原型是func new(Type) *Type,分配零值填充的T类型的内存空间，并且返回
其地址(指针)。make只能创建slice、map和channel，函数原型func make(t Type, size ...IntegerType) Type,返回一个有初始值的T类型，
而不是*T。因为这三种类型就是引用类型，就没有必要返回他们的指针了，同时必须须得初始化，但是不是置为零值。 new不常用，make是不可替代的。

零值并非是空值，而是一种“变量未填充前”的默认值，int类型的零值是0,string类型的零值是""，引用类型的零值是nil

### 函数
应用包中大写开头的函数和变量是公有的，小写开头的是私有的。如果你的函数是导出的(首字母大写)，官方建议：最好命名返回值，因为不命名返回值，
虽然使得代码更加简洁了，但是会造成生成的文档可读性差。

由于 Go 支持 “多值返回”, 而对于“声明而未被调用”的变量, 编译器会报错, 在这种情况下, 可以使用_来丢弃不需要的返回值 例

Go没有像Java那样的异常机制，它不能抛出异常，而是使用了panic和recover机制。一定要记住，你应当把它作为最后的手段来使用，也就是说，你的代码中应当没有，或者很少有panic的东西。

Go里面有两个保留的函数：init函数（能够应用于所有的package）和main函数（只能应用于package main）。这两个函数在定义时不能有任何的参数和返回值。
考虑到可读性和可维护性，强烈建议用户在一个package中每个文件最多写一个init函数，Go程序会自动调用init()和main()。init()可以用于比如数据库连接建立，连接池建立等。

程序的初始化和执行都起始于main包。如果main包还导入了其它的包，那么就会在编译时将它们依次导入。有时一个包会被多个包同时导入，那么它只会被导入一次。
当一个包被导入时，如果该包还导入了其它的包，那么会先将其它包导入进来，然后再对这些包中的包级常量和变量进行初始化，接着执行init函数（如果有的话），依次类推。

import导包

    import fmt  导入标准库，从GOROOT目录下加载
    import "./model"    相对路径加载，从当前文件同一目录的model包，但是不建议这种方式来import
    import "shorturl/model"   绝对路径加载，加载gopath/src/shorturl/model模块
    import . fmt       点操作,这个包导入之后在你调用这个包的函数时，你可以省略前缀的包名，fmt.Println("hello")可以简写成Println("hello")
    import f fmt       别名操作，命令成一个容易记忆的名字
    import  _ "github.com/ziutek/mymysql/godrv"    _操作，引入该包而不直接使用包里面的函数，而是调用包的init函数,比如注册数据库驱动
    
defer,延迟的意思，在普通语句前加defer关键字，表示不会立即执行，当函数执行到最后时，这些defer语句会按照逆序执行，最后该函数返回。
特别是在进行一些打开资源的操作时，遇到错误需要提前返回，在返回前需要关闭相应的资源，不然很容易造成资源泄露等问题，使用defer可减少重复代码，显得更优雅。

函数要作为变量传递给另外一个函数，需要先申明好函数类型 type testfunc func(int, int) bool

Println可以打印出字符串，和变量; Printf只可以打印出格式化的字符串,可以输出字符串类型的变量，不可以输出整形变量和整形。
Fprintf不是写入一个文件，而是写入一个 io.Writer 接口类型的变量.原型是func Fprintf(w io.Writer, format string, a ...interface{}) (n int, err error)。
Fprintf 将参数列表 a 填写到格式字符串format的占位符中并将填写后的结果写入 w 中，返回写入的字节数。

### struct
与c语言的struct一样，用于自定义复合类型。

定义
    
    type person struct {
        name string
        age int
    }
    
声明
    
    var p1 person
    p2:= person{"tom", 25}   按找顺序提供初始化值
    p2:= person{age:24,name:"tom"}   通过field:value方式任务顺序初始化
    p3:= new(person) 
    
    使用
    p1.name = "tom"
    p1.age = 10
    
匿名字段
    
    定义struct的是会后若只提供类型，不写字段名，就是匿名字段也叫嵌入字段。匿名字段实现了字段的继承。
    当匿名字段是一个struct的时候，那么这个struct所拥有的全部字段都被隐式地引入了当前定义的这个struct，访问的时候就跟访问自己字段一样。
    如果匿名struct中的字段和自身的字段重名了，最外层的优先访问，要访问匿名字段就要加上匿名struct名。
    
    
### 面向对象编程
数据绑定方法即对象，在go里面method是函数的另外一种形态，是单独定义，不是在struct里面定义，与定义func类似，只是加了一个receiver。

method可以定义在任何自定义类型、内置类型、struct上面。自定义类型除了struct还有type typeName typeLiteral形式。
类似于C语言的typedef。 当method需要修改对象的数据时，receiver应该指定为指针类型
    
    type Color byte
    
    type Box struct {
    	width, height, depth float64
    	color Color
    }
    
    func (b Box) Volume() float64 {
        return b.width * b.height * b.depth
    }

    func (b *Box) SetColor(c Color) {
    	b.color = c
    }
        
    Volume()定义了接收者为Box，返回Box的容量
    SetColor(c Color)，把Box的颜色改为c
    
如果一个method的receiver是*T,你可以在一个T类型的实例变量V上面调用这个method，而不需要&V去调用这个method
如果一个method的receiver是T，你可以在一个*T类型的变量P上面调用这个method，而不需要 *P去调用这个method，go自动做了转换。

method继承与重写，跟匿名字段的处理方式一样。


### interface
interface类型定义了一组方method，如果某个对象实现了某个接口的所有方法，则此对象就实现了此接口。每个对象定义了多个method，不同对象之间有相同的method的，也有不同的method，
比如Student实现了SayHi、Sing、BorrowMoney；而Employee实现了SayHi、Sing、SpendSalary，都实现了SayHi、Sing，这样就把SayHi、Sing组成一组作为interface。
interface可以被任意的对象实现，同理一个对象可以实现任意多个interface。
   
使用

    type Human struct {
        name string
        age int
        phone string
    }
    
    type Student struct {
        Human //匿名字段
        school string
        loan float32
    }
    type Men interface {
        SayHi()
        Sing(lyrics string)
    }
    
    mike := Student{Human{"Mike", 25, "222-222-XXX"}, "MIT", 0.00}
    var i Men
    i = mike
	i.SayHi()
	
    Men是interface类型，需要使用该类型去定义变量再使用 

interface的变量可以持有任意实现该interface类型的对象,interface的变量可以持有任意实现该interface类型的对象,类似多态。
得到一个interface的变量，可以通过value, ok = element.(T)判断变量具体的对象类型。

### 反射
反射是指一类应用，它们能够自描述和自控制。Golang语言实现了反射，反射机制就是在运行时动态的调用对象的方法和属性，官方自带的reflect包就是反射相关的，
只要包含这个包就可以使用。
   
Go是静态类型语言。每个变量都有且只有一个静态类型，在编译时就已经确定。比如 int、float32、*MyType、[]byte。 如果我们做出如下声明：

    type MyInt int
    
    var i int
    var j MyInt
    
上面的代码中，变量 i 的类型是 int，j 的类型是 MyInt。尽管变量 i 和 j 具有共同的底层类型 int，但它们的静态类型并不一样。不经过类型转换直接相互赋值时，编译器会报错。
   
<Go 语言反射三定律> https://segmentfault.com/a/1190000006190038 是官方文档的翻译 https://blog.golang.org/laws-of-reflection

<Golang的反射reflect深入理解和示例> https://juejin.im/post/5a75a4fb5188257a82110544

### 并发Goroutine
协程无需操作系统支持就能实现并发，因为都在用户态。

go关键词就是创建并开始执行goroutine，用法如下：

    //go 关键字放在方法调用前新建一个 goroutine 并让他执行方法体
    go GetThingDone(param1, param2);
    
    //上例的变种，新建一个匿名方法并执行，返回值在代码体后边
    go func(param1, param2) {
    }(val1, val2) 
    
    //直接新建一个 goroutine 并在 goroutine 中执行代码块
    go {
        //do someting...
    }
    
    golang的goroutine默认情况下使用单核运行，开启多核运行的方法是使用runtime包中的GOMAXPROCS函数设置核心数.
    runtime.GOMAXPROCS(runtime.NumCPU())

channel类似于双向管道,可以通过它发送或者接收值.定义一个channel时，也需要定义发送到channel的值的类型,必须使用make 创建channel.
默认情况下，channel接收和发送数据都是阻塞的即无缓冲，除非另一端已经准备好。无缓冲channel是在多个goroutine之间同步很棒的工具

channel操作：
    
    定义channel
    ci := make(chan int)
    
    channel通过操作符<-来接收和发送数据, <-左边从右边的变量到左边的变量，如果channel变量在左边就是发送，在右边就是读取
    ch <- v    // 发送v到channel ch.
    v := <-ch  // 从ch中接收数据，并赋值给v
    
    close(ci)  //需要显式关闭，避免内存泄露
缓冲channel即创建的时候指定缓冲大小，ch:= make(chan bool, 4)，创建了可以存储4个元素的bool 型channel。在这个channel 中，
前4个元素可以无阻塞的写入。当写入第5个元素时，代码将会阻塞，直到其他goroutine从channel 中读取一些元素，腾出空间。

select:有多个channel时，通过select可以监听channel上的数据流动。select默认是阻塞的，只有当监听的channel中有发送或接收可以进行时才会运行，
当多个channel都准备好的时候，select是随机的选择一个执行的。 select功能类似io复用的select，用法类似switch语句。

   
## go语言web编程
开发web服务器可以使用标准库net/http

Go没有内置的驱动支持数据库，但是定义了database/sql接口，用户可以基于驱动接口开发相应数据库的驱动,只要是按照标准接口开发的代码， 以后需要迁移数据库时，不需要任何修改.
除了标注的database/sql接口也支持orm操作，go没有定义nosql的操作接口。 nosql可以上orm,但一般没必要。
    
    import (
        "database/sql"
        _ "github.com/go-sql-driver/mysql"
        )
    sql.Open("mysql", "root:123456@/test?charset=utf8")
    "database/sql" 就是go定义的标准接口，sql.Open是其中的一个语句，无论是用MySQL，PgSQL还是其他数据库，使用方式都一样，
    都是先sql.Open(),再db.Prepare(),再stmt.Exec(),这样换数据库代码不用变，只要换下驱动即可。 驱动只要加载，不用显式调用。
    
go提供了rpc标准库，分为tcp,http,json三个层次
   
   
## 调试与error处理
Go定义了一个叫做error的类型，来显式表达错误。在使用时，通过把返回的error变量与nil的比较，来判定操作是否成功。

error类型是一个接口类型

    type error interface {
        Error() string
    }

Go在错误处理上采用了与C类似的检查返回值的方式，而不是其他多数主流语言采用的异常方式，这造成了代码编写上的一个很大的缺点:错误处理代码的冗余，
对于这种情况是我们通过复用检测函数来减少类似的代码。

go代码调试可以直接用gdb工具，与调试c代码是一样的。

##单元测试
Go语言中自带有一个轻量级的测试框架testing和自带的go test命令来实现单元测试和性能测试.

对单测文件的要求：文件名必须是_test.go结尾的，这样在执行go test的时候才会执行到相应的代码。
你必须import testing这个包；所有的测试用例函数必须是Test开头。

<go的测试> https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/11.3.md


<build-web-application-with-golang> https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/preface.md
