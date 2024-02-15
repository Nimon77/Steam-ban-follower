package main

import (
	"context"
	"fmt"
	"log"

	"github.com/labstack/echo"
	"github.com/nimon77/steam-users-monitor/pkg/openapi/v1"
	"github.com/spf13/cobra"
)

var version string = "dev"

var _ openapi.ServerInterface = (*Application)(nil)

type Application struct {
	*echo.Echo
	config *Config
}

func NewApplication(config *Config) *Application {
	return &Application{
		Echo:   echo.New(),
		config: config,
	}
}

func (app *Application) Run(ctx context.Context) error {
	return app.Start(fmt.Sprintf("%s:%d", app.config.HTTPListen, app.config.HTTPPort))
}

var runCmd = &cobra.Command{
	Use: "run",
	Run: func(cmd *cobra.Command, args []string) {
		log.Println("test")

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
