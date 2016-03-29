/*
Name:
    home.control

Description:
    Controls the content of the photo view.

Author:
    Tim "KetsuN" Butler
*/

angular.module('KdaControl', [])
    .controller('KdaController', function ($scope, kdaFactory, dailyKdaFactory, monthlyKdaFactory, summonerFactory) {
        // KDA Chart
        $scope.chartOptions = {
            title: {
                text: 'Mean Performance per Hour'
            },
            xAxis: {
                categories: []
            },
            yAxis: {
                max: 1,
                min: 0
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
                width: 700,
                height: 300
            }
        };
        $scope.summoner_names = [];
        $scope.clicked = false;
        $scope.category = null

        summonerFactory.list().then(function(result) {
            $scope.summoner_names = result.data;
        });

        $scope.isActive = function(category) {
            return $scope.category === category;
        };

        $scope.sortCategory = function(category) {
            $scope.category = category;
        };

        $scope.queryForHourlyKda = function(summoner) {
            $scope.clicked = false;
            $scope.chartOptions.series[0].data = [];
            $scope.chartOptions.series[1].data = [];
            $scope.chartOptions.xAxis.categories = [];
            $scope.chartOptions.title.text = "Performance per Hour of Day";
            $scope.chartOptions.yAxis.min = 0;
            $scope.chartOptions.yAxis.max = 1;

            kdaFactory.get(summoner.name).then(function(result) {
                var kda_info = result.data['KDA'];
                var data = eval(kda_info);

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        $scope.chartOptions.series[0].data.push(data[key]);
                        $scope.chartOptions.xAxis.categories.push(key);
                    }
                }

                $scope.clicked = true;

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

        $scope.queryForDailyKda = function(summoner) {
            $scope.chartOptions.series[0].data = [];
            $scope.chartOptions.series[1].data = [];
            $scope.chartOptions.xAxis.categories = [];
            $scope.chartOptions.title.text = "Performance per Day of Week";
            $scope.chartOptions.yAxis.min = 0;
            $scope.chartOptions.yAxis.max = 1;

            dailyKdaFactory.get(summoner.name).then(function(result) {
                var kda_info = result.data['KDA'];
                var data = eval(kda_info);

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        $scope.chartOptions.series[0].data.push(data[key]);
                        $scope.chartOptions.xAxis.categories.push(key);
                    }
                }

                $scope.clicked = true;

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

        $scope.queryForMonthlyKda = function(summoner) {
            $scope.chartOptions.series[0].data = [];
            $scope.chartOptions.series[1].data = [];
            $scope.chartOptions.xAxis.categories = [];
            $scope.chartOptions.title.text = "Performance per Month of Year";
            $scope.chartOptions.yAxis.min = 0;
            $scope.chartOptions.yAxis.max = 1;

            monthlyKdaFactory.get(summoner.name).then(function(result) {
                var kda_info = result.data['KDA'];
                var data = eval(kda_info);

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        $scope.chartOptions.series[0].data.push(data[key]);
                        $scope.chartOptions.xAxis.categories.push(key);
                    }
                }

                $scope.clicked = true;

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

        $scope.queryForTopFive = function(summoner_name) {
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