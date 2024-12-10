import socket
import threading
import time
import random

# Состояния узлов
FOLLOWER = "Follower"
CANDIDATE = "Candidate"
LEADER = "Leader"

class Node:
    def __init__(self, node_id, port, peer_ports):
        self.node_id = node_id
        self.port = port
        self.peer_ports = peer_ports
        self.state = FOLLOWER
        self.votes = 0
        self.current_leader = None
        self.election_timeout = random.uniform(5, 10)  # Случайный тайм-аут для выборов
        self.last_heartbeat = time.time()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("localhost", self.port))

    def send_message(self, message, target_port):
        """Отправить сообщение на указанный порт."""
        self.sock.sendto(message.encode(), ("localhost", target_port))

    def broadcast_message(self, message):
        """Рассылка сообщения всем узлам."""
        for peer_port in self.peer_ports:
            self.send_message(message, peer_port)

    def handle_message(self, message, addr):
        """Обработка входящих сообщений."""
        if message.startswith("VoteRequest"):
            if self.state == FOLLOWER:
                print(f"Node {self.port} votes for {addr[1]}")
                self.send_message("VoteGranted", addr[1])
        elif message.startswith("VoteGranted"):
            if self.state == CANDIDATE:
                self.votes += 1
                print(f"Node {self.port} received vote from {addr[1]}")
        elif message.startswith("Heartbeat"):
            self.state = FOLLOWER
            self.current_leader = addr[1]
            self.last_heartbeat = time.time()
            print(f"Node {self.port} received heartbeat from leader {addr[1]}")

    def run(self):
        """Запуск узла."""
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.monitor).start()

    def listen(self):
        """Слушать входящие сообщения."""
        while True:
            message, addr = self.sock.recvfrom(1024)
            self.handle_message(message.decode(), addr)

    def monitor(self):
        """Мониторинг состояния узла."""
        while True:
            if self.state == FOLLOWER and time.time() - self.last_heartbeat > self.election_timeout:
                self.start_election()
            elif self.state == CANDIDATE and self.votes > len(self.peer_ports) // 2:
                self.become_leader()
            elif self.state == LEADER:
                self.broadcast_message("Heartbeat")
            time.sleep(1)

    def start_election(self):
        """Инициация процесса выборов."""
        self.state = CANDIDATE
        self.votes = 1  # Голос за себя
        print(f"Node {self.port} started an election")
        self.broadcast_message("VoteRequest")

    def become_leader(self):
        """Становление лидером."""
        self.state = LEADER
        self.current_leader = self.port
        print(f"Node {self.port} is now the leader")
        self.broadcast_message("Heartbeat")


def main():
    # Создание узлов
    nodes = [
        Node(node_id=1, port=3000, peer_ports=[3001, 3002]),
        Node(node_id=2, port=3001, peer_ports=[3000, 3002]),
        Node(node_id=3, port=3002, peer_ports=[3000, 3001]),
    ]

    # Запуск узлов
    for node in nodes:
        threading.Thread(target=node.run).start()

    # Основной поток остается активным
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
