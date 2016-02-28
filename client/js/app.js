/*
Name:
    app.js

Description:
    Defines the main application module for the Inventory Management application along with all application
    dependencies.

Author:
    Tim "KetsuN" Butler
*/
'use strict';

angular
    .module('leagueStatsApp', [
        'ui.bootstrap',
        'ngRoute',
        'appRoutes',
        'highcharts-ng',
        'StatsControl',
        'KdaControl',
        'KdaService',
        'DailyKdaService',
        'SummonerService',
        'MatchListService',
        'MatchService',
        'ChampionService'
    ]);
