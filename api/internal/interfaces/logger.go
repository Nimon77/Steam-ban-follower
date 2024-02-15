package interfaces

import (
	"context"

	"go.uber.org/zap"
)

type ILoggerService interface {
	InGlobalContext(ctx context.Context, additionalFields ...zap.Field) context.Context
	LoggerG(ctx context.Context) *zap.Logger
	Logger() *zap.Logger
}
