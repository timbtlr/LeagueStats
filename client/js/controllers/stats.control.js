/*
Name:
    home.control

Description:
    Controls the content of the photo view.

Author:
    Tim "KetsuN" Butler
*/

angular
    .module('StatsControl', [])
    .directive('ngChampDisplay', function() {
      return {
        restrict: 'A',
        template: '<span style="font-size:25px;">{{champ.name}}: {{champ.title}} | Times Played: {{champ.times_played}}</span>'
      }
    })
    .filter("toArray", function() {
        return function(obj) {
            var result = [];
                angular.forEach(obj, function(val, key) {
                    result.push(val);
                });
        return result;
        };
    })
    .controller('StatsController', function($scope, summonerFactory, matchListFactory, matchFactory, championFactory) {
        $scope.summoner_info = {}
        $scope.champ_summary = {}

        $scope.queryForSummonerMatches = function(summoner_name) {
            summonerFactory.get(summoner_name, $scope.api_key).then(function(result) {
                $scope.summoner_info = result.data[summoner_name];
                matchListFactory.get($scope.summoner_info['id'], $scope.api_key).then(function(result) {
                    $scope.process_match_list(result.data.matches);
                });
            });
        };

        $scope.process_match_list = function(match_list) {
            var summary = {}
            console.log(match_list)
            for (var i=0; i < match_list.length; i++) {
                var champ_id = match_list[i]['champion'];

                if (!(champ_id in summary)) {
                    summary[champ_id] = {"times_played": 1};
                } else {
                    summary[champ_id].times_played = summary[champ_id].times_played + 1;
                };
            };

            for (var champ_id in summary) {
                championFactory.get(champ_id, $scope.api_key).then(function(result) {
                    summary[result.data['id']].name = result.data['name']
                    summary[result.data['id']].title = result.data['title']
                    summary[result.data['id']].image_url = "http://ddragon.leagueoflegends.com/cdn/5.23.1/img/champion/" + result.data['image']['full']
                });
            };

            $scope.champ_summary = summary;
        };
});


