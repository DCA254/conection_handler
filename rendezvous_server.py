import socket
import threading

HOST = '0.0.0.0'
PORT = 6000

clients = []

def handle_client(conn, addr):
    print(f"[+] Cliente conectado: {addr}")
    clients.append(conn)

    if len(clients) == 2:
        print("[*] Fazendo troca de IPs entre os dois clientes...")
        client1 = clients[0]
        client2 = clients[1]

        addr1 = client1.getpeername()
        addr2 = client2.getpeername()

        client1.send(f"{addr2[0]}:{addr2[1]}".encode())
        client2.send(f"{addr1[0]}:{addr1[1]}".encode())

        clients.clear()

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
        except:
            break

    conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[*] Rendezvous Server rodando em {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
