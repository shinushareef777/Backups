package config

import (
	"github.com/jinzhu/gorm"
)

var DB *gorm.DB

func ConnectDatabase() {
	var err error

	DB, err := gorm.Open("mysql")
}
