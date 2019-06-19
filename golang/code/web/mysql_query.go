/*
访问数据库的例子

创建库和表
create database test;
use test;
CREATE TABLE `userinfo` (
`uid` INT(10) NOT NULL AUTO_INCREMENT,
`username` VARCHAR(64) NULL DEFAULT NULL,
`department` VARCHAR(64) NULL DEFAULT NULL,
`created` DATE NULL DEFAULT NULL,
PRIMARY KEY (`uid`)
);

安装驱动  go get github.com/go-sql-driver/mysql

驱动github.com/go-sql-driver/mysql在driver.go/init()通过sql.Register进行注册

import (
"database/sql"
_ "github.com/go-sql-driver/mysql"
)
sql.Open("mysql", "root:123456@/test?charset=utf8")
"database/sql" 就是go定义的标准接口，sql.Open是其中的一个语句，无论是用MySQL，PgSQL还是其他数据库，使用方式都一样，
都是先sql.Open(),再db.Prepare(),再stmt.Exec(),这样换数据库代码不用变，只要换下驱动即可。 驱动只要加载，不用显式调用。
*/

package main

import (
    "database/sql"
    "fmt"
    //"time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:123456@/test?charset=utf8")
    checkErr(err)

    //生成插入数据的sql对象
    stmt, err := db.Prepare("INSERT INTO userinfo SET username=?,department=?,created=?")
    checkErr(err)
    fmt.Println(stmt)

    //执行插入操作
    res, err := stmt.Exec("astaxie", "研发部门", "2012-12-09")
    checkErr(err)

    id, err := res.LastInsertId()
    checkErr(err)
    fmt.Println(id)

    //更新数据
    stmt, err = db.Prepare("update userinfo set username=? where uid=?")
    checkErr(err)

    res, err = stmt.Exec("astaxieupdate", id)
    checkErr(err)

    affect, err := res.RowsAffected()
    checkErr(err)
    fmt.Println(affect)

    //查询数据
    rows, err := db.Query("SELECT * FROM userinfo")
    checkErr(err)

    for rows.Next() {
        var uid int
        var username string
        var department string
        var created string

        // 将结果赋值给变量
        err = rows.Scan(&uid, &username, &department, &created)
        checkErr(err)
        fmt.Println(uid)
        fmt.Println(username)
        fmt.Println(department)
        fmt.Println(created)
    }

    //删除数据
/*
    stmt, err = db.Prepare("delete from userinfo where uid=?")
    checkErr(err)

    res, err = stmt.Exec(id)
    checkErr(err)

    affect, err = res.RowsAffected()
    checkErr(err)

    fmt.Println(affect)
*/
    db.Close()

}

func checkErr(err error) {
    if err != nil {
        panic(err)
    }
}