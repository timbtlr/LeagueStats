angular
    .module('SummonerService', [])
    .factory('summonerFactory', ['$http', 'ENV', function($http, ENV) {
        return {
            get : function(summoner_name) {
                return $http.get(ENV.baseServerUrl + '/summoners/?name=' + summoner_name);
            },
            list : function() {
                return $http.get(ENV.baseServerUrl + '/summoners/');
            }
        }
    }])

angular
    .module('MatchListService', [])
    .factory('matchListFactory', ['$http', 'ENV', function($http, ENV) {
        return {
            get : function(summoner_id) {
                return $http.get(ENV.baseServerUrl + '/matches/?summoner=' + summoner_id);
            }
        }
    }])

angular
    .module('MatchService', [])
    .factory('matchFactory', ['$http', 'ENV', function($http, ENV) {
        return {
            get : function(match_id) {
                return $http.get('https://na.api.pvp.net/api/lol/na/v2.2/match/' + match_id,  {
                    params: {api_key: ENV.leagueApiKey}
                });
            }
        }
    }])

angular
    .module('ChampionService', [])
    .factory('championFactory', ['$http', 'ENV', function($http, ENV) {
        return {
            get : function(champ_id) {
                return $http.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + champ_id + '?champData=image',  {
                    params: {api_key: ENV.leagueApiKey}
                });
            }
        }
    }])

angular
    .module('KdaService', [])
    .factory('kdaFactory', ['$http', 'ENV', function($http, ENV) {
        return {
            get : function(summoner_name) {
                return $http.get(ENV.baseServerUrl + '/matches/hourly-kda/?summoner=' + summoner_name);
            }
        }
    }])

angular
    .module('DailyKdaService', [])
    .factory('dailyKdaFactory', ['$http', 'ENV', function($http, ENV) {
        return {
            get : function(summoner_name) {
                return $http.get(ENV.baseServerUrl + '/matches/daily-kda/?summoner=' + summoner_name);
            }
        }
    }])

angular
    .module('ChampStatsService', [])
    .factory('champStatsFactory', ['$http', 'ENV', function($http, ENV) {
        return {
            get : function(summoner_name) {
                return $http.get('http://localhost:8001/matches/champion-stats/?summoner=' + summoner_name);
            }
        }
    }])

