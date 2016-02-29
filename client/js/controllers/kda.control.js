/*
Name:
    home.control

Description:
    Controls the content of the photo view.

Author:
    Tim "KetsuN" Butler
*/

angular.module('KdaControl', [])
    .controller('KdaController', function ($scope, kdaFactory, dailyKdaFactory) {
        // KDA Chart
        $scope.chartOptions = {
            title: {
                text: 'Mean KDA per Hour'
            },
            xAxis: {
                categories: []
            },
            series: [
                {
                    name: 'KDA',
                    data: []
                },
                {
                    name: 'Win Percent',
                    data: []
                }
            ],
            size: {
                width: 800,
                height: 300
            }
        };

        $scope.queryForHourlyKda = function(summoner_name) {
            $scope.chartOptions.series[0].data = [];
            $scope.chartOptions.series[1].data = [];
            $scope.chartOptions.xAxis.categories = [];

            kdaFactory.get(summoner_name).then(function(result) {
                var kda_info = result.data['KDA'];
                var data = eval(kda_info);

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        $scope.chartOptions.series[0].data.push(data[key]);
                        $scope.chartOptions.xAxis.categories.push(key);
                    }
                }

                var win_info = result.data['Win'];
                var data = eval(win_info);

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        $scope.chartOptions.series[1].data.push(data[key]);
                        $scope.chartOptions.xAxis.categories.push(key);
                    }
                }
            });
        };

        $scope.queryForDailyKda = function(summoner_name) {
            $scope.chartOptions.series[0].data = [];
            $scope.chartOptions.series[1].data = [];
            $scope.chartOptions.xAxis.categories = [];

            dailyKdaFactory.get(summoner_name).then(function(result) {
                var kda_info = result.data['KDA'];
                var data = eval(kda_info);

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        $scope.chartOptions.series[0].data.push(data[key]);
                        $scope.chartOptions.xAxis.categories.push(key);
                    }
                }
            });
        };
    });