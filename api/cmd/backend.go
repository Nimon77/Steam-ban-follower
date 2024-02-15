package main

import (
	"context"
	"fmt"
	"log"

	"github.com/labstack/echo/v4"
	"github.com/nimon77/steam-users-monitor/pkg/openapi/v1"
	"github.com/spf13/cobra"
)

var version string = "dev"

var _ openapi.ServerInterface = (*Application)(nil)

type Application struct {
	*echo.Echo
}

// GetUsers implements openapi.ServerInterface.
func (*Application) GetUsers(ctx echo.Context) error {
	panic("unimplemented")
}

func (app *Application) Run(ctx context.Context) error {
	// return app.Start(fmt.Sprintf("%s:%d", app.config.HTTPListen, app.config.HTTPPort))
	return app.Start(fmt.Sprintf("%s:%d", "0.0.0.0", 8080))
}

var runCmd = &cobra.Command{
	Use: "run",
	Run: func(cmd *cobra.Command, args []string) {
		log.Println("test")
		app := &Application{echo.New()}

		app.GET("/v1", func(c echo.Context) error {
			return c.String(200, "Hello, World!")
		})

		if err := app.Run(context.Background()); err != nil {
			log.Fatal(err)
		}
	}}

var rootCmd = &cobra.Command{
	Use:     "backend",
	Version: version,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

func main() {
	rootCmd.PersistentFlags().StringP("config", "c", "config.yml", "path to configuration file")

	rootCmd.AddCommand(runCmd)
	rootCmd.Execute()

}
