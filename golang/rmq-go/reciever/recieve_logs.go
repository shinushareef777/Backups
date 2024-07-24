package main

import (
	"log"
	"os"
	"rmq-go/rabbitmq"
	"rmq-go/utils"
)

func main() {
	ch, err := rabbitmq.GetChannel()
	utils.FailOnError(err, "Failed to connect or failed to get channel")

	err = ch.ExchangeDeclare("logs_direct", "direct", true, false, false, false, nil)
	utils.FailOnError(err, "Failed to declare an exchange")

	q, err := ch.QueueDeclare("", false, false, true, false, nil)
	utils.FailOnError(err, "Failed to declare a queue")

	// err = ch.Qos(1, 0, false)
	// utils.FailOnError(err, "Failed to set QoS")

	// err = ch.QueueBind(q.Name, "", "logs", false, nil)
	// utils.FailOnError(err, "Failed to declare a queue")

	if len(os.Args) < 2 {
		log.Printf("Usage: %s [info|warning|error]\n", os.Args[0])
		os.Exit(0)
	}

	for _, s := range os.Args[1:] {
		log.Printf("Binding queue %s to exchange %s with routing key %s", q.Name, "logs_direct", s)
		err = ch.QueueBind(q.Name, s, "logs_direct", false, nil)
		utils.FailOnError(err, "Failed to bind a queue")
	}

	msgs, err := ch.Consume(q.Name, "", true, false, false, false, nil)
	utils.FailOnError(err, "Failed to register a consumer")

	var forever chan struct{}

	go func() {

		for d := range msgs {
			log.Printf("Received a message: %s", d.Body)
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever

	// select {
	// case <-forever:
	// 	log.Printf(" [*] Exiting...")
	// case <-time.After(5 * time.Second):
	// 	log.Printf(" [*] Timeout")
	// }
}
