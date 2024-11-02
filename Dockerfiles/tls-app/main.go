package main

import (
	"crypto/tls"
	"fmt"
	"log"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, TLS world!")
	logRequest(r)
}

func logRequest(r *http.Request) {
	log.Printf("Received request: Method=%s, URL=%s, RemoteAddr=%s, UserAgent=%s", r.Method, r.URL, r.RemoteAddr, r.UserAgent())
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", handler)

	server := &http.Server{
		Addr:    ":8443",
		Handler: mux,
		TLSConfig: &tls.Config{
			Certificates: []tls.Certificate{getCertificate()},
			MinVersion:   tls.VersionTLS12,
		},
	}

	log.Println("Starting server with TLS")
	log.Fatal(server.ListenAndServeTLS("cert.pem", "key.pem"))
}

func getCertificate() tls.Certificate {
	cert, err := tls.LoadX509KeyPair("cert.pem", "key.pem")
	if err != nil {
		log.Fatalf("Failed to load certificate: %v", err)
	}
	return cert
}
