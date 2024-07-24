package main

import (
	"fmt"
	"net/http"
	"sync"
)

var wg = sync.WaitGroup{}

func worker(in <-chan string, out chan<- string) {
	defer wg.Done()
	for url := range in {
		resp, err := http.Get(url)
		if err != nil {
			continue
		}

		if resp.StatusCode == http.StatusOK {
			out <- url
		}
		resp.Body.Close()
	}
}

func main() {
	urls := []string{"https://www.dsalkfjlkadsjf.com", "https://www.example.com", "https://www.google.com"}

	urlChan := make(chan string)
	successChan := make(chan string)

	wg.Add(3)

	go worker(urlChan, successChan)

	go func() {
		for _, url := range urls {
			urlChan <- url
		}
		close(urlChan)
		wg.Done()
	}()

	go func() {
		for url := range successChan {
			fmt.Println(url)
		}
		close(successChan)
		wg.Done()
	}()

	wg.Wait()

}
