angular
    .module('SummonerControl', [])
    .controller('SummonerController', function($scope, summonerFactory, summonerStatsFactory) {
        $scope.summoner_names = []
        $scope.summoner_info = {}
        $scope.champ_summary = []
        $scope.clicked = false;
        $scope.category = [];

        $scope.chartOptions = {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Summoner Statistics'
            },
            xAxis: {
                categories: [
                    'Wins','Losses', 'Kills','Deaths','Assists','Doubles','Triples','Quadras',
                    'Pentas'
                ],
                crosshair: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [],
            size: {
                width: 720,
                height: 400
            }
        };

        summonerFactory.list().then(function(result) {
            $scope.summonerStats = result.data;
            console.log($scope.summonerStats.length);
            console.log($scope.summonerStats[0]);

            for (var i=0; i < $scope.summonerStats.length; i++) {
                var summonerId = $scope.summonerStats[i].id;
                summonerStatsFactory.get(summonerId).then(function(result) {
                    stats = result.data
                    for (var k=0; k < $scope.summonerStats.length; k++) {
                        if ($scope.summonerStats[k].id == stats.id) {
                            $scope.summonerStats[k].stats = stats;
                        };
                    };
                });
            };
        });

        $scope.isActive = function(category) {
            return $scope.category.indexOf(category) != -1;
        };

        $scope.sortCategory = function(category) {
            var index = $scope.category.indexOf(category);
            if (index == -1) {
                if ($scope.category.length <= 2) {
                    $scope.category.push(category);
                }
            } else {
                $scope.category.splice(index, 1);
            }
        };

        $scope.editChart = function(summoner) {
            var exists = false;
            var index = -1;
            for (var i=0; i < $scope.chartOptions.series.length; i++) {
                if ($scope.chartOptions.series[i].name == summoner.name){
                    exists = true;
                    index = i;
                };
            };

            if (!exists) {
                var highestIndex = $scope.chartOptions.series.length;
                if (highestIndex <= 2) {
                    $scope.chartOptions.series[highestIndex] = {
                        "type": 'column',
                        "name": summoner.name,
                        "data": [
                            summoner.stats['wins'],
                            summoner.stats['losses'],
                            summoner.stats['kills'],
                            summoner.stats['deaths'],
                            summoner.stats['assists'],
                            summoner.stats['doubles'],
                            summoner.stats['triples'],
                            summoner.stats['quads'],
                            summoner.stats['pentas']
                        ]
                    }
                };
            } else {
                $scope.chartOptions.series.splice(index, 1);
            };
        };
    });


