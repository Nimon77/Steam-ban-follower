package applications

import "github.com/labstack/echo"

// Application is the main application
type Application struct {
	*echo.Echo
}

// NewApplication creates a new application
func NewApplication() *Application {
	return &Application{
		Echo: echo.New(),
	}
}