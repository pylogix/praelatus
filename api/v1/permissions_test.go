package v1_test

import (
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestGetPermissionscheme(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/permissionschemes/1", nil)
	testAdminLogin(w, r)

	router.ServeHTTP(w, r)

	var p models.PermissionScheme

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	if p.ID != 1 {
		t.Errorf("Expected 1 Got %d\n", p.ID)
	}

	t.Log(w.Body)
}

func TestGetAllPermissionschemes(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/permissionschemes", nil)
	testLogin(w, r)

	router.ServeHTTP(w, r)

	var p []models.PermissionScheme

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	t.Log(w.Body)

	if len(p) != 2 {
		t.Errorf("Expected 2 Got %d\n", len(p))
		return
	}

	if p[0].Name != "mock" {
		t.Errorf("Expected mock Got %s\n", p[0].Name)
	}

}

func TestCreatePermissionscheme(t *testing.T) {
	p := models.PermissionScheme{Name: "Snug"}
	byt, _ := json.Marshal(p)
	rd := bytes.NewReader(byt)

	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST", "/api/v1/permissionschemes", rd)
	testAdminLogin(w, r)

	router.ServeHTTP(w, r)

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	if p.ID != 1 {
		t.Errorf("Expected 1 Got %d", p.ID)
	}

	t.Log(w.Body)
}