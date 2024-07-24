// // // package main

// // // import (
// // // 	"bytes"
// // // 	"fmt"
// // // 	"io"
// // // 	"log"
// // // 	"math"
// // // 	"os"
// // // 	"regexp"
// // // 	"sort"
// // // 	"strconv"
// // // 	"strings"
// // // 	"sync"
// // // )

// // // func firstExercise(seq string) string {
// // // 	const C int = 50
// // // 	const H int = 30
// // // 	var result string
// // // 	splitted := strings.Split(seq, ",")
// // // 	for j, i := range splitted {
// // // 		D, err := strconv.Atoi(strings.TrimSpace(i))
// // // 		if err != nil {
// // // 			fmt.Println(err, "err")
// // // 			return ""
// // // 		}
// // // 		op := (2 * C * D) / H
// // // 		sqrt := math.Sqrt(float64(op))
// // // 		result += strconv.Itoa(int(sqrt))
// // // 		if j != len(splitted)-1 {
// // // 			result += ", "
// // // 		}
// // // 	}
// // // 	return result
// // // }

// // // func secondExercise(x, y int) [][]int {
// // // 	var result [][]int
// // // 	for i := 0; i < x; i++ {
// // // 		var arr []int
// // // 		for j := 0; j < y; j++ {
// // // 			arr = append(arr, i*j)
// // // 		}
// // // 		result = append(result, arr)
// // // 	}
// // // 	return result
// // // }

// // // func thirdExercise(seq string) string {
// // // 	words := []string{}
// // // 	for _, i := range strings.Split(seq, ",") {
// // // 		words = append(words, strings.TrimSpace(i))
// // // 	}
// // // 	sort.Strings(words)
// // // 	newSeq := strings.Join(words, ",")
// // // 	return newSeq
// // // }

// // // func fourthExercise(lines string) string {
// // // 	return strings.ToUpper(lines)
// // // }

// // // func fifthExercise(seq string) string {
// // // 	words := strings.Split(seq, " ")
// // // 	var newArr []string
// // // 	contains := func(word string) bool {
// // // 		for _, j := range newArr {
// // // 			if j == word {
// // // 				return true
// // // 			}
// // // 		}
// // // 		return false
// // // 	}
// // // 	for _, i := range words {
// // // 		if contains(i) {
// // // 			continue
// // // 		} else {
// // // 			newArr = append(newArr, i)
// // // 		}
// // // 	}
// // // 	sort.Strings(newArr)
// // // 	joined := strings.Join(newArr, " ")
// // // 	return joined
// // // }

// // // func sixthExercise(binSeq string) string {
// // // 	seqArr := strings.Split(binSeq, ",")
// // // 	var output string
// // // 	for _, bin := range seqArr {
// // // 		binNum, err := strconv.ParseInt(bin, 2, 64)
// // // 		if err != nil {
// // // 			return ""
// // // 		}
// // // 		if binNum%5 == 0 {
// // // 			if output != "" {
// // // 				output += ","
// // // 			}
// // // 			output += bin
// // // 		}
// // // 	}
// // // 	return output
// // // }

// // // func seventhExercise() string {
// // // 	var output string
// // // 	for i := 100; i < 301; i++ {
// // // 		converted := strconv.Itoa(i)
// // // 		first, _ := strconv.Atoi(string(converted[0]))
// // // 		second, _ := strconv.Atoi(string(converted[1]))
// // // 		third, _ := strconv.Atoi(string(converted[2]))
// // // 		if first%2 == 0 && second%2 == 0 && third%2 == 0 {
// // // 			if output != "" {
// // // 				output += ","
// // // 			}
// // // 			output += converted
// // // 		}
// // // 	}
// // // 	return output
// // // }

// // // func eighthExercise(sentence string) {
// // // 	var letters int
// // // 	var digits int
// // // 	re := regexp.MustCompile("[^a-zA-Z0-9]+")
// // // 	converted := strings.Split(re.ReplaceAllString(sentence, ""), "")
// // // 	for _, i := range converted {
// // // 		if _, err := strconv.Atoi(i); err == nil {
// // // 			digits += 1
// // // 		} else {
// // // 			letters += 1
// // // 		}
// // // 	}
// // // 	fmt.Println("LETTERS: ", letters)
// // // 	fmt.Println("DIGITS: ", digits)
// // // }

