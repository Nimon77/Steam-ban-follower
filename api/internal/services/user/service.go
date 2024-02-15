package user

import (
	"context"
	"sync"

	"github.com/nimon77/steam-users-monitor/internal/interfaces"
	"github.com/nimon77/steam-users-monitor/pkg/openapi/v1"
)

var _ interfaces.IUserService = (*UserService)(nil)

type UserService struct {
	identifierLocks sync.Map
	globalLock      sync.RWMutex
}

func NewUserService() *UserService {
	return &UserService{}
}

func (s *UserService) Get(ctx context.Context) ([]*openapi.User, error) {
	return nil, nil
}
