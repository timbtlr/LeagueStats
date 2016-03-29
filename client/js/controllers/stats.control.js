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
        template: '<span style="font-size:25px;">{{champ.name}}: {{champ.title}} | Times Played: {{champ.times_played}} | KDA: {{champ.kda}}</span>'
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
        $scope.summoner_names = []
        $scope.summoner_info = {}
        $scope.champ_summary = []
        $scope.clicked = false;
        $scope.category = null;

        summonerFactory.list().then(function(result) {
            $scope.summoner_names = result.data;
        });

        $scope.isActive = function(category) {
            console.log($scope.category === category)
            return $scope.category === category;
        };

        $scope.sortCategory = function(category) {
            console.log($scope.category)
            $scope.category = category;
        };


        $scope.queryForSummonerMatches = function(summoner) {
            $scope.clicked = true;
            $scope.errorMessage = null;
            $scope.error = null;

            matchListFactory.get(summoner['id']).then(function(result) {
                if (result.data.length > 0) {
                    $scope.process_match_list(result.data);
                } else {
                    $scope.champ_summary = []
                };
            });
        };

        $scope.process_match_list = function(match_list) {
            var summary = {}
            for (var i=0; i < match_list.length; i++) {
                var champ_id = match_list[i]['champ'];

                if (!(champ_id in summary)) {
                    summary[champ_id] = {
                        "times_played": 1,
                        "kills": match_list[i]['kills'],
                        "deaths": match_list[i]['deaths'],
                        "assists": match_list[i]['assists']
                    };
                } else {
                    summary[champ_id].times_played += 1;
                    summary[champ_id].kills += match_list[i]['kills'];
                    summary[champ_id].deaths += match_list[i]['deaths'];
                    summary[champ_id].assists += match_list[i]['assists'];
                };
            };

            for (var champ_id in summary) {
                championFactory.get(champ_id, $scope.api_key).then(function(result) {
                    summary[result.data['id']].name = result.data['name'];
                    summary[result.data['id']].title = result.data['title'];
                    summary[result.data['id']].image_url = "http://ddragon.leagueoflegends.com/cdn/5.23.1/img/champion/" + result.data['image']['full'];
                });

                if (summary[champ_id].deaths > 0) {
                    summary[champ_id].kda = Math.round(((summary[champ_id].kills + summary[champ_id].assists) / summary[champ_id].deaths * 100)) / 100;
                } else {
                    summary[champ_id].kda = (summary[champ_id].kills + summary[champ_id].assists);
                }
            };

            $scope.champ_summary = summary;
        };
});


