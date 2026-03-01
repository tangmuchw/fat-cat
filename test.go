package main

import "fmt"

func main() {
	// var v = 13.12764567
	// fmt.Printf("精度为 2：%.2f \n", v) // 精度为 2：13.12

	// // 通过参数控制
	// var (
	// 	width = 7
	// 	prec  = 2
	// )
	// fmt.Printf("%[1]*.[2]*f", width, prec, v)

	s := "Go语言😀"

	// len(s) 是字节数：12
	fmt.Printf("字节数：%d\n", len(s))

	// 转成 []rune 后统计长度，是实际字符数：5
	runeSlice := []rune(s)
	fmt.Printf("实际字符数：%d\n", len(runeSlice))

	// 取第4个字符（言）
	fmt.Printf("第4个字符：%c\n", runeSlice[3]) // 输出：言
}