// // // func twelthExercise() {
// // // 	m := map[int]bool{1: true, 2: false, 3: false}
// // // 	delete(m, 2)
// // // 	for k, v := range m {
// // // 		fmt.Println(k, v)
// // // 	}
// // // }

// // // func thirteenExercise() {
// // // 	f, err := os.Create("info.txt")
// // // 	if err != nil {
// // // 		log.Fatal("err1: ", err)
// // // 	}
// // // 	defer f.Close()
// // // 	_, err2 := f.WriteString("The Go gopher is an iconic mascot!")
// // // 	if err2 != nil {
// // // 		log.Fatal("err2: ", err2)
// // // 	}
// // // }

// // // func SwapValues() {
// // // 	x, y := 5.5, 8.8
// // // 	ptrx, ptry := &x, &y
// // // 	x, y = *ptry, *ptrx
// // // 	fmt.Println(x, y)
// // // }

// // // type Vehicle interface {
// // // 	License() string
// // // 	Name() string
// // // }

// // // type Car struct {
// // // 	licenseNo string
// // // 	brand     string
// // // }

// // // func (c *Car) License() string {
// // // 	return c.licenseNo
// // // }

// // // func (c *Car) Name() string {
// // // 	return c.brand
// // // }

// // // type Writer interface {
// // // 	Write([]byte) (int, error)
// // // }

// // // type Closer interface {
// // // 	Close() error
// // // }

// // // type WriterCloser interface {
// // // 	Writer
// // // 	Closer
// // // }

// // // type BufferedWriterCloser struct {
// // // 	buffer *bytes.Buffer
// // // }

// // // func (bwc *BufferedWriterCloser) Write(data []byte) (int, error) {
// // // 	n, err := bwc.buffer.Write(data)
// // // 	if err != nil {
// // // 		return 0, err
// // // 	}
// // // 	v := make([]byte, 8)
// // // 	for bwc.buffer.Len() > 8 {
// // // 		_, err := bwc.buffer.Read(v)
// // // 		if err != nil {
// // // 			return 0, err
// // // 		}
// // // 		_, err = fmt.Println(string(v))
// // // 		if err != nil {
// // // 			return 0, err
// // // 		}
// // // 	}
// // // 	return n, nil
// // // }

// // // func (bwc *BufferedWriterCloser) Close() error {
// // // 	for bwc.buffer.Len() > 0 {
// // // 		data := bwc.buffer.Next(8)
// // // 		_, err := fmt.Println(string(data))
// // // 		if err != nil {
// // // 			return err
// // // 		}
// // // 	}
// // // 	return nil
// // // }

// // // func NewBufferedWriterCloser() *BufferedWriterCloser {
// // // 	return &BufferedWriterCloser{
// // // 		buffer: bytes.NewBuffer([]byte{}),
// // // 	}
// // // }

// // // func deposit(b *int, n int, wg *sync.WaitGroup, m *sync.Mutex) {
// // // 	m.Lock()
// // // 	*b += n
// // // 	m.Unlock()
// // // 	wg.Done()
// // // }

// // // func withdraw(b *int, n int, wg *sync.WaitGroup, m *sync.Mutex) {
// // // 	m.Lock()
// // // 	*b -= n
// // // 	m.Unlock()
// // // 	wg.Done()
// // // }

// // // func main() {
// // // 	first := firstExercise("100, 150, 180")
// // // 	second := secondExercise(3, 5)
// // // 	third := thirdExercise("without, hello,bag,world")
// // // 	fourth := fourthExercise("Hello World")
// // // 	fifth := fifthExercise("hello world and practice makes perfect and hello world again")
// // // 	sixth := sixthExercise("101,0100,0011,10100,1010,1001,1111")
// // // 	seventh := seventhExercise()
// // // 	eighthExercise("hello world! 123")
// // // 	fmt.Println("first: ", first)
// // // 	fmt.Println("Second: ", second)
// // // 	fmt.Println("Third: ", third)
// // // 	fmt.Println("fourth: ", fourth)
// // // 	fmt.Println("fifth: ", fifth)
// // // 	fmt.Println("sixth: ", sixth)
// // // 	fmt.Println("seventh: ", seventh)
// // // 	twelthExercise()
// // // 	thirteenExercise()
// // // 	SwapValues()

