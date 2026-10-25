# GrokCord

A Discord bot that connects your server to xAI's Grok and keeps the chat clean.

- `/chat` talks to Grok, and it remembers your conversation per channel
- `/reset` clears your history
- Auto-moderation: spam detection, banned-word filter, strikes and auto-mute
- Mod commands: `/warnings`, `/clearwarnings`, `/mute`, `/unmute`, `/addword`, `/removeword`
- Actions are logged to a `#mod-logs` channel

## Setup
1. Create a bot at https://discord.com/developers/applications and copy the token.
2. In the Bot tab, turn on **Message Content Intent** and **Server Members Intent**.
3. Invite it with scopes `bot` and `applications.commands`, and permissions:
   Manage Messages, Moderate Members, Send Messages, Embed Links, View Channels.
4. Get an API key from the xAI console (https://console.x.ai).
5. `python -m venv venv`, activate it, then `pip install -r requirements.txt`
6. Put your keys in `.env` (see `.env.example`).
7. Make a `#mod-logs` channel, and move the bot's role above your member roles.
8. `python main.py`

## Config
- `config.json` holds the system prompt, history length, spam limits, banned words and mute settings.
- `GROK_MODEL` in `.env` sets the model. Change it if xAI renames models.

## Structure
```
main.py            starts the bot
grok_client.py     talks to the xAI API
db.py              SQLite for chat history and strikes
cogs/chat.py       /chat and /reset
cogs/moderation.py auto-mod and mod commands
```
