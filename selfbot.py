import discord
from discord.ext import commands
import asyncio
import requests
import json
import pypresence

try: # Ошибка врзникает если нету такой приложухи, нет инета, не включен дискорд. Этим я и пользуюсь
    statys = pypresence.Presence('765984319541477407') # Сюда пихаем циферки которые мы скопировали
    statys.connect() # Проверка на подключение
    connection = True # Это значит что с подключением все ок
    print('Все ок')
except Exception:
    connection = False # Это значит что все плохо с подрубом к дс
    print('Все плохо. Проблемы у тебя. Фикси сам')

statys.update(
    state = 'Взлом',
    details = 'Хмм...',
    start = None, # таймкод начала. можно вытащить из модуля time
    end = None, # тиаймкод конца. тоже есть в модуле time. про это я писать не буду. разберетесь сами
    large_image = 'hack', # Это название картинки которую вы хотите сделать большой
    large_text = 'hmm',
    small_image = 'hack2', # Это название картинки которую вы хотите сделать маленькой
    small_text = 'hmmm',
    party_id = 'secret', # айди комнаты с игроками. незнаю что оно делает но все можно посмотреть тут(см. скрин 3)
    party_size = [1, 2], # список с числами. первое - количество игроков в комнате. второе - максималка игроков в комнате.
    join = 'MTI4NzM0OjFpMmhuZToxMjMxMjM= ', # айди приглашения. тоже незнаю что оно делает
    spectate = 'ya.ochen.staralsa.postavte.laik.syda', # ади наблюдательного приглашения. беспонятия что оно делает
    match = 'neznau.chto.eto',
    instance = True # не ну тут реально не понимаю
    )

client = commands.Bot(command_prefix = 's>', self_bot = True)
prefix = client.command_prefix
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet2 = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
    '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
    '!': 'grey_exclamation',
    '?': 'grey_question',
    '#': 'hash',
    '*': 'asterisk'}
_title = ''

@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_message(msg):
    if msg.author.id == int(730666067474645103) and msg.content[:len(prefix)]==prefix:
        await msg.delete()
        await client.process_commands(msg)


@client.command()
async def big(ctx, *txt):
    txt = ctx.message.content[len(prefix)+4:]
    text = ''
    for char in txt:
        if char=='\n':
            text += '\n'
        elif char==' ':
            text += '      '
        elif char in alphabet:
            text += f':regional_indicator_{char}: '
        elif char in list(alphabet2.keys()):
            text += f':{alphabet2[char]}: '
    await ctx.send(text)

class token:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f'<Token name="{self.name}" value="{self.value}">'

class parser:
    def __init__(self, txt):
        self.txt = txt
        self.idx = -1
        self.currentChar = None
        self.tokenList = []
        self.next()
        self.makeTokens()

    def next(self):
        self.idx += 1
        if len(self.txt)>self.idx:
            self.currentChar = self.txt[self.idx]
        else:
            self.currentChar = None

    def makeTokens(self):
        while self.currentChar!=None:
            if self.currentChar == '-':
                self.makeArgumentName()
            elif self.currentChar == '"' or self.currentChar == "'":
                self.makeArgumentValue()

            self.next()

    def makeArgumentName(self):
        self.next()
        name = ''
        while self.currentChar!=None:
            if self.currentChar==' ':
                break
            name += self.currentChar
            self.next()
        self.tokenList.append(token('TT_ARGNAME', name))

    def makeArgumentValue(self):
        quote = self.currentChar
        self.next()
        value = ''
        while self.currentChar!=None:
            if self.currentChar==quote:
                break
            value += self.currentChar
            self.next()
        self.tokenList.append(token('TT_ARGVALUE', value))
def createEmbed(json):
    standart = {'t': '', 'd': '', 'url': '', 'img': '', 'author': '', 'f': '', 'fi': ''}
    standart.update(json)
    embed = discord.Embed(title=standart['title'], description=standart['desc'], url=standart['url'])
    embed.set_image(url=standart['image'])
    embed.set_author(name=standart['author'])
    embed.set_footer(text=standart['footer'], icon_url=standart['footerImage'])
    return embed

@client.command()
async def embed(ctx, *txt):
    txt = ctx.message.content[len(prefix)+6:]
    pars = parser(txt)
    tokens = pars.tokenList
    args = {}

    for i in range(0, len(tokens), 2):
        try:
            name = tokens[i]
            value = tokens[i+1]
            if name.name=='TT_ARGNAME' and value.name=='TT_ARGVALUE':
                args.update([(name.value, value.value)])
        except: pass
    await ctx.send(embed = createEmbed(args))


client.run("тут токен", bot=False)
