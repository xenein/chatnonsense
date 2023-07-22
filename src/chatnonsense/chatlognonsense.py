#!/usr/bin/env python3
"""
we snag some twitchchat via websocket/irc and put things in some csv
"""

import twitchio

import csv
import dataclasses
import threading
import tomllib

from datetime import datetime


@dataclasses.dataclass
class serializedMessage:
    timestamp: datetime
    mod: str
    chatter: str
    message: str


class Writer:
    """
    TwitchIO tut Dinge asynchron. Das kann fishy werden, wenn wir da klassisch synchronized in files schreiben.
    besser mal Kanonen zu den Spatzen.
    """

    def __init__(self, path):
        self.write_lock = threading.Lock()
        self.file_path = path

    def write_message(self, message: serializedMessage):
        with self.write_lock:
            with open(self.file_path, "a") as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerow(dataclasses.astuple(message))


class Client(twitchio.Client):
    def __init__(
        self,
        log_csv: str,
        token: str,
        client_id: str,
        client_secret: str,
        channel: str,
        chatty: bool = False,
    ):
        super().__init__(
            token=token, client_secret=client_secret, initial_channels=[channel]
        )
        self.chatty = chatty
        self.writer = Writer(log_csv)

    async def event_message(self, message: twitchio.Message):

        if type(message.author) == twitchio.PartialChatter:
            return

        role: str
        if message.author.is_mod:
            role = "🗡️"
        elif message.author.is_broadcaster:
            role = "🎥"
        elif message.tags.get("subscriber"):
            role = "💸"
        elif "vip" in str(message.tags.get("badges")):
            role = "💎"
        else:
            role = "👁️"

        if self.chatty:
            print(
                f"{message.timestamp} <{role} {message.author.name}>: {message.content}"
            )

        serialized_message = serializedMessage(
            chatter=message.author.name,
            message=message.content,
            timestamp=message.timestamp,
            mod=role,
        )

        thread = threading.Thread(
            target=self.writer.write_message, args=(serialized_message,)
        )
        thread.start()

    async def event_ready(self):
        print(f"Logged in as: {self.nick}")
        print(f"User id: {self.user_id}")


if __name__ == "__main__":
    with open("./config.toml", mode="rb") as tc:
        config = tomllib.load(tc)

    client = Client(
        log_csv=config["csv"]["log_csv"],
        token=config["Twitch"]["ACCESS_TOKEN"],
        client_id=config["Twitch"]["client_id"],
        client_secret=config["Twitch"]["client_secret"],
        channel=config["Twitch"]["CHANNEL"],
        chatty=True,
    )
    client.run()
