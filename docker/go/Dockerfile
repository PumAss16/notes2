FROM golang:1.21-alpine AS builder
WORKDIR /home/pumas/Desktop/my-project/notes2/docker/go
COPY main.go  .
RUN go build -o myapp main.go
FROM alpine:latest
WORKDIR /home/pumas/Desktop/my-project/notes2/docker/go
COPY --from=builder /home/pumas/Desktop/my-project/notes2/docker/go/myapp .
CMD ["./myapp"]
