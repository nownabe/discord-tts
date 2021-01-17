apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: discord-tts
  name: discord-tts
  annotations:
    iam.gke.io/gcp-service-account: discord-tts@${GOOGLE_PROJECT_ID}.iam.gserviceaccount.com
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  namespace: discord-tts
  name: discord-tts
spec:
  selector:
    matchLabels:
      app: discord-tts
  serviceName: discord-tts
  replicas: 1
  template:
    metadata:
      labels:
        app: discord-tts
    spec:
      securityContext:
        runAsUser: 61000
        runAsGroup: 61000
        fsGroup: 61000
      serviceAccountName: discord-tts
      containers:
        - name: discord-tts
          image: ghcr.io/nownabe/discord-tts
          envFrom:
            - secretRef:
                name: discord-tts
          resources:
            requests:
              memory: 512Mi
              cpu: 1000m
