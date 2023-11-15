FROM golang:1.18

WORKDIR /usr/src/tmp

COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .
RUN go build -v -o /usr/local/bin/go-st

ENTRYPOINT [ "go-st" ]