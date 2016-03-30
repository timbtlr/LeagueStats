/*
Name:
    appRoutes

Description:


Author:
    Tim "KetsuN" Butler
*/
angular
    .module('appRoutes', [])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $routeProvider
        //  Home view
        .when('/', {
            templateUrl: '/templates/main.html'
        })

        //  Champs view
        .when('/summoners', {
            templateUrl: '/templates/summoner.html'
        })

        //  Champs view
        .when('/champs', {
            templateUrl: '/templates/champs.html'
        })

        //  Hourly KDA view
        .when('/kda-hour', {
            templateUrl: '/templates/kda_hour.html'
        })

        //  Daily KDA view
        .when('/kda-day', {
            templateUrl: '/templates/kda_day.html'
        })

        //  Monthly KDA view
        .when('/kda-month', {
            templateUrl: '/templates/kda_month.html'
        })

        //  Redirect incorrect navigation to the default (Home) view
        .otherwise({ redirectTo: '/' });
}]);