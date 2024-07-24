package main

import (
	"fmt"
	"sync"
	"time"
)

// multiple channel operation

// func main() {
// 	ch1 := make(chan int)
// 	ch2 := make(chan int)

// 	go func() {
// 		time.Sleep(time.Second)
// 		ch1 <- 1
// 	}()

// 	go func() {
// 		time.Sleep(time.Second * 2)
// 		ch2 <- 2
// 	}()

// 	for i := 0; i < 2; i++ {
// 		select {
// 		case msg1 := <-ch1:
// 			fmt.Println("Recieved", msg1)
// 		case msg2 := <-ch2:
// 			fmt.Println("Recieved", msg2)
// 		}
// 	}
// 	fmt.Println("Finishedd")
// }

// pipeline

func fanIn(ch ...<-chan int) <-chan int {
	out := make(chan int)

	var wg sync.WaitGroup
	output := func(c <-chan int) {
		defer wg.Done()
		for n := range c {
			out <- n
		}
	}

	wg.Add(len(ch))

	for _, c := range ch {
		go output(c)
	}

	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}

func worker(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Printf("worker %d start job %d\n", id, j)
		time.Sleep(time.Second)
		fmt.Printf("worker %d end job %d\n", id, j)
		results <- j * 2
	}

}

// func fib(n int)	int {

// 	if n <= 1 {
// 		return n
// 	}
// 	a, b := 0, 1
// 	for i := 0;
// }

func validParenthesis(s string) bool {
	parenthesis := map[rune]rune{
		'}': '{', ']': '[', ')': '(',
	}
	stack := []rune{}
	for _, c := range s {
		if p, ok := parenthesis[c]; ok {
			if len(stack) > 0 && p == stack[len(stack)-1] {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		} else {
			stack = append(stack, c)
		}

	}

	return len(stack) == 0
}

func main() {

	// ch1 := make(chan int)
	// ch2 := make(chan int)
	// go func() {
	// 	ch1 <- 1
	// 	close(ch1)
	// }()

	// go func() {
	// 	ch2 <- 1
	// 	close(ch2)
	// }()

	// for n := range fanIn(ch1, ch2) {
	// 	fmt.Println(n)
	// }

	jobs := make(chan int, 100)
	results := make(chan int, 100)

	for w := 1; w <= 3; w++ {
		go worker(w, jobs, results)
	}

	for j := 1; j <= 9; j++ {
		jobs <- j
	}
	close(jobs)

	for a := 1; a <= 9; a++ {
		fmt.Println("Result: ", <-results)
	}

	s := Person{name: "shinu", age: 22}
	s.GetName()

	fmt.Println("Valid Parenthesis: ", validParenthesis("(})[]{}"))
	// <-results
}

type Person struct {
	name string
	age  int
}

func (p *Person) GetName() string {
	return p.name
}
