# discord-tts

Text-to-speech for Discord.

## Usage

```bash
docker run \
  -e DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN\
  -v /path/to/credentials.json:/app/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  ghcr.io/nownabe/discord-tts
```

https://github.com/users/nownabe/packages/container/package/discord-tts
