import io
import os
import tempfile

import discord
from google.cloud import texttospeech

class MessageClient(discord.Client):
    def __init__(self, language_code, voice_name=None, command_prefix='!tts'):
        super().__init__()

        self.command_prefix = command_prefix

        self.tts_client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        text = message.content

        if not text.startswith(self.command_prefix):
            await self.speech(message)
        elif text == f'{self.command_prefix} start' or text == f'{self.command_prefix} s':
            await self.start_speech(message)
        elif text == f'{self.command_prefix} end' or text == f'{self.command_prefix} e':
            await self.finish_speech(message)
        else:
            await message.channel.send(f"{message.author.mention} Unknown command.")

    async def start_speech(self, message):
        mention = message.author.mention

        if message.author.voice is None:
            await message.channel.send(f"{mention} You're not connected to any voice channel.")
            return
        elif message.guild.voice_client is None:
            text_channel = message.channel
            voice_channel = message.author.voice.channel
            await voice_channel.connect()
            await message.channel.send(f"{mention} Started TTS from {text_channel.mention} to {voice_channel.mention}")
        else:
            await message.channel.send(f"{mention} TTS already started at {message.channel.mention}.")

    async def finish_speech(self, message):
        mention = message.author.mention

        if message.guild.voice_client is None:
            await message.channel.send(f"{mention} TTS is not serving at {message.channel.mention}")
        else:
            await message.guild.voice_client.disconnect()
            await message.channel.send(f"{mention} Finished TTS.")

    async def speech(self, message):
        if len(message.mentions) != 0:
            return
        if message.guild.voice_client is None:
            return

        synthesis_input = texttospeech.SynthesisInput(text=message.content)
        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config)

        mp3 = tempfile.NamedTemporaryFile(mode="wb", prefix="discord-tts_", suffix=".mp3", delete=False)
        mp3.write(response.audio_content)
        mp3.flush()

        message.guild.voice_client.play(
            discord.FFmpegPCMAudio(mp3.name),
            after=self.delete_tempfile_callback(mp3.name)
        )

    def delete_tempfile_callback(self, filename):
        return lambda error: os.remove(filename)

language_code = os.environ.get('TTS_LANGUAGE_CODE', 'en-US')
voice_name = os.environ.get('TTS_VOICE_NAME', None)
command_prefix = os.environ.get('COMMAND_PREFIX', '!tts')

client = MessageClient(language_code, voice_name, command_prefix)
client.run(os.environ.get('DISCORD_BOT_TOKEN'))
