package main

import (
	"context"
	"log"
	"os"
	"rmq-go/rabbitmq"
	"rmq-go/utils"
	"strings"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func bodyFrom(args []string) string {
	var s string
	if (len(args) < 3) || os.Args[2] == "" {
		s = "hello"
	} else {
		s = strings.Join(args[2:], " ")
	}
	return s
}

func severityFrom(args []string) string {

	var s string
	if (len(args) < 2) || os.Args[1] == "" {
		s = "info"
	} else {
		s = os.Args[1]
	}

	return s
}

func main() {
	ch, err := rabbitmq.GetChannel()

	utils.FailOnError(err, "Failed to connect or failed to get channel")

	err = ch.ExchangeDeclare("logs_direct", "direct", true, false, false, false, nil)

	utils.FailOnError(err, "Failed to declare an exchange")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	body := bodyFrom(os.Args)
	err = ch.PublishWithContext(ctx, "logs_direct", severityFrom(os.Args), false, false, amqp.Publishing{
		DeliveryMode: amqp.Persistent,
		ContentType:  "text/plain",
		Body:         []byte(body),
	})

	utils.FailOnError(err, "Failed to publish a message")
	log.Printf(" [x] Sent %s\n", body)
}