// // // 	var car Car = Car{licenseNo: "KL12344", brand: "MG"}
// // // 	var vehicle Vehicle = &car
// // // 	fmt.Println(vehicle.Name())

// // // 	var wc WriterCloser = NewBufferedWriterCloser()
// // // 	wc.Write([]byte("Hello world, this is a test"))
// // // 	wc.Close()

// // // 	var myObj interface{} = NewBufferedWriterCloser()
// // // 	if wc, ok := myObj.(WriterCloser); ok {
// // // 		wc.Write([]byte("Hello world"))
// // // 		wc.Close()
// // // 	}
// // // 	// bwc := wc.(*BufferedWriterCloser)
// // // 	r, ok := myObj.(io.Reader)
// // // 	if ok {
// // // 		fmt.Println(r)
// // // 	} else {
// // // 		fmt.Println("Conversion failed")
// // // 	}
// // // 	// fmt.Println(bwc.buffer)

// // // 	var i interface{} = 0

// // // 	switch i.(type) {
// // // 	case int:
// // // 		fmt.Println("i is an integer")
// // // 	default:
// // // 		fmt.Println("don't know")
// // // 	}

// // // 	var wg sync.WaitGroup
// // // 	var m sync.Mutex

// // // 	wg.Add(200)

// // // 	balance := 100

// // // 	for i := 0; i < 100; i++ {
// // // 		go deposit(&balance, i, &wg, &m)
// // // 		go withdraw(&balance, i, &wg, &m)
// // // 	}
// // // 	wg.Wait()
// // // 	fmt.Println("Final balance value:", balance)
// // // }

// // // package main

// // // import (
// // // 	"fmt"
// // // 	"io"
// // // 	"net/http"
// // // 	"sync"
// // // )

// // // func fetchURL(wg *sync.WaitGroup, url string, ch chan<- string) {
// // // 	defer wg.Done()
// // // 	resp, err := http.Get(url)
// // // 	if err != nil {
// // // 		ch <- fmt.Sprintf("Error fetching %s: %v", url, err)
// // // 		return
// // // 	}

// // // 	defer resp.Body.Close()
// // // 	body, err := io.ReadAll(resp.Body)

// // // 	if err != nil {
// // // 		ch <- fmt.Sprintf("Error reading response from %s: %v", url, err)
// // // 	}

// // // 	ch <- fmt.Sprintf("Fetched %s: %d bytes", url, len(body))

// // // }

// // // func main() {
// // // 	var wg sync.WaitGroup

// // // 	ch := make(chan string, 3)

// // // 	urls := []string{
// // // 		"https://www.google.com",
// // // 		"https://www.github.com",
// // // 		"https://www.openai.com",
// // // 		"https://www.sldfjlds.com",
// // // 	}

// // // 	for _, url := range urls {
// // // 		wg.Add(1)
// // // 		go fetchURL(&wg, url, ch)
// // // 	}

// // // 	go func() {
// // // 		wg.Wait()
// // // 		close(ch)
// // // 	}()

// // // 	for msg := range ch {
// // // 		fmt.Println(msg)
// // // 	}
// // // }

// // package main

// // import (
// // 	"fmt"
// // 	"sort"
// // )

// // func player(name string, table chan int, done chan struct{}) {
// // 	for ball := range table {
// // 		fmt.Printf("%s hits the ball! Ball count: %d\n", name, ball)
// // 		ball++
// // 		if ball > 10 {
// // 			fmt.Printf("Reached 10 hits\n")
// // 			done <- struct{}{}
// // 			return
// // 		}
// // 		table <- ball
// // 	}
// // }

