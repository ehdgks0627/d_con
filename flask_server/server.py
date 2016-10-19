import httplib2
import os
import json
from flask import Flask, render_template, url_for, session

profile_list = ['levelFrame', 'playtime_quick', 'playtime_competitive', 'avatar', 'username', 'star', 'level', 'games_quick_wins', 'games_competitive_played', 'games_competitive_lost', 'games_competitive_wins', 'competitive_rank_img', 'competitive_rank']
quick_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadsDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'ReconAssists']
competitive_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'GamesPlayed', 'GamesTied', 'GamesLost']
achievements_list = ['name', 'finished', 'image', 'description', 'category']
hero_list = []
user_no = 1

app = Flask(__name__)
app.secret_key = 'secret'

server_domain = '192.168.43.230'
server_port = 5000

def api_profile(name):
    h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/profile'%(name), 'GET')
    j = json.loads(content.decode('utf-8'))
    try:
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
    except:
        return False
    return dic

def api_quick_allheros(name):
    h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/quick-play/allHeroes/'%(name), 'GET')
    return json.loads(content.decode('utf-8'))

def api_competitive_allheros(name):
    h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive-play/allHeroes/'%(name), 'GET')
    return json.loads(content.decode('utf-8'))

def api_achievements(name):
    h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/achievements'%(name), 'GET')
    j = json.loads(content.decode('utf-8'))
    '''
    이미지는 image에서 받아옴
    finished 가 true면 이미지를 진하게 표시
    마우스 오버시 name 표시
    '''
    return j['achievements']

@app.before_request
def before_request():
    global user_no
    if 'session' in session and 'user-id' in session:
        pass
    else:
        session['session'] = os.urandom(32) #make session id
        session['username'] = 'user' + str(user_no)
        user_no += 1

@app.route('/')
@app.route('/main/')
def chatting():
    return render_template('index.html')

@app.route('/info/<name>')
def hello(name):
    name = name.replace('#','-')
    profile = api_profile(name)
    if profile == False:
        return 'no username'
    quick_allheors = api_quick_allheros(name)
    competitive = api_competitive_allheros(name)
    achievements = api_achievements(name)

    return 'complete'

if __name__ == '__main__':
    app.run(host=server_domain, port=server_port, debug=True)
