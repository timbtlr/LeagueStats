'use strict';

angular
    .module('leagueStatsApp', [
        'ui.bootstrap',
        'ngRoute',
        'appRoutes',
        'ngResource',
        'highcharts-ng',
        'SummonerControl',
        'MainControl',
        'StatsControl',
        'KdaControl',
        'KdaService',
        'DailyKdaService',
        'ChampStatsService',
        'SummonerService',
        'MatchListService',
        'MatchService',
        'ChampionService',
        'envConfig'
    ])
    .config(function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    });
