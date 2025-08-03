import socket
import os
import redis
from dotenv import load_dotenv

load_dotenv()

class TwitchIRCClient:
    def __init__(self):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.username = os.getenv('TWITCH_USERNAME')
        self.token = os.getenv('TWITCH_OAUTH')
        self.channel = os.getenv('TWITCH_CHANNEL')

        # Redis setup
        self.redis = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            db=int(os.getenv('REDIS_DB'))
        )

        # IRC connection
        self.sock = socket.socket()
        self.connect()

    def connect(self):
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.token}\r\n".encode('utf-8'))
        self.sock.send(f"NICK {self.username}\r\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\r\n".encode('utf-8'))
        print(f"Connected to {self.channel}")

    def listen(self):
        while True:
            resp = self.sock.recv(2048).decode('utf-8')
            print(resp)
            if resp.startswith("PING"):
                self.sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
            elif "PRIVMSG" in resp:
                user = resp.split("!", 1)[0][1:]
                message = resp.split("PRIVMSG", 1)[1].split(":", 1)[1]
                print(f"{user}: {message.strip()}")
                self.store_message(user, message.strip())

    def store_message(self, user, message):
        entry = {
            'user': user,
            'message': message
        }
        self.redis.rpush(f"chat:{self.channel}", str(entry))

