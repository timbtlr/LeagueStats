angular
    .module('MainControl', [])
    .controller('MainController', function($scope, summonerFactory) {
        $scope.summoner_info = {};
        $scope.champ_summary = {};
        $scope.category = null;

        $scope.isActive = function(category) {
            return $scope.category === category;
        };

        $scope.sortCategory = function(category) {
            $scope.category = category;
        };
});


