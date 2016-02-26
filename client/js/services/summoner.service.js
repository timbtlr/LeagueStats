angular
    .module('SummonerService', [])
    .factory('summonerFactory', ['$http', function($http) {
        return {
            get : function(summoner_name, league_api_key) {
                return $http.get('https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + summoner_name,  {
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
                return $http.get('https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/' + summoner_id,  {
                    params: {
                        api_key: league_api_key,
                        rankedQueues: 'RANKED_SOLO_5x5',
                        seasons: 'PRESEASON3,SEASON3,PRESEASON2014,SEASON2014,PRESEASON2015,SEASON2015,PRESEASON2016,SEASON2016'
                    }
                });
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