package main

import "fmt"

func main() {
	i := 0

Here:
	fmt.Println(i)
	i++
	goto Test

Test:
	i = 0
	fmt.Println(i)
	goto Here
}
