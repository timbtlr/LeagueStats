/*
Name:
    appRoutes

Description:


Author:
    Tim "KetsuN" Butler
*/
angular
    .module('appRoutes', [])
    .config(['$routeProvider', '$locationProvider', '$httpProvider', function($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider
        //  Home view
        .when('/', {
            templateUrl: '/templates/main.html'
        })

        //  KDA view
        .when('/kda-hour', {
            templateUrl: '/templates/kda_hour.html'
        })

        //  Redirect incorrect navigation to the default (Home) view
        .otherwise({ redirectTo: '/' });

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];

    $locationProvider.html5Mode(true);
}]);