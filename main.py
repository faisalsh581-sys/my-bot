import discord
from discord.ext import commands
from datetime import datetime
import os

intents = discord.Intents.default()
intents.voice_states = True 
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_CATEGORY_NAME = "🎙️︱〢︱rooms︱•︱رومات"
LOG_CHANNEL_ID = 1481175006909169747 
voice_data = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.category and after.channel.category.name == TARGET_CATEGORY_NAME:
        if before.channel != after.channel:
            voice_data[member.id] = datetime.now()

    if before.channel and before.channel.category and before.channel.category.name == TARGET_CATEGORY_NAME:
        if before.channel != after.channel:
            entry_time = voice_data.pop(member.id, None)
            if entry_time:
                exit_time = datetime.now()
                duration = exit_time - entry_time
                hours, remainder = divmod(int(duration.total_seconds()), 3600)
                minutes, _ = divmod(remainder, 60)
                entry_str = entry_time.strftime("%I:%M %p")
                exit_str = exit_time.strftime("%I:%M %p")

                embed = discord.Embed(title="🎙️ سجل مكالمة صوتية", color=0x2f3136)
                embed.add_field(name="User", value=member.mention, inline=False)
                embed.add_field(name="Entry", value=f"``{entry_str}``", inline=True)
                embed.add_field(name="Exit", value=f"``{exit_str}``", inline=True)
                embed.add_field(name="Duration", value=f"**{hours}** hours and **{minutes}** minutes", inline=False)
                embed.set_footer(text="صنع من قبل منظومة طايف")
                
                log_channel = bot.get_channel(LOG_CHANNEL_ID)
                if log_channel:
                    await log_channel.send(embed=embed)

bot.run('MTQ4MTE3NTk4NDYzOTA0OTkxMA.GgZJsS.jmiOlJ3IQll80K9PcEs-Pr8b1LnmylC0xLwub0')
