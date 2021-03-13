import discord
from discord.ext import commands
from discord import FFmpegOpusAudio
from dotenv import load_dotenv
import os

load_dotenv()

RADIO_URL = "http://stream.antenne1.de/a1stg/livestream1.aac"

client = commands.Bot(command_prefix="$", case_insensitive=True)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command()
async def join(ctx):
    if ctx.author.voice is not None:
        voiceChannel = ctx.author.voice.channel
        voice = ctx.voice_client
        if voice is None:
            await voiceChannel.connect()
            await ctx.send("HERE'S JOHNNY")
            voice = ctx.voice_client
            voice.play(FFmpegOpusAudio(RADIO_URL,bitrate=2))

        else:
            await ctx.send("Bin gerade beschäftigt, sorry.")

    else:
        await ctx.send("{0}, komm erst mal ran aufn Meter!".format(
            ctx.author.mention))


@client.command()
async def leave(ctx):
    voice = ctx.voice_client
    if voice is None or not voice.is_connected():
        await ctx.send("Junge, komm mal klar. Was willst du von mir?")
    else:
        await voice.disconnect()

@client.command()
async def punish(ctx, victim: discord.Member):
    # Wenn Author nicht connected ist, sende nen Spruch
    if ctx.author.voice is None:
        await ctx.send("{0}, komm erst mal ran aufn Meter!".format(
            ctx.author.mention))
        return
    else:
        # Wenn Victim nicht connected ist, sende Spruch
        if victim.voice is None:
            await ctx.send("Wenn ich {0} in Finger bekomme...".format(victim.mention))
            return

        # Wenn Author connected ist, aber nicht im selben Channel wie Victim, dann wird er gepunished
        elif victim.voice.channel != ctx.author.voice.channel:
            await ctx.send("You can't trick the Punisher.")
            victim = ctx.author

        # Wenn bot nicht connected ist, suche einen freien Voicechannel
        voice = ctx.voice_client
        if voice is None:
            for channel in ctx.guild.voice_channels:
                if not channel.voice_states:
                    await channel.connect()
                    break
            voice = ctx.voice_client
            if voice is None or not voice.is_connected():
                await ctx.send(
                        "Ich kann nicht, wenn mir jemand dabei zuschaut...")
                return
        
        # Ist im Voice Channel nur der Bot, dann ziehe Victim zum Bot
        else:
            if len(voice.channel.voice_states.keys()) > 1:
                for channel in ctx.guild.voice_channels:
                    if not channel.voice_states:
                        await voice.move_to(channel)
                        break

        # Verschieben des Victims
        if not voice.is_playing():
            voice.play(FFmpegOpusAudio(RADIO_URL,bitrate=2))
        await ctx.send("Mach dich bereit für deine Strafe!")
        await victim.move_to(voice.channel)


@punish.error
async def punish_error(ctx,error):
  if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
  # Wenn kein Member ermittelt werden konnte
      await punish(ctx,ctx.author)

client.run(os.getenv("TOKEN"))
