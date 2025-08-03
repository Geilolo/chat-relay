from twitch_irc import TwitchIRCClient

def main():
    twitch_client = TwitchIRCClient()
    twitch_client.listen()

if __name__ == "__main__":
    main()

