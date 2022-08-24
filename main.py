import datetime
import interactions
import json
import asyncio

with open('./config.json', 'r') as f:
    data = json.load(f)

bot = interactions.Client(token=data["token"],presence=interactions.ClientPresence(activities=[interactions.PresenceActivity(name="La Réputation", type=interactions.PresenceActivityType.WATCHING)]))
            
    
if data["SlashCommand"]:
    @bot.command(
        name="show",
        description="vous donne le nombre de point boutique",
        scope=int(data["guildId"])
    )
    async def show(ctx: interactions.CommandContext):
        userid = ctx.author.id
        avatar = ctx.author.avatar
        with open('./rep.json', 'r') as f:
            dataload = json.load(f)
            try:
                userdata = dataload[userid]
                rep = userdata["rep"]
            except:
                userid = int(userid)
                rep = 0
                value = {"rep":rep}
                with open('./rep.json','r+') as f:
                    file_data = json.load(f)
                    file_data[userid] = value
                    f.seek(0)
                    json.dump(file_data,f,indent=4) 
        embed = interactions.Embed(title="Réputation de "+ctx.author.name,color=0xA37FC8,footer=interactions.EmbedFooter(text="Attention vous ne pouvez checker que vos propres stats"),timestamp=datetime.datetime.now())
        embed.add_field(name="Points de réputation :",value=rep)
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{userid}/{avatar}.png?size=512")
        await ctx.send(embeds=embed,ephemeral=True)

    @bot.command(
        name="rep",
        description="vous donne le nombre de point boutique",
        scope=int(data["guildId"]),
        options=[
            interactions.Option(
                name="user",
                type=interactions.OptionType.USER,
                description="Indiquez l'utilisateur",
                required=True
            )
        ]
    )
    async def rep(ctx: interactions.CommandContext,user: interactions.User):
        verif = False
        roleverif = data["roleverif"]
        member = interactions.Member(**await bot._http.get_member(data["guildId"],user.id),_client=bot._http)
        userid = user.id
        userid = int(userid)
        useravatar = user.avatar
        listrole = member.roles
        rep = 0
        if user.id != ctx.author.id:
            for i in listrole:
                if i in roleverif:
                    verif = True
                    break
            try:
                with open('./rep.json', 'r+') as f:
                    dataload = json.load(f)
                    userdata = dataload[user.id]
                    rep = userdata["rep"]
                    rep = int(rep)
                    rep += 1
                    if (rep == 25) and (not verif):
                        channel = interactions.Channel(** await bot._http.get_channel(980577733916622918), _client=bot._http)
                        embedstaff = interactions.Embed(title="Passage en joueur Vérifier",color=0xA37FC8,timestamp=datetime.datetime.now())
                        embedstaff.add_field(name="joueur",value=f"<@{member.id}>")
                        embedstaff.add_field(name="Nombre de réputation",value=rep)
                        embedstaff.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{userid}/{useravatar}.png?size=512")
                        await channel.send(embeds=embedstaff)
                    userdata["rep"] = rep
                    f.seek(0)        # <--- should reset file position to the beginning.
                    json.dump(dataload, f, indent=4)
                    f.truncate()     # remove remaining part
            except:
                rep = 1
                value = {"rep":rep}
                with open('./rep.json','r+') as f:
                    file_data = json.load(f)
                    file_data[userid] = value
                    f.seek(0)
                    json.dump(file_data,f,indent=4) 
            embed = interactions.Embed(title="Ta réputation",color=0xA37FC8,timestamp=datetime.datetime.now(),description="Tu viens de gagner un point de réputation qui vient récompenser ton bon comportement en jeu")
            embed.add_field(name="**Total de reputation :**", value=rep)
            embed.add_field(name="**Rappel**",value="tu peux consulter à  tout moment le montant de points que tu as acquis en tapant la commande **+show**")
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{userid}/{useravatar}.png?size=512")
            await member.send(embeds=embed)
            await ctx.send(content=f"<@{ctx.author.id}>, ton +rep a bien été pris en compte",ephemeral=True)
        else:
            await ctx.send(content=f"<@{ctx.author.id}>, tu ne peux pas voté pour toi meme ",ephemeral=True)


    @bot.command(
        name="reset",
        description="reset l'utilisateur au niveau de la reputation",
        scope=int(data["guildId"]),
        options=[
            interactions.Option(
                name="user",
                type=interactions.OptionType.USER,
                description="Indiquez l'utilisateur",
                required=True
            )
        ]
    )
    async def reset(ctx: interactions.CommandContext,user : interactions.User):
        rolestaff = data["rolestaff"]
        staff = False
        listrole = ctx.author.roles
        for i in listrole:
            if i in rolestaff:
                staff = True
                break
        if staff:
            member = interactions.Member(**await bot._http.get_member(data["guildId"],user.id),_client=bot._http)
            userid = user.id
            userid = int(userid)
            embed = interactions.Embed(title="Remise a Zéro de ta réputation",color=0xA37FC8,timestamp=datetime.datetime.now(),description="Ta réputation vient d'etre remise a zero")
            try:
                with open('./rep.json', 'r+') as f:
                    dataload = json.load(f)
                    userdata = dataload[user.id]
                    rep = userdata["rep"]
                    rep = int(rep)
                    rep = 0
                    userdata["rep"] = rep
                    f.seek(0)        # <--- should reset file position to the beginning.
                    json.dump(dataload, f, indent=4)
                    f.truncate()     # remove remaining part
                    embed.add_field(name="**Total de reputation :**", value=rep)
                    embed.add_field(name="**Rappel**",value="tu peux consulter à  tout moment le montant de points que tu as acquis en tapant la commande **+show**")
                    await ctx.send(content=f"l'utilisateur <@{userid}> a été remis a 0 de réputation",ephemeral=True)
                    await member.send(embeds=embed)
            except:
                await ctx.send(content=f"l'utilisateur <@{userid}> n'a pas de reputation",ephemeral=True)
        else:
            await ctx.send(content="Tu n'es pas membre du staff, pour executer cette commande",ephemeral=True)

    @bot.command(
        name="rep-",
        description="reset l'utilisateur au niveau de la reputation",
        scope=int(data["guildId"]),
        options=[
            interactions.Option(
                name="user",
                type=interactions.OptionType.USER,
                description="Indiquez l'utilisateur",
                required=True
            ),
            interactions.Option(
                name="number",
                type=interactions.OptionType.INTEGER,
                description="numbre a retirer",
                required=True
            ),
        ]
    )
    async def repmoins(ctx: interactions.CommandContext,user : interactions.User,number: int):
        rolestaff = data["rolestaff"]
        staff = False
        listrole = ctx.author.roles
        for i in listrole:
            if i in rolestaff:
                staff = True
                break
        if staff:
            if int(number):
                member = interactions.Member(**await bot._http.get_member(data["guildId"],user.id),_client=bot._http)
                userid = user.id
                userid = int(userid)
                useravatar = user.avatar
                try:
                    with open('./rep.json', 'r+') as f:
                        dataload = json.load(f)
                        userdata = dataload[user.id]
                        rep = userdata["rep"]
                        rep = int(rep)
                        rep -= number
                        userdata["rep"] = rep
                        embed = interactions.Embed(title="Ta réputation",color=0xA37FC8,timestamp=datetime.datetime.now(),description="Tu viens de perdre des points de réputation, suite a ton comportement")
                        embed.add_field(name="Nombre de réputation enlevé",value=number)
                        embed.add_field(name="Total de réputation",value=rep)
                        embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{userid}/{useravatar}.png?size=512")
                        await member.send(embeds=embed)
                        await ctx.send(content=f"{number} de réputation a été retirer a <@{userid}>",ephemeral=True)
                        f.seek(0)        
                        json.dump(dataload, f, indent=4)
                        f.truncate()    
                except:
                    await ctx.send(content=f"l'utilisateur <@{userid}> n'a pas de reputation",ephemeral=True)
            else:
                await ctx.send(content="Tu n'as pas mis un bon chiffre",ephemeral=True)
        else:
            await ctx.send(content="Tu n'es pas membre du staff, pour executer cette commande",ephemeral=True)
bot.start()