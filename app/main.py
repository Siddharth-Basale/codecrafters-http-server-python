import socket  # noqa: F401
import threading
import os
import gzip


def handle_client(client, addr):
    print(f"New Connected at addr {addr}")
    while True:
        data = client.recv(1024).decode()
        print(f"data is :{data}")

        line = data.split("\r\n")
        line_first = data.split("\r\n")[0]
        print(f"full line is :{line} ")
        if line[2] == "Connection: close":
            response = (
                            f"HTTP/1.1 200 OK\r\n"
                            f"Content-Type: text/plain\r\n"
                            f"Connection: close\r\n\r\n"
                           
                        )
            client.sendall(response.encode())
            
            break
        print(f"truncated line is :{line_first}")

        path = line_first.split(" ")
        path_actual = line_first.split(" ")[1]

        print(f"list of path is : {path}")
        print(f"wanted path is path is : {path_actual}")


        if path_actual == "/":
            client.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")

        elif path_actual.startswith("/echo/"):
            echo_str = path_actual[6:]
            print(f"echo_str{echo_str}")
            content_length = len(echo_str)
            print(f"content length {content_length}")

            if "gzip" in line[2]:
                body = path_actual[6:]
                print(f"body is {body}")
                encoded = body.encode()
                compressed = gzip.compress(encoded)
                length = len(compressed)
                headers= (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Encoding: gzip\r\n"
                    f"Content-Length:{length} \r\n"
                    f"Content-Type: text/plain\r\n\r\n"
                )
                response  = headers.encode()+ compressed 
                client.sendall(response)

            elif line[2].startswith("Accept-Encoding:") and "gzip" not in line[2]:
                response  = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n\r\n"
                )
                client.sendall(response.encode())



            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {content_length}\r\n\r\n"
                f"{echo_str}"
            )
            client.sendall(response.encode())

        elif path_actual == "/user-agent":
            val = line[2]
            ans = val[12:]
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(ans)}\r\n\r\n"
                f"{ans}"
            )
            client.sendall(response.encode())


        elif path_actual[0:7] == "/files/":
            if path[0] == "GET":
                path = path_actual[7:]
                print(path)
                if os.path.isfile("/tmp/data/codecrafters.io/http-server-tester/"+path):
                    with open("/tmp/data/codecrafters.io/http-server-tester/"+path, "rb") as f:
                        body = f.read()
                        print(body)
                        content_length = len(body)
                        print("length is", content_length )
                    headers = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: application/octet-stream\r\n"
                        f"Content-Length: {content_length}\r\n\r\n"
                    )
                    header_byte = headers.encode()
                    responce = header_byte + body
                    client.sendall(responce)
                else:
                    client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            else:
                print("its post")
                path = path_actual[7:]
                print(path)
                full_path = os.path.join("/tmp/data/codecrafters.io/http-server-tester/", path)
                body = line[5]
                with open(full_path, "w") as f:
                    f.write(body)
                client.sendall(b"HTTP/1.1 201 Created\r\n\r\n")





        else:
            client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") 
    client.close()
 




def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client, addr = server_socket.accept()
    
        thread = threading.Thread(target = handle_client, args=(client, addr))
        thread.start()
  
    

    

    


if __name__ == "__main__":
    main()
