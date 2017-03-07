package v1

import (
	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/store"
)

// Store is the global store used in our HTTP handlers.
var Store store.Store

// Cache is the global session store used in our HTTP handlers.
var Cache store.SessionStore

func V1Routes(router *mux.Router) {
	labelRouter(router)
	fieldRouter(router)
	projectRouter(router)
	teamRouter(router)
	ticketRouter(router)
	typeRouter(router)
	userRouter(router)
	workflowRouter(router)
}
