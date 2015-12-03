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

        //  Redirect incorrect navigation to the default (Home) view
        .otherwise({ redirectTo: '/' });

    $locationProvider.html5Mode(true);
}]);