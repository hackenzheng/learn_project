package pkgexample

func AddMulti(a int, b int) int {
    sum := Add(a,b)
    product := Multi(a,b)
    return sum + product
}

