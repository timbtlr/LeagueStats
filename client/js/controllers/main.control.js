angular
    .module('MainControl', [])
    .controller('MainController', function($scope, summonerFactory) {
        $scope.summoner_info = {};
        $scope.champ_summary = {};
        $scope.category = null;

        $scope.isActive = function(category) {
            console.log($scope.category === category)
            return $scope.category === category;
        };

        $scope.sortCategory = function(category) {
            console.log($scope.category)
            $scope.category = category;
        };
});


