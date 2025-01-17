import json
import logging
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import team as _team
import league as _league
import player as _player
import event as _event
import user as _user
import livescores
import tableentry
import datetime as _datetime
from utils import util as _util


API_BASE_URL = 'http://www.thesportsdb.com/api/v1/json'


class Api:
    def __init__(self, key=None):
        global API_KEY
        API_KEY = key
        if API_KEY != None and type(API_KEY) == str:
            logging.info(
                f'[TheSportsDB] Module initiated with API key {str(API_KEY)}')
        else:
            logging.error("[TheSportsDB] API Key is not valid")

    class Lookups:
        def Team(self, teamid=None, leagueid=None):
            teamlist = []
            if teamid or leagueid:
                if teamid and not leagueid:
                    url = f"{API_BASE_URL}/{API_KEY}/lookupteam.php?id={str(teamid)}"
                elif leagueid and not teamid:
                    url = f"{API_BASE_URL}/{API_KEY}/lookup_all_teams.php?id={str(leagueid)}"
                else:
                    logging.error("[TheSportsDB] Invalid parameters")
                    return teamlist
                data = json.load(urllib.request.urlopen(url))
                teams = data["teams"]
                if teams:
                    for tm in teams:
                        teamlist.append(_team.as_team(tm))
            else:
                logging.error(
                    "[TheSportsDB] teamid or leagueid must be provided")
            return teamlist

        def League(self, leagueid=None):
            leaguelist = []
            if leagueid:
                url = f"{API_BASE_URL}/{API_KEY}/lookupleague.php?id={str(leagueid)}"
                data = json.load(urllib.request.urlopen(url))
                leagues = data["leagues"]
                if leagues:
                    for lg in leagues:
                        leaguelist.append(_league.as_league(lg))
            else:
                logging.log("[TheSportsDB] leagueid must be provided", )
            return leaguelist

        def Player(self, playerid=None, teamid=None):
            playerlist = []
            if playerid or teamid:
                if playerid and not teamid:
                    url = f"{API_BASE_URL}/{API_KEY}/lookupplayer.php?id={str(playerid)}"
                    key = "players"
                elif teamid and not playerid:
                    url = f"{API_BASE_URL}/{API_KEY}/lookup_all_players.php?id={str(teamid)}"
                    key = "player"
                else:
                    logging.log("[TheSportsDB] Invalid parameters", )
                    return playerlist
                data = json.load(urllib.request.urlopen(url))
                players = data[key]
                if players:
                    for pl in players:
                        playerlist.append(_player.as_player(pl))
            else:
                logging.log(
                    "[TheSportsDB] playerid or teamid must be provided", )
            return playerlist

        def Event(self, eventid=None):
            eventlist = []
            if eventid:
                url = f"{API_BASE_URL}/{API_KEY}/lookupevent.php?id={str(eventid)}"
                data = json.load(urllib.request.urlopen(url))
                events = data["events"]
                if events:
                    for ev in events:
                        eventlist.append(_event.as_event(ev))
            else:
                logging.log("[TheSportsDB] eventid must be provided", )
            return eventlist

        def Table(self, leagueid=None, season=None, objects=False):
            table = []
            if leagueid:
                if season:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/lookuptable.php?l={str(leagueid)}&s={str(season)}"
                    )
                else:
                    url = f"{API_BASE_URL}/{API_KEY}/lookuptable.php?l={str(leagueid)}"
                    if objects:
                        teams_in_league = self.Team(leagueid=leagueid)
                data = json.load(urllib.request.urlopen(url))
                entries = data["table"]
                if entries:
                    for entry in entries:
                        tentry = tableentry.as_tableentry(entry)
                        if objects:
                            if not season:
                                for team in teams_in_league:
                                    if team.idTeam == tentry.teamid:
                                        tentry.setTeamObject(team)
                            else:
                                team_id = tentry.teamid
                                tentry.setTeamObject(self.Team(team_id)[0])
                        table.append(tentry)
            else:
                logging.log("[TheSportsDB] leagueid must be provided", )
            return table

        def Seasons(self, leagueid=None):
            seasonlist = []
            if leagueid:
                url = f"{API_BASE_URL}/{API_KEY}/lookupleague.php?id={str(leagueid)}&s=all"
                data = json.load(urllib.request.urlopen(url))
                entries = data["leagues"]
                if entries:
                    for entry in entries:
                        seasonlist.append(entry["strSeason"])
            else:
                logging.log("[TheSportsDB] leagueid must be provided", )
            return seasonlist

    class Search:
        def Teams(self, team=None, sport=None, country=None, league=None):
            teamlist = []
            if team or sport or country or league:
                if team and not sport and not country and not league:
                    url = f"{API_BASE_URL}/{API_KEY}/searchteams.php?t={urllib.parse.quote(team)}"
                elif not team and league and not sport and not country:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/search_all_teams.php?l={urllib.parse.quote(league)}"
                    )
                elif not team and not league and sport and country:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/search_all_teams.php?s={urllib.parse.quote(sport)}&c={urllib.parse.quote(country)}"
                    )
                else:
                    url = None
                if url:
                    data = json.load(urllib.request.urlopen(url))
                    teams = data["teams"]
                    if teams:
                        for tm in teams:
                            teamlist.append(_team.as_team(tm))
                else:
                    logging.log("[TheSportsDB] Invalid Parameters", )
            else:
                logging.log(
                    "[TheSportsDB] team,sport,country or league must be provided",
                )
            return teamlist

        def Players(self, team=None, player=None):
            playerlist = []
            if team or player:
                if team and not player:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/searchplayers.php?t={urllib.parse.quote(team)}"
                    )
                elif not team and player:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/searchplayers.php?p={urllib.parse.quote(player)}"
                    )
                else:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/searchplayers.php?t={urllib.parse.quote(team)}&p={urllib.parse.quote(player)}"
                    )
                data = json.load(urllib.request.urlopen(url))
                players = data["player"]
                if players:
                    for pl in players:
                        playerlist.append(_player.as_player(pl))
            else:
                logging.log("[TheSportsDB] team or player must be provided", )
            return playerlist

        def Events(self, event=None, filename=None, season=None):
            eventlist = []
            if event or season or filename:
                if event and not season and not filename:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/searchevents.php?e={str(event).replace(' ', '_')}"
                    )
                elif event and season:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/searchevents.php?e={str(event).replace(' ', '_')}&s={str(season)}"
                    )
                elif filename:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/searchfilename.php?e={str(filename).replace(' ', '_')}"
                    )
                else:
                    url = ""
                if url:
                    data = json.load(urllib.request.urlopen(url))
                    events = data["event"]
                    if events:
                        for ev in events:
                            eventlist.append(_event.as_event(ev))
            else:
                logging.log(
                    "[TheSportsDB] event and season or filename must be provided",
                )
            return eventlist

        def Leagues(self, country=None, sport=None):
            leaguelist = []
            if country or sport:
                if country and not sport:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/search_all_leagues.php?c={urllib.parse.quote(country)}"
                    )
                elif not country and sport:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/search_all_leagues.php?s={urllib.parse.quote(sport)}"
                    )
                else:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/search_all_leagues.php?s={urllib.parse.quote(sport)}&c={urllib.parse.quote(country)}"
                    )
                data = json.load(urllib.request.urlopen(url))
                leagues = data["countrys"]
                if leagues:
                    for lg in leagues:
                        leaguelist.append(_league.as_league(lg))
            else:
                logging.log(
                    "[TheSportsDB] country or league must be provided", )
            return leaguelist

        def Loves(self, user=None, objects=False):
            if user:
                userobj = _user.User()
                userobj.setUsername(user)
                playerlist = []
                teamlist = []
                leaguelist = []
                eventlist = []
                url = f"{API_BASE_URL}/{API_KEY}/searchloves.php?u={str(user)}"
                data = json.load(urllib.request.urlopen(url))
                edits = data["players"]
                if edits:
                    for edit in edits:
                        if edit["idTeam"]: teamlist.append(edit["idTeam"])
                        if edit["idPlayer"]:
                            playerlist.append(edit["idPlayer"])
                        if edit["idLeague"]:
                            leaguelist.append(edit["idLeague"])
                        if edit["idEvent"]: eventlist.append(edit["idEvent"])
                    if objects:
                        _teamlist = []
                        _playerlist = []
                        _eventlist = []
                        _leaguelist = []
                        if teamlist:
                            for tmid in teamlist:
                                try:
                                    _teamlist.append(
                                        Api(API_KEY).Lookups().Team(
                                            teamid=tmid)[0])
                                except:
                                    pass
                        teamlist = _teamlist
                        del _teamlist
                        if playerlist:
                            for plid in playerlist:
                                try:
                                    _playerlist.append(
                                        Api(API_KEY).Lookups().Player(
                                            playerid=plid)[0])
                                except:
                                    pass
                        playerlist = _playerlist
                        del _playerlist
                        if leaguelist:
                            for lgid in leaguelist:
                                try:
                                    _leaguelist.append(
                                        Api(API_KEY).Lookups().League(
                                            leagueid=lgid)[0])
                                except:
                                    pass
                        leaguelist = _leaguelist
                        del _leaguelist
                        if eventlist:
                            for evid in eventlist:
                                try:
                                    _eventlist.append(
                                        Api(API_KEY).Lookups().Event(
                                            eventid=lgid)[0])
                                except:
                                    pass
                        eventlist = _eventlist
                        del _eventlist
                userobj.setTeams(teamlist)
                userobj.setPlayers(playerlist)
                userobj.setLeagues(leaguelist)
                userobj.setEvents(eventlist)
                return userobj
            else:
                logging.log("[TheSportsDB] A user must be provided", )

        def Seasons(self, leagueid=None):
            seasonlist = []
            if leagueid:
                url = f"{API_BASE_URL}/{API_KEY}/search_all_seasons.php?id={str(leagueid)}"
                data = json.load(urllib.request.urlopen(url))
                seasons = data["seasons"]
                if seasons:
                    for season in seasons:
                        seasonlist.append(season["strSeason"])
            else:
                logging.log("[TheSportsDB] leagueid must be provided", )
            return seasonlist

    class Schedules:
        class Last:
            def Team(self, teamid=None):
                eventlist = []
                if teamid:
                    url = f"{API_BASE_URL}/{API_KEY}/eventslast.php?id={str(teamid)}"
                    data = json.load(urllib.request.urlopen(url))
                    events = data["results"]
                    if events:
                        for event in events:
                            eventlist.append(_event.as_event(event))
                else:
                    logging.log("[TheSportsDB] teamid must be provided", )
                return eventlist

            def League(self, leagueid=None):
                eventlist = []
                if leagueid:
                    url = f"{API_BASE_URL}/{API_KEY}/eventspastleague.php?id={str(leagueid)}"
                    data = json.load(urllib.request.urlopen(url))
                    events = data["events"]
                    if events:
                        for event in events:
                            eventlist.append(_event.as_event(event))
                else:
                    logging.log("[TheSportsDB] leagueid must be provided", )
                return eventlist

        class Next:
            def Team(self, teamid=None):
                eventlist = []
                if teamid:
                    url = f"{API_BASE_URL}/{API_KEY}/eventsnext.php?id={str(teamid)}"
                    data = json.load(urllib.request.urlopen(url))
                    events = data["events"]
                    if events:
                        for event in events:
                            eventlist.append(_event.as_event(event))
                else:
                    logging.log("[TheSportsDB] teamid must be provided", )
                return eventlist

            def League(self, leagueid=None, rnd=None):
                eventlist = []
                if leagueid and not rnd:
                    url = f"{API_BASE_URL}/{API_KEY}/eventsnextleague.php?id={str(leagueid)}"
                elif leagueid and rnd:
                    url = (f"{API_BASE_URL}/{API_KEY}/eventsnextleague.php"
                           f"?id={str(leagueid)}&r={str(rnd)}")
                else:
                    logging.log("[TheSportsDB] leagueid must be provided", )
                    return eventlist
                data = json.load(urllib.request.urlopen(url))
                events = data["events"]
                if events:
                    for event in events:
                        eventlist.append(_event.as_event(event))
                return eventlist

        def Lookup(self,
                   datestring=None,
                   datetimedate=None,
                   league=None,
                   leagueid=None,
                   season=None,
                   rnd=None,
                   sport=None):
            eventlist = []
            if leagueid and season and rnd:
                url = (f"{API_BASE_URL}/{API_KEY}/eventsround.php"
                       f"?id={str(leagueid)}&r={str(rnd)}&s={str(season)}")
            elif leagueid and season and not rnd:
                url = (f"{API_BASE_URL}/{API_KEY}/eventsseason.php"
                       f"?id={str(leagueid)}&s={str(season)}")
            elif datestring or datetimedate:
                if datestring:
                    if _util.CheckDateString(datestring):
                        pass
                    else:
                        logging.log(
                            "[TheSportsDB] Wrong format for the datestring. "
                            "Valid format is {YYYY-MM-DD} (eg: 2014-10-10)", )
                        return eventlist
                else:
                    if _util.CheckDateTime(datetimedate):
                        datestring = datetimedate.strftime("%Y-%m-%d")
                    else:
                        logging.log(
                            "[TheSportsDB] Wrong type for datetime object. "
                            "A python datetime object is required", )
                        return eventlist
                if sport:
                    url = (f"{API_BASE_URL}/{API_KEY}/eventsday.php"
                           f"?d={str(datestring)}&s={str(sport)}")
                elif league:
                    url = (
                        f"{API_BASE_URL}/{API_KEY}/eventsday.php"
                        f"?d={str(datestring)}&l={urllib.parse.quote(league)}")
                else:
                    url = f"{API_BASE_URL}/{API_KEY}/eventsday.php?d={str(datestring)}"
            else:
                logging.log(
                    "[TheSportsDB] Wrong method invocation. "
                    "You need to declare either a datetimedate (datetime.date), "
                    "a datestring, a leagueid, season, rnd or sport", )
                return eventlist
            data = json.load(urllib.request.urlopen(url))
            events = data["events"]
            if events:
                for event in events:
                    eventlist.append(_event.as_event(event))
            return eventlist

    class Livescores:
        def Soccer(self, objects=False):
            url = f"{API_BASE_URL}/{API_KEY}/latestsoccer.php"
            eventlist = []
            data = json.load(urllib.request.urlopen(url))
            try:
                events = data["teams"]["Match"]
            except:
                events = ''
            if objects:
                api = Api(API_KEY)
            if events:
                if type(events) != list:
                    events = [events]
                for event in events:
                    eventobj = livescores.as_event(event)
                    try:
                        if objects:
                            hometeam = api.Lookups().Team(
                                eventobj.HomeTeam_Id)[0]
                            awayteam = api.Lookups().Team(
                                eventobj.AwayTeam_Id)[0]
                            eventobj.setHomeTeamObj(hometeam)
                            eventobj.setAwayTeamObj(awayteam)
                        eventlist.append(eventobj)
                    except:
                        pass
            return eventlist

    class Image:
        def Preview(self, image):
            if (image.startswith("http://www.thesportsdb.com/images/")
                    and image.endswith(".png")) or (
                        image.startswith("http://www.thesportsdb.com/images/")
                        and image.endswith(".jpg")):
                return image + "/preview"
            else:
                return None

        def Original(self, image):
            if (image.startswith("http://www.thesportsdb.com/images/")
                    and image.endswith(".png")) or (
                        image.startswith("http://www.thesportsdb.com/images/")
                        and image.endswith(".jpg")):
                return image
            else:
                return None