// // func main() {
// // 	even := make(chan int)
// // 	odd := make(chan int)
// // 	table := make(chan int)
// // 	done := make(chan struct{})
// // 	nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 0}

// // 	sort.Ints(nums)

// // 	go generateEven(even, nums)
// // 	go generateOdd(odd, nums)

// // 	for num := range even {
// // 		fmt.Println(num)
// // 	}

// // 	for n := range odd {
// // 		fmt.Println(n)
// // 	}

// // 	// close(odd)

// // 	go player("Player 1", table, done)
// // 	go player("Player 2", table, done)

// // 	table <- 1

// // 	<-done

// // 	var num int = 42
// // 	var ptr *int = &num

// // 	fmt.Println(*ptr)

// // 	fmt.Println("game has ended")
// // }

// // func generateEven(evenChan chan<- int, nums []int) {

// // 	for _, num := range nums {
// // 		if num%2 == 0 {
// // 			evenChan <- num
// // 		}
// // 	}
// // 	close(evenChan)
// // }

// // func generateOdd(oddChan chan<- int, nums []int) {
// // 	for _, num := range nums {
// // 		if num%2 != 0 {
// // 			oddChan <- num
// // 		}
// // 	}
// // 	close(oddChan)
// // }

// // // func evenGenerator() <-chan int {

// // // 	ch := make(chan int)

// // // 	go func() {
// // // 		for i := 0; i < 50; i += 2 {
// // // 			ch <- i
// // // 		}
// // // 		close(ch)
// // // 	}()

// // // 	return ch
// // // }

// // // func main() {
// // // 	for n := range evenGenerator() {
// // // 		fmt.Println(n)
// // // 	}

// // // 	// var a []int

// // // 	arr := []int{6, 7, 8, 9, 10, 56, 3, 2, 90, 2}
// // // 	fmt.Println(mergeSort(arr))

// // // }

// func mergeSort(arr []int) []int {
// 	if len(arr) <= 1 {
// 		return arr
// 	}

// 	mid := len(arr) / 2

// 	left := arr[:mid]

// 	right := arr[mid:]

// 	merge := func(left, right []int) []int {
// 		var result []int
// 		l := 0
// 		r := 0
// 		for l < len(left) && r < len(right) {
// 			if left[l] < right[r] {
// 				result = append(result, left[l])
// 				l += 1
// 			} else {
// 				result = append(result, right[r])
// 				r += 1
// 			}
// 		}
// 		if len(left[l:]) > 0 {
// 			result = append(result, left[l:]...)
// 		}
// 		if len(right[r:]) > 0 {
// 			result = append(result, right[r:]...)
// 		}
// 		return result
// 	}

// 	return merge(mergeSort(left), mergeSort(right))

// }

// // You can edit this code!
// // Click here and start typing.
// package main

// import (
// 	"fmt"
// )

// func fib(n int) int {

// 	if n <= 0 {
// 		return 0
// 	}

// 	a, b := 0, 1

// 	for i := 2; i <= n; i++ {
// 		a, b = b, a+b
// 	}
// 	return b

// }

// func worker(id int, jobs <-chan int, result chan<- int, done chan struct{}) {
// 	for work := range jobs {
// 		result <- fib(work)
// 	}
// 	// done <- struct{}{}
// }

// func main() {
// 	jobs := make(chan int, 100)
// 	result := make(chan int, 100)
// 	done := make(chan struct{})
// 	fmt.Println("Hello, 世界")

// 	for j := 0; j < 3; j++ {
// 		go worker(j, jobs, result, done)
// 	}

// 	for i := 0; i < 50; i++ {
// 		jobs <- i
// 	}
// 	close(jobs)

// 	for r := 0; r < 30; r++ {
// 		fmt.Println(<-result)
// 	}
// 	// for {
// 	// 	select {
// 	// 	case res := <-result:
// 	// 		fmt.Println(res)
// 	// 	case <-done:
// 	// 		return

// 	// 	}

// 	// }

// 	// for r := range result {
// 	// 	fmt.Println(r)
// 	// }
// 	// <-done

// }
