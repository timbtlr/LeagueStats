angular
    .module('SummonerService', [])
    .factory('summonerFactory', ['$http', function($http) {
        return {
            get : function(summoner_name, league_api_key) {
                return $http.get('http://localhost:8000/summoners/?name=' + summoner_name,  {
                    params: {api_key: league_api_key}
                });
            }
        }
    }])

angular
    .module('MatchListService', [])
    .factory('matchListFactory', ['$http', function($http) {
        return {
            get : function(summoner_id, league_api_key) {
                return $http.get('http://localhost:8000/matches/?summoner=' + summoner_id);
            }
        }
    }])

angular
    .module('MatchService', [])
    .factory('matchFactory', ['$http', function($http) {
        return {
            get : function(match_id, league_api_key) {
                return $http.get('https://na.api.pvp.net/api/lol/na/v2.2/match/' + match_id,  {
                    params: {api_key: league_api_key}
                });
            }
        }
    }])

angular
    .module('ChampionService', [])
    .factory('championFactory', ['$http', function($http) {
        return {
            get : function(champ_id, league_api_key) {
                return $http.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + champ_id + '?champData=image',  {
                    params: {api_key: league_api_key}
                });
            }
        }
    }])

angular
    .module('KdaService', [])
    .factory('kdaFactory', ['$http', function($http) {
        return {
            get : function(champ_name) {
                return $http.get('http://localhost:8000/matches/hourly-kda/?summoner=' + champ_name);
            }
        }
    }])

angular
    .module('DailyKdaService', [])
    .factory('dailyKdaFactory', ['$http', function($http) {
        return {
            get : function(champ_name) {
                return $http.get('http://localhost:8000/matches/daily-kda/?summoner=' + champ_name);
            }
        }
    }])

