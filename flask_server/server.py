import httplib2
import os
import json
import random
import time
import sys
from multiprocessing import Process, Queue, Manager, Value
from flask import Flask, render_template, url_for, session
from pprint import pprint

profile_list = ['levelFrame', 'playtime_quick', 'playtime_competitive', 'avatar', 'username', 'star', 'level', 'games_quick_wins', 'games_competitive_played', 'games_competitive_lost', 'games_competitive_wins', 'competitive_rank_img', 'competitive_rank']
quick_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadsDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'ReconAssists']
competitive_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'GamesPlayed', 'GamesTied', 'GamesLost']
achievements_list = ['name', 'finished', 'image', 'description', 'category']
hero_list = ['Ana', 'Bastion', 'DVa', 'Genji', 'Hanzo', 'Junkrat', 'Lucio', 'Mccree', 'Mei', 'Mercy', 'Pharah', 'Reaper', 'Reinhardt', 'Roadhog', 'Soldier76', 'Symmetra', 'Torbjoern', 'Tracer', 'Widowmaker', 'Winston', 'Zarya', 'Zenyatta']
profiles = {}
quick_heroses = {}
cookies = {}
hero_datas = {}
user_no = 1
background_count = 7
request_count = 0

app = Flask(__name__)
app.secret_key = 'this isssssssssssss secret!'

server_domain = '0.0.0.0'
server_port = 5000

def api_profile(name,d,count,ident):
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
        d[ident] = j
        count.value += 1
        return True
    except:
        return False

def api_quick_allheros(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/quick-play/allHeroes/'%(name), 'GET')
        return False
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

def api_quick_heros(name,d,count,ident):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/quick-play/heroes'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        d[ident] = j
        count.value += 1
        return True
    except:
        return False

def api_competitive_heros(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/heroes'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j
    except:
        pass

def api_quick_hero(name, hero, d,count):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/hero/%s/'%(name,hero), 'GET')
        j = json.loads(content.decode('utf-8'))
        d[hero] = j
        count.value += 1
        return True
    except:
        return False

def api_competitive_hero(name, hero):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/hero/%s/'%(name,hero), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j
    except:
        pass

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
    global request_count
    request_count += 1
    print(request_count)
    #try:
    if True:
        name = name.replace('#','-')
        if cookies.get(name) != None and (time.time() - cookies.get(name)) < 600:
            profile = profiles[name]
            quick_heros = quick_heroses[name]
            d = hero_datas[name]
        else:
            # Multi Processing...
            manager = Manager()
            d = manager.dict()
            count = Value('i',0)
            p = {}
            p[1] = Process(target=api_profile,args=(name,d,count,'1'))
            p[2] = Process(target=api_quick_heros,args=(name,d,count,'2'))
            p[1].start()
            p[2].start()
            p[1].join()
            p[2].join()
            profiles[name] = d['1']
            quick_heroses[name] = d['2']
            d.pop('1')
            d.pop('2')
            for h in hero_list:
                p[name] = Process(target=api_quick_hero,args=(name,h,d,count))
                p[name].start()
            for h in hero_list:
                p[name].join()
            # Multri Processing End...
            profile = profiles[name]
            quick_heros = quick_heroses[name]
            if profile == False:
                return "<html><head><script>alert('no username');document.location='/'</script></head><body></body></html>"
            cookies[name] = time.time()
            hero_datas[name] = d
        return render_template('info.html',random=random.randint(1,background_count),pro=profile['data'],qui=quick_heros,infos=[profile['data']['competitive']['rank_img'],profile['data']['level'],profile['data']['competitive']['rank'],profile['data']['username'],profile['data']['avatar']],hero_data=d)
    #except:
    #    return "<html><head><script>alert('no username');document.location='/'</script></head><body></body></html>"

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
