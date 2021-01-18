# discord-tts

Text-to-speech for Discord.


## Usage

```bash
docker run \
  -e DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN\
  -v /path/to/credentials.json:/app/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  ghcr.io/nownabe/discord-tts:1.0.0
```

https://github.com/users/nownabe/packages/container/package/discord-tts


## Environment Variables

* `DISCORD_BOT_TOKEN` - (Required) Your Discord bot token.
* `COMMAND_PREFIX` - (Default: `!tts`) Prefix to command the bot.
* `TTS_LANGUAGE_CODE` - (Default: `en-US`) Language code expressed as a [BCP-47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt) language tag.
* `TTS_VOICE_NAME` - (Default: `None`) You can choose voice type. See [Text-to-Speech reference](https://cloud.google.com/text-to-speech/docs/voices) to get voice options.


## Bot Usage

1. Connect to voice channel
1. Type `!tts start` into text chat
1. Type any messages in text chat


## Deploy to Google Kubernetes Engine

```bash
# Use your own GOOGLE_PROJECT_ID and DISCORD_BOT_TOKEN

gcloud iam service-account create discord-tts --project ${GOOGLE_PROJECT_ID}
gcloud iam service-accounts add-iam-policy-binding \
  discord-tts@${GOOGLE_PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:${GOOGLE_PROJECT_ID}.svc.id.goog[discord-tts/discord-tts]" \
  --project ${GOOGLE_PROJECT_ID}
kubectl create namespace discord-tts
kubectl create secret generic discord-tts \
  -n discord-tts \
  --from-literal=DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
envsubst < k8s.yaml.tpl | kubectl apply -f -
```
