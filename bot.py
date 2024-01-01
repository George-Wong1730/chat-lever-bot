import datetime
import discord
import json
import random
import os
import random, string
import requests


#George (c)1-1-2024     
print("##########################################")
print("##请著名来源,George制作！如有雷同纯属巧合##")
print("##########################################")
print("更新时间:1 January 2024 | 21:50PM.........")
print("Uptada time:1 January 2024 | 21:50PM......")

#設定
with open ("config.json",mode="r",encoding="utf-8") as filt:
    data = json.load(filt)
PREFIX = data["prefix"]
op_id = data["owner_id"]
TOKEN = data["token"]
V_NOW = "1.2"




client = discord.Client()

@client.event   
async def on_ready():
        
    print('机器人已启动，目前使用的机器人：',client.user)
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
    await client.change_presence(status= status_w, activity=activity_w)
    
@client.event
async def on_message(message):
#help
    if message.content == f"{PREFIX}help":
        await message.delete()
        embed = discord.Embed(title="指令清单", description=f"前缀是[{PREFIX}]", color=0x04f108)
        embed.add_field(name=f"{PREFIX}help", value="操作手冊")
        embed.add_field(name=f"{PREFIX}info", value="关于")
        embed.add_field(name=f"{PREFIX}oc", value="开启/关闭功能(预设为关闭,第一次设定会自动开启)")
        embed.add_field(name=f"{PREFIX}start <通知訊息發送頻道id(若為0將會發送到預設的頻道)> <多少訊息上升一等>", value="設定")
        embed.add_field(name=f"{PREFIX}me", value="看你的等級和訊息量")
        embed.add_field(name=f"{PREFIX}xp id", value="看别人的资料")
        embed.add_field(name=f"{PREFIX}set id", value="将指定id等级纪录归零")
        await message.channel.send(content=None, embed=embed)

#info
    if message.content == f"{PREFIX}info":
        await message.delete()
        embed = discord.Embed(title="关于", description=f"前辍是{PREFIX}", color=0x04f108)
        embed.add_field(name="目前版本", value=f"v {V_NOW}")
        embed.add_field(name="关于此机器人:", value="来自开源: https://github.com/George-Wong1730/chat-lever-bot/")
        await message.channel.send(content=None, embed=embed)

#start
    if message.content.startswith(f'{PREFIX}start'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            tmp = message.content.split(" ",2)
            CL = tmp[1]
            tmp = message.content.split(f"{CL} ",2)
            msg = tmp[1]
            filepath = f"data/{message.guild.id}/config.json"
            if os.path.isfile(filepath):
                with open (f"data/{message.guild.id}/config.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                data["cl"] = int(CL)
                data["msg"] = int(msg)
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                if CL == "0":
                    cls = "预设"
                else:
                    cls = f"<#{CL}>"
                await message.channel.send(f"{message.author.mention}设定完成!\n目前设定:\n\n提示频道: {cls}\n升级所要的讯息数量: {msg}")
            else:
                os.mkdir(f"data/{message.guild.id}")
                if CL == "0":
                    cls = "预设"
                else:
                    cls = f"<#{CL}>"
                data = {"cl":CL,"msg":msg,"open":"1"}
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                    await message.channel.send(f"{message.author.mention}设定完成!\n目前设定:\n\n提示频道: {cls}\n升级所要的讯息数量: {msg}")
        else:
            await message.channel.send(f"{message.author.mention}你没有权限更改这个设定！")

    if message.content == f"{PREFIX}me":
        with open (f"data/{message.guild.id}/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}\n你目前的等级:`{data['now']}`\n说话的次数:`{data['msg']}`")

    if message.content.startswith(f'{PREFIX}xp'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("你是在查谁的等级？")
      else:
        with open (f"data/{message.guild.id}/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}id`{tmp[1]}`\n他目前等级:`{data['now']}`\n说话的次数:`{data['msg']}`")

    #set
    if message.content.startswith(f'{PREFIX}set'):
        if message.author.guild_permissions.manage_messages:
          await message.delete()
          tmp = message.content.split(" ",2)
          tmp1 = tmp[1]
          #亨哥0126
          if len(tmp) == 1:
            await message.channel.send(f"格式:{PREFIX}set id")
          else:
              filepath = f"data/{message.guild.id}/{message.author.id}.json"
              with open (f"data/{message.guild.id}/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
              data["msg"] = 0
              data["now"] = 0
              if os.path.isfile(filepath):
                with open (f"data/{message.guild.id}/{tmp1}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                await message.channel.send(f"已经把id:`{tmp1}`等级记录归零")
              else:
                await message.channel.send(f"找不到关于ID:`{tmp1}`的记录")
        else:
            await message.channel.send(f"{message.author.mention}你沒有權限")

    if message.content == f"{PREFIX}oc":
        if message.author.guild_permissions.manage_messages:
            with open (f"data/{message.guild.id}/config.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            if data["open"] == "1":
                data["open"] = "0"
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    data = json.dump(data,filt)
                await message.channel.send(f"{message.author.mention}已`关闭`等级功能")
            else:
                data["open"] = "1"
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    data = json.dump(data,filt)
                await message.channel.send(f"{message.author.mention}已`开启`等级功能")

    if message.author.bot:
        return
    else:
        filepath = f"data/{message.guild.id}/config.json"
        if os.path.isfile(filepath):
            with open (f"data/{message.guild.id}/config.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
                up_msg = data["msg"]
                up_cl = data["cl"]
            if data["open"] == "1":
                filepath = f"data/{message.guild.id}/{message.author.id}.json"
                if os.path.isfile(filepath):
                    with open (f"data/{message.guild.id}/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                        data = json.load(filt)
                    next_msg = int(data["msg"]) + 1
                    IF_msg = int(next_msg) // int(up_msg)
                    if int(IF_msg) > int(data["now"]):
                        up = int(data["now"]) + 1
                        data["msg"] = next_msg
                        data["now"] = int(IF_msg)
                        with open (f"data/{message.guild.id}/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                            data = json.dump(data,filt)
                        if up_cl == 0:
                            await message.channel.send(f"{message.author.mention}恭喜你升级到`{up}`等")
                        else:
                            channel = client.get_channel(int(up_cl))
                            await channel.send(f"{message.author.mention} 恭喜你升级到`{up}`等")
                    else:
                        next_msg = int(data["msg"]) + 1
                        data["msg"] = next_msg
                        with open (f"data/{message.guild.id}/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                            data = json.dump(data,filt)
                else:
                    with open (f"data/{message.guild.id}/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                        data = {"msg":"1","now":"0"}
                        data = json.dump(data,filt)
            

client.run(TOKEN)