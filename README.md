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


## Environment Variables

* `DISCORD_BOT_TOKEN` - Your Discord bot token.


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
