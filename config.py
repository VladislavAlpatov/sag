
class Bot_info:
    token = 'NzA5Njk4NTk3NDE1MDI2NzA3.XrpsyA.2meGa2Q39zk_2Qo54kA2XRZEN0o'
    game = '/help'
    heads = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}


class Nullserver:
    id = 711919810434433105


class Messages:

    invite = '''
    **You can add me on your server by this link:**
`https://discord.com/api/oauth2/authorize?client_id=709698597415026707&permissions=387136&scope=bot`'''


class Cathook:
    features = [
        'Aimbot:Aimbot is that tool which automatically aims and shoots.All classes can use aimbot with guns or melees!',
        'Backtracking: (Broken right now, do not use, thanks)',
        'Autoshot: Automatically Shoot while aiming with aimbot.',
        'Silent: Cathook shots without turning to target.',
        'FOV: max FOV to shoot in',
        'FOV circle: draw that circle where aimbot Shoots enemies. (When Priority mode is FOV.)',
        'Zoomed only: Cathook shots only when zoomed in.',
        "Auto spin-up: Heavy's minigun will be automaticly spinned-up (before shooting.)",
        "Auto unzoom: when Cathook doesn't see any targets it auto unzooms the sniper's scope.",
        "Autozoom: before aiming sniper's scope will be zoomed in.",
        'Hitbox: Aim at the selected hitbox.',
        'Hitbox mode: Auto Prefers Head, if no Head is visible it aims at the spine hitboxes, Static: aiming only at the selected Hitbox, Auto Closest: Shoot the hitbox closest to you.',
        'Lock target: Aims at the same target until it turns invalid.',
        'Miss chance: Miss chance as Decimal, 10 = 10%, 100 = 100%.',
        'Multipoint: Try hitting other points than the center of the hitboxes if possible',
        'Priority mode: No explanation needed.',
        'Max range: Maximum aimbot range.',
        'Enable projectile aimbot: duh.',
        'Extrapolate: Take ping into compensation (Not recommended).',
        'Slow aimbot: Slow aimbot option makes you turn slower and aims for a more legit feel (also combine with triggerbot and disable autoshoot to hit better).',
        'Auto Detonator, Auto Backstab: Automatically blows up the Detonator projectile when near enemies.',
        'Auto Reflect: A tool for Pyros. Airblast will be automated with the use of Auto Ref',
        'Auto Sticky: matically detonates stickies.',
        '#nohomo: NO HOMO HERE BOY!!!'
    ]
    download = 'https://github.com/nullworks/cathook'
    grafana = 'https://accgen.cathook.club/grafana/d/BKdne-tWz/accgen-core-services?orgId=1&refresh=10s'

    """
    @bot.event
async def on_message(message):
    await bot.process_commands(message)
    author = message.author
    msg = message.content
    msg = msg.replace('@everyone', 'everyone')
    if str(author) == 'cat-bot#4210' or message.guild.id == 665856387439656972:
        pass
    else:
        channel = bot.get_channel(config.Nullserver.id)
        await channel.send(f'<{message.guild.name}>  <{message.channel.name}> **{author}** :{msg} ')"""
