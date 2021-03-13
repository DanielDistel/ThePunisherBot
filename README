# ThePunisher Discord Bot

This is a simple bot, which can be used to punish discord users with low bitrate internet radio audio.

## Getting Started

This python program has a few prerequisities to run.
First of all, you have to register a Bot on the Discord homepage and get a Token.
This Token should then be included in an `.env` file which should be located in the same directory as main.py, like:
```
TOKEN=??????
```

### Dependencies

ThePunisher Bot uses the discord.py module to access the Discord API. To install the module as well as the modules which are used to load the `.env` file and to connect to the voice channel, the following commands can be used:
```
pip install discord.py
pip install PyNaCl
pip install python-dotenv
```

To play the audio stream in a voice channel discord.py uses [FFmpeg](https://www.ffmpeg.org/). Make sure to add the installed program to the path!

## Usage 

With the command `$join` you can let the bot join your voice channel and automatically play the audio stream.
`$leave` will disconnect the bot from the voice channel.
You can use `$punish @username` to punish a specified member in your voice channel, but it's only possible if there is an empty voice channel on the discord server.