FROM golang:1.19

WORKDIR /app

COPY go.mod ./

RUN go mod download

COPY *.go ./

RUN go build -o tls-app .

EXPOSE 8443

CMD ["./tls-app"]
