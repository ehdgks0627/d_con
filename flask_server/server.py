import httplib2
import os
import json
import random
from flask import Flask, render_template, url_for, session

profile_list = ['levelFrame', 'playtime_quick', 'playtime_competitive', 'avatar', 'username', 'star', 'level', 'games_quick_wins', 'games_competitive_played', 'games_competitive_lost', 'games_competitive_wins', 'competitive_rank_img', 'competitive_rank']
quick_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadsDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'ReconAssists']
competitive_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'GamesPlayed', 'GamesTied', 'GamesLost']
achievements_list = ['name', 'finished', 'image', 'description', 'category']
hero_list = ['Ana', 'Bastion', 'DVa', 'Genji', 'Hanzo', 'Junkrat', 'Lucio', 'Mccree', 'Mei', 'Mercy', 'Pharah', 'Reaper', 'Reinhardt', 'Roadhog', 'Soldier76', 'Symmetra', 'Torbjoern', 'Tracer', 'Widowmaker', 'Winston', 'Zarya', 'Zenyatta']
user_no = 1
background_count = 7

app = Flask(__name__)
app.secret_key = 'this isssssssssssss secret!'

server_domain = '0.0.0.0'
server_port = 5000

def api_profile(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/profile'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        dic = {}
        dic['levelFrame'] = j['data']['levelFrame']
        dic['playtime_quick'] = j['data']['playtime']['quick']
        dic['playtime_competitive'] = j['data']['playtime']['competitive']
        dic['avatar'] = j['data']['avatar']
        dic['username'] = j['data']['username']
        dic['star'] = j['data']['star']
        dic['level'] = str(j['data']['level'])
        dic['games_quick_wins'] = j['data']['games']['quick']['wins']
        dic['games_competitive_played'] = j['data']['games']['competitive']['played']
        dic['games_competitive_lost'] = j['data']['games']['competitive']['lost']
        dic['games_competitive_wins'] = j['data']['games']['competitive']['wins']
        dic['competitive_rank_img'] = j['data']['competitive']['rank_img']
        dic['competitive_rank'] = j['data']['competitive']['rank']
        return dic
    except:
        return False

def api_quick_allheros(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/quick-play/allHeroes/'%(name), 'GET')
        return json.loads(content.decode('utf-8'))
    except:
        pass

def api_competitive_allheros(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/allHeroes/'%(name), 'GET')
        return json.loads(content.decode('utf-8'))
    except:
        pass

def api_achievements(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/achievements'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j['achievements']
    except:
        pass

def api_quick_heros(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/quick-play/heroes'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j
    except:
        pass

def api_competitive_heros(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/heroes'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j
    except:
        pass

def api_quick_hero(name, hero):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/hero/%s/'%(name,hero), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j
    except:
        pass

def api_competitive_hero(name, hero):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/hero/%s/'%(name,hero), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j
    except:
        pass

'''
GET /{platform}/{region}/{tag}/{mode}/hero/{heroes}/ 대상으로 알고리즘 적용
heros 대상으로 전체적인 챔피언 정보 보여주기
'''

@app.before_request
def before_request():
    try:
        global user_no
        if 'session' in session and 'user-id' in session:
            pass
        else:
            session['session'] = os.urandom(32)
            session['username'] = 'user' + str(user_no)
            user_no += 1
    except:
        pass

@app.route('/')
def chatting():
    try:
        return render_template('index.html',random=random.randint(1,background_count));
    except:
        pass

@app.route('/info/<name>/')
def info(name):
    name = name.replace('#','-')
    profile = api_profile(name)
    if profile == False:
        return 'no username'
    quick_heros = api_quick_heros(name)
    try:
        return render_template('info.html',pro=profile,qui=quick_heros)
    except:
        pass

@app.route('/heros/<name>/')
def heros(name):
    try:
        name = name.replace('#','-')
        profile = api_profile(name)
        if profile == False:
            return 'no username'
        quick_heros = api_quick_heros(name)
        competitive_heros = api_competitive_heros(name)
        return render_template('heros.html',pro=profile,qui=quick_heros)
    except:
        pass

@app.route('/allheros/<name>/')
def allheros(name):
    try:
        name = name.replace('#','-')
        profile = api_profile(name)
        if profile == False:
            return 'no username'
        quick_allheors = api_quick_allheros(name)
        competitive_allheros = api_competitive_allheros(name)
        return render_template('allheros.html',qui=quick_allheors,com=competitive_allheros)
    except:
        pass

@app.route('/achievements/<name>/')
def achievements(name):
    try:
        name = name.replace('#','-')
        profile = api_profile(name)
        if profile == False:
            return 'no username'
        achievements = api_achievements(name)
        return render_template('achievements.html',ach=achievements)
    except:
        pass

@app.route('/hero/<name>/<hero>/')
def hero(name,hero):
    try:
        name = name.replace('#','-')
        profile = api_profile(name)
        if profile == False:
            return 'no username'
        hero_data = api_competitive_hero(name,hero)
        return render_template('hero.html',her=list(hero_data.items())[0][1])
    except:
        pass

@app.route('/chart/')
def chart():
    try:
        return render_template('chart.html')
    except:
        pass


if __name__ == '__main__':
    app.run(host=server_domain, port=server_port, debug=True)
