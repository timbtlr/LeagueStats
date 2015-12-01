angular
    .module('lolService', [])
    .factory('lolApiServiceFactory', ['$http', function($http) {
        return {
            get : function() {
                return $http.get('https://agile-hamlet-2538.herokuapp.com/photos/');
            }
        }
    }])