import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client, addr = server_socket.accept()
    print(addr)
    data = client.recv(1024).decode()
    print(f"data is {data}")

    line = data.split("\r\n")
    line_first = data.split("\r\n")[0]
    print(f"full line is :{line} ")
    print(f"truncated line is :{line_first}")

    path = line_first.split(" ")
    path_actual = line_first.split(" ")[1]

    print(f"list of path is : {path}")
    print(f"wanted path is path is : {path_actual}")


    if path_actual == "/":
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    elif path_actual.startswith("/echo/"):
        # Extract everything after "/echo/" (6 characters long)
        echo_str = path_actual[6:]
        print(f"echo_str{echo_str}")
        content_length = len(echo_str)
        print(f"content length {content_length}")

        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {content_length}\r\n\r\n"
            f"{echo_str}"
        )
        client.sendall(response.encode())

    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") 

    

    


if __name__ == "__main__":
    main()
