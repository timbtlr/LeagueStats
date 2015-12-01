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
            templateUrl: '/templates/home.html'
        })

        //  Query view
        .when('/about/', {
            templateUrl: '/templates/about.html'
        })

        //  Query view
        .when('/photos/', {
            templateUrl: '/templates/photos.html',
            controller: 'PhotoController'
        })

        //  Query view
        .when('/rsvp/', {
            templateUrl: 'templates/rsvp.html'
            //controller: 'RsvpController'
        })

        //  Query view
        .when('/registry', {
            templateUrl: 'templates/registry.html',
            controller: 'RegistryController'
        })

        //  Query view
        .when('/contact', {
            templateUrl: 'templates/contact.html'
        })

        //  Query view
        .when('/admin', {
            templateUrl: 'templates/admin.html'
        })

        //  Redirect incorrect navigation to the default (Home) view
        .otherwise({ redirectTo: '/' });

    $locationProvider.html5Mode(true);
}]);