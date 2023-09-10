import discord
from discord.ext import commands
import requests
from discord.ext.commands import *
from random import randint

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot("$", intents=intents)


API_TOKEN = ''
BOT_TOKEN = ''


def busca(num):
    ranges = [(501, 524, [4, 500]), (525, 549, [6, 524]), (550, 574, [8, 549]), (575, 599, [10, 574]),
              (600, 624, [12, 599]), (625, 649, [14, 624]), (650, 674, [16, 649]), (675, 699, [18, 674]),
              (700, 724, [20, 699]), (725, 749, [22, 724]), (750, 774, [24, 749]), (775, 799, [26, 774]),
              (800, 824, [28, 799]), (825, 849, [30, 824]), (850, 874, [32, 849]), (875, 899, [34, 874]),
              (900, 924, [36, 899]), (925, 949, [38, 924]), (950, 974, [40, 949]), (975, 999, [42, 974]),
              (1000, 1049, [44, 999]), (1050, 1099, [46, 1049]), (1100, 1149, [48, 1099]), (1150, 1199, [50, 1149]),
              (1200, 1249, [52, 1199]), (1250, 1299, [54, 1249]), (1300, 1349, [56, 1299]), (1350, 1399, [58, 1349]),
              (1400, 1449, [60, 1399]), (1450, 1499, [62, 1449]), (1500, 200000, [64, 1499])]
    for r in ranges:
        if r[0] <= num <= r[1]:
            return r[2]
    return 0


def request(tag_aux):
    return requests.get(f'https://api.brawlstars.com/v1/players/%23{tag_aux}',
                        headers={'Authorization': f'Bearer {API_TOKEN}'})


def role(ctx, id_role):
    return discord.utils.get(client.get_guild(ctx.guild.id).roles, id=id_role)


@client.command(name="status")
async def player_info(ctx, tag):
    try:
        
        try:
            brawler = request(tag).json()
            response = f"""
Nome: {brawler['name']}
Trofeus: {brawler['trophies']}
Máximo de troféus: {brawler['highestTrophies']}
Nível: {brawler['expLevel']}
Total de pontos de experiência: {brawler['expPoints']}
3v3: {brawler['3vs3Victories']}
Solo: {brawler['soloVictories']}
Duo: {brawler['duoVictories']}
Quantidade de brawlers: {len(brawler['brawlers'])}
Tag: {brawler['tag'].upper()}
Clube: {brawler['club']['name'] if brawler['club'] else 'Sem clube'}"""
            await ctx.send(response)
        except Exception as e:
            await ctx.send("Player nâo encontrado")
    except:
        pass


@client.command(name="foto")
async def tag(ctx, tamanho):
    try:
        tamanho = str(tamanho).split("x")
        url = f"http://picsum.photos/{tamanho[0]}/{tamanho[1]}"
        embed = discord.Embed(
            title="Resultado da busca de imagem",
            color=0x0000FF,
        )
        embed.set_author(name=client.user.name)
        embed.add_field(name="Parâmetros", value=f"{tamanho[0]}x{tamanho[1]}")
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    except:
        pass


@client.command(name="frase")
async def frase(ctx, *, f):
    tema = f.split(" ")
    r = requests.get(f'https://pensador-api.vercel.app/?term={"+".join(tema)}&max=12').json()
    ra = randint(0, 12)
    em = discord.Embed(title=r['frases'][ra]['autor'], description=r['frases'][ra]['texto'])
    await ctx.send(embed=em)


@client.command(name="vice_presidente?")
async def vice_presidente(ctx):
    if role(ctx, 1038265309255176252) in ctx.author.roles:
        await ctx.send("SIMM")
    else:
        await ctx.send("NAAAO")




@client.command(name="brawler")
async def brawler_info(ctx, tag, cmd):
    try:
        info = request(tag).json()
        for brawler in info['brawlers']:
            if str(brawler['name']).upper() == str(cmd).upper():
                response = f"""
Nome: {brawler['name']}
Trofeus: {brawler['trophies']}
Poder: {brawler['power']}
Classe: {brawler['rank']}
Troféus máximo: {brawler['highestTrophies']}
Engrenagens: {", ".join(list(map(lambda dado: str(dado["name"]).capitalize(), brawler['gears'])))}
Poderes de estrela: {", ".join(list(map(lambda dado: str(dado["name"]).capitalize(), brawler['starPowers'])))}
Acessórios: {", ".join(list(map(lambda dado: str(dado["name"]).capitalize(), brawler['gadgets'])))}
    """
                await ctx.send(response)
                return
        await ctx.send("Brawler ou player não encontrado!")
    except:
        pass


@client.command(name="cargo")
async def cargo(ctx, tag):
    try:
        if role(ctx, 1038265309255176252) in ctx.author.roles or role(ctx,
                                                                      1038263912346427493) in ctx.author.roles or role(
                ctx, 1038262712205049948) in ctx.author.roles:
            await ctx.send("Voce ja tem um cargo, não é possível obter dois cargos de patamares")
            return
        info = request(tag).json()
        club = requests.get(f'https://api.brawlstars.com/v1/clubs/%23{str(info["club"]["tag"]).replace("#", "")}',
                            headers={'Authorization': f'Bearer {API_TOKEN}'})
        club = club.json()
        for member in club['members']:
            if str(tag).upper() in str(member['tag']):
                if member['role'] == 'vicePresident':
                    await ctx.author.add_roles(
                        discord.utils.get(client.get_guild(ctx.guild.id).roles, id=1038265309255176252))
                    await ctx.send(f'Você recebeu o cargo no servidor de vice presidente')
                    return
                if member['role'] == 'senior':
                    await ctx.author.add_roles(
                        discord.utils.get(client.get_guild(ctx.guild.id).roles, id=1038263912346427493))
                    await ctx.send(f'Você recebeu o cargo no servidor de ancião')
                    return
                if member['role'] == 'member':
                    await ctx.author.add_roles(
                        discord.utils.get(client.get_guild(ctx.guild.id).roles, id=1038262712205049948))
                    await ctx.send(f'Você recebeu o cargo no servidor de membro')
                    return
        await ctx.send("Tag não encontrada")
    except:
        pass


@client.command(name="bitcoin")
async def btc(ctx):
    info = requests.get('https://economia.awesomeapi.com.br/last/BTC-BRL').json()
    await ctx.send(f"valor do bitcoin: {info['BTCBRL']['bid']}")


@client.command(name="dolar")
async def dol(ctx):
    info = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL').json()
    await ctx.send(f"valor do dolar: {info['USDBRL']['bid']}")


@client.command(name="maxuel")
async def max_recorde_all(ctx, tag):
    try:
        
        info = request(tag).json()
        cont = 0
        for brawler in info['brawlers']:
            cont += brawler['highestTrophies']
        await ctx.send(f'Caso todos os brawlers estivessem no recorde de trofeus: {cont}')
    except:
        pass


@client.command(name="oi")
async def oi(ctx):
    await ctx.author.send(f"Fala ae {ctx.author.name}, um oi bonitinho direto no seu PV")


@client.command(name="after_v0")
async def trofeus_apos_termino(ctx, tag):
    try:
        
        info = request(tag).json()
        cont = 0
        for brawler in info['brawlers']:
            trof = busca(brawler['trophies'])
            if trof == 0:
                cont += brawler['trophies']
            else:
                cont += trof[1]
        await ctx.send(cont)
    except:
        pass


@client.command(name="after_explicado_v0")
async def after_explicado(ctx, tag):
    try:
        
        info = request(tag).json()
        brawl = {}
        for brawler in info['brawlers']:
            trof = busca(brawler['trophies'])
            if trof == 0:
                pass
            else:
                brawl[brawler['name']] = brawler['trophies'] - trof[1]
        brawl = dict(sorted(brawl.items(), key=lambda item: item[1], reverse=True))
        await ctx.send(brawl)
    except:
        pass


@client.command(name="after")
async def trofeus_apos_termino(ctx, tag):
    try:
        
        cont = 0
        info = request(tag).json()
        brawl, brawlers = {}, {}
        for brawler in info['brawlers']:
            brawl[brawler['name']] = brawler['trophies']
        brawl = dict(sorted(brawl.items(), key=lambda item: item[1], reverse=True))

        for c, v in brawl.items():
            if cont < 20:
                trof = busca(v)
                if trof == 0:
                    pass
                else:
                    brawlers[c] = trof[1]
                cont += 1
            else:
                brawlers[c] = v
        trof = 0
        for t in brawlers.values():
            trof += t
        await ctx.send(trof)
    except:
        pass


@client.command(name="after_info")
async def after_info(ctx, tag):
    try:
        
        cont = 0
        info = request(tag).json()
        brawl, brawlers = {}, {}
        for brawler in info['brawlers']:
            brawl[brawler['name']] = brawler['trophies']
        brawl = dict(sorted(brawl.items(), key=lambda item: item[1], reverse=True))

        for c, v in brawl.items():
            if cont < 20:
                trof = busca(v)
                if trof == 0:
                    pass
                else:
                    brawlers[c] = v - trof[1]
                cont += 1
        brawlers = dict(sorted(brawlers.items(), key=lambda item: item[1], reverse=True))
        trof = 0
        for t in brawlers.values():
            trof += t
        await ctx.send(brawlers)
    except:
        pass


@client.command(name="bling_old")
async def bling(ctx, tag):
    try:
        
        info = request(tag).json()
        cont = 0
        for brawler in info['brawlers']:
            trof = busca(brawler['trophies'])
            if trof == 0:
                continue
            else:
                cont += trof[0]

        await ctx.send(cont)
    except:
        pass


@client.command(name="bling")
async def bling(ctx, tag):
    try:
        
        bling, cont = 0, 0
        info = request(tag).json()
        brawl = {}
        for brawler in info['brawlers']:
            trof = busca(brawler['trophies'])
            if trof == 0:
                continue
            else:
                brawl[brawler['name']] = trof[0]
            brawl = dict(sorted(brawl.items(), key=lambda item: item[1], reverse=True))
        for c, v in brawl.items():
            if cont < 20:
                bling += v
                cont += 1

        await ctx.send(bling)
    except:
        pass


@client.command(name="bling_info")
async def bling_info(ctx, tag):
    try:
        
        info = request(tag).json()
        cont = ""
        for brawler in info['brawlers']:
            trof = busca(brawler['trophies'])
            if trof == 0:
                continue
            else:
                cont = cont + f"{brawler['name']}-> {trof[0]} blings\n"
        await ctx.send(cont)
    except:
        pass


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Favor enviar argumentos restantes do comando")
    if isinstance(error, CommandNotFound):
        await ctx.send("O comando não existe")
    else:
        raise error


@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        await guild.system_channel.send(f'{member.mention} acabou de entrar no {guild.name}')


@client.command("id")
async def id(ctx):
    await ctx.send(ctx.author.id)  # 456498329032065037




client.remove_command("help")


@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='Help', description=f'Digite !help junto com o comando desejado para as explicações')
    em.add_field(name='brawler', value='todas as informações sobre um brawler do jogador', inline=False)
    em.add_field(name='status', value='informaçoes sobre o jogador', inline=False)
    em.add_field(name='cadastrar_tag', value='Cadastra um apelido para uma tag para facilitar nas buscas posteriores',
                 inline=False)
    em.add_field(name='lista', value='Lista todos os apelidos para uma tag especifica', inline=False)
    em.add_field(name='foto', value='foto aleatorio com tamanho especificado', inline=False)
    em.add_field(name='cargo', value='da a um jogador o cargo de acordo com a tag no clã', inline=False)
    em.add_field(name='dolar', value='valor exato do dolar no momemto', inline=False)
    em.add_field(name='bitcoin', value='valor exato do bitcoin no momemto', inline=False)
    em.add_field(name='maxuel', value='Suposição, quantidade de trofeus caso você estivesse com todos os brawlers no '
                                      'recorde de trofeus', inline=False)
    em.add_field(name='after', value='trofeus apos termino da temporada', inline=False)
    em.add_field(name='after_info', value='trofeus que perderá com cada brawler', inline=False)
    em.add_field(name='bling', value='blings obtidos apos termino da temporada', inline=False)
    em.add_field(name='bling_info', value='trofeus que obterá com cada brawler', inline=False)
    await ctx.send(embed=em)


@help.command()
async def brawler(ctx):
    em = discord.Embed(title='brawler', description=' $brawler <tag> <nome brawler>')
    em.add_field(name='Ex: $brawler #vlqpvpy stu', value="""Nome: STU
Trofeus: 1422
Poder: 11
Classe: 35
Troféus máximo: 1422
Engrenagens: Damage, Shield
Poderes de estrela: Zero drag, Gaso-heal
Acessórios: Speed zone, Breakthrough""")
    await ctx.send(embed=em)


@help.command()
async def status(ctx):
    em = discord.Embed(title='status', description=' $status <tag>')
    em.add_field(name='Ex: $status #jlgyl8lp', value="""Nome: CO | ⛩️Sun Tzu⛩
Trofeus: 33023
Máximo de troféus: 33041
Nível: 230
Total de pontos de experiencia: 271517
3v3: 6326
Solo: 2049
Duo: 4209
Quantidade de brawlers: 59
Tag: #jlgyl8lp
Clube: Comando""")
    await ctx.send(embed=em)


@help.command()
async def cargo(ctx):
    em = discord.Embed(title='cargo', description=' $cargo <sua tag no clube>')
    em.add_field(name='Ex: $cargo #jlgyl8lp', value="""
Você recebeu o cargo no servidor de vice presidente
""")
    em.add_field(name='OBS: ', value="""
Só é possível receber um cargo de patamar
""")
    await ctx.send(embed=em)


@help.command()
async def cadastrar_tag(ctx):
    em = discord.Embed(title='cadastrar_tag', description=' $cadastrar_tag <apelido> <tag>')
    em.add_field(name='$cadastrar_tag pablao jlgyl8lp', value="""
""")
    await ctx.send(embed=em)


@help.command()
async def foto(ctx):
    em = discord.Embed(title='foto', description=' $foto <largura>x<altura>')
    em.add_field(name='Ex: $foto 500x500', value="""
uma foto no formato especificado
""")
    await ctx.send(embed=em)


@help.command()
async def after(ctx):
    em = discord.Embed(title='after', description=' $after <tag>')
    em.add_field(name='Ex: $after #jlgyl8lp', value="""
10000
""")
    await ctx.send(embed=em)


@help.command()
async def bling(ctx):
    em = discord.Embed(title='bling', description=' $bling <tag>')
    em.add_field(name='Ex: $bling #jlgyl8lp', value="""
200
""")
    await ctx.send(embed=em)


client.run(BOT_TOKEN)
