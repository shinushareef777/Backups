package rabbitmq

// function to connect to rabbitmq and return ch, err := conn.Channel() ch

import (
	"rmq-go/utils"
	"sync"

	amqp "github.com/rabbitmq/amqp091-go"
)

var (
	conn    *amqp.Connection
	ch      *amqp.Channel
	once    sync.Once
	initErr error
)

func initRabbitMQ() {

	conn, initErr = amqp.Dial("amqp://guest:guest@localhost:5672/")
	utils.FailOnError(initErr, "Failed to connect to RabbitMQ")
	// defer conn.Close()

	ch, initErr = conn.Channel()
	utils.FailOnError(initErr, "Failed to open a connection")
	// defer ch.Close()
}

func GetChannel() (*amqp.Channel, error) {
	once.Do(initRabbitMQ)

	return ch, initErr
}
