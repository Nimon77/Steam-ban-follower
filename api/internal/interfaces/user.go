package interfaces

import (
	"context"

	"github.com/nimon77/steam-users-monitor/pkg/openapi/v1"
)

type IUserService interface {
	Get(ctx context.Context) ([]*openapi.User, error)
}
