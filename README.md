# requestnonsense
because sometimes you need all the chat all the time

## get started

1. git clone
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `cp example_config.toml config.toml`
6. get twitch chat bot token via https://twitchtokengenerator.com/
7.  `python chatlognonsense.py`

## csv-format

the output-format is quite simple. after all, it's basically irc-logging. 

`<timestamp>, <user-role>, <user>, <message>`

### timestamp

it's the default str() for `datetime.datetime`. Given in UTC.

### user-role

currently:
- moderator: 🗡️
- broadcaster: 🎥
- subscriber: 💸
- viewer: 👁️

### todo

- maybe add other output-modules: SQL, JSON, …
- stop using ttg and do things _right_
- have a mechanism to refresh tokens in time
