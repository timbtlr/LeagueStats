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
        .when('/champs', {
            templateUrl: '/templates/champs.html'
        })

        //  KDA view
        .when('/kda-hour', {
            templateUrl: '/templates/kda_hour.html'
        })

        //  Redirect incorrect navigation to the default (Home) view
        .otherwise({ redirectTo: '/' });
}]);