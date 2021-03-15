import discord
from discord.ext import commands
from discord import FFmpegOpusAudio
from dotenv import load_dotenv
import os

load_dotenv()

RADIO_URL = "http://stream.antenne1.de/a1stg/livestream1.aac"




class thePunisher(commands.Bot):

    def __init__(self,command_prefix="$", case_insensitive=True ):
        super().__init__(command_prefix="$", case_insensitive=True)
        self.is_punishing = False
        self.victim = None
        self.setup()

    async def on_voice_state_update(self,member, before, after):
        if self.is_punishing and member == self.victim:
            voice = discord.utils.get(self.voice_clients, guild=member.guild)
            if (before.channel != after.channel and after.channel)  and not (voice and voice.channel == after.channel):
                
                # If bot is not connected anymore, try to find empty voice channels
                if voice is None:
                    for channel in member.guild.voice_channels:
                        if not channel.voice_states:
                            await channel.connect()
                            break
                    voice = discord.utils.get(self.voice_clients, guild=member.guild)
                    if voice is None or not voice.is_connected():
                        return
    
                text_channel = member.guild.text_channels[0]
                if text_channel is not None:
                    await text_channel.send("Hier geblieben!")

                # Move the victim in the channel of the bot and play music if not already playing
                if not voice.is_playing():
                    voice.play(FFmpegOpusAudio(RADIO_URL,bitrate=2))
                await member.move_to(voice.channel)   

    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))

    def setup(self):
        @self.command()
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


        @self.command()
        async def leave(ctx):
            voice = ctx.voice_client
            if voice is None or not voice.is_connected():
                await ctx.send("Junge, komm mal klar. Was willst du von mir?")
            else:
                await voice.disconnect()

        @self.command()
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
                self.victim = victim
                self.is_punishing = True

        @self.command()
        async def stop(ctx):
            await ctx.send("Du bist frei {0} ... fürs Erste".format(self.victim.mention))
            self.is_punishing = False
            self.victim = None

        @punish.error
        async def punish_error(ctx,error):
            if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            # Wenn kein Member ermittelt werden konnte
                await punish(ctx,ctx.author)

if __name__ == "__main__":
    client = thePunisher(command_prefix="$", case_insensitive=True)
    client.run(os.getenv("TOKEN"))
