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
                {name: 'KDA', data: []},
                {name: 'Win Percent', data: []},
                {name: 'Kills', data: []},
                {name: 'Deaths', data: []},
                {name: 'Assists', data: []}
            ],
            size: {
                width: 720,
                height: 400
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

        $scope.addDataToSeries = function(data, seriesIndex) {
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    $scope.chartOptions.series[seriesIndex].data.push(data[key]);
                }
            }
        }

        $scope.prepareKdaSeriesData = function(kdaInfo, winInfo, killInfo, deathInfo, assistInfo) {
            $scope.chartOptions.series[0].data = [];
            $scope.chartOptions.series[1].data = [];
            $scope.chartOptions.series[2].data = [];
            $scope.chartOptions.series[3].data = [];
            $scope.chartOptions.series[4].data = [];
            $scope.addDataToSeries(eval(kdaInfo), 0);
            $scope.addDataToSeries(eval(winInfo), 1);
            $scope.addDataToSeries(eval(killInfo), 2);
            $scope.addDataToSeries(eval(deathInfo), 3);
            $scope.addDataToSeries(eval(assistInfo), 4);
        }

        $scope.queryForHourlyKda = function(summoner) {
            $scope.clicked = false;
            $scope.chartOptions.xAxis.categories = [
                "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
                "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
                "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"
            ];
            $scope.chartOptions.title.text = "Performance per Hour of Day";
            $scope.chartOptions.yAxis.min = 0;
            $scope.chartOptions.yAxis.max = 1;

            kdaFactory.get(summoner.name).then(function(result) {
                $scope.prepareKdaSeriesData(
                    result.data['KDA'],
                    result.data['Win'],
                    result.data['Kills'],
                    result.data['Deaths'],
                    result.data['Assists']
                );
                $scope.clicked = true;
            });
        };

        $scope.queryForDailyKda = function(summoner) {
            $scope.chartOptions.xAxis.categories = [
                "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday"
            ];
            $scope.chartOptions.title.text = "Performance per Day of Week";
            $scope.chartOptions.yAxis.min = 0;
            $scope.chartOptions.yAxis.max = 1;

            dailyKdaFactory.get(summoner.name).then(function(result) {
                $scope.prepareKdaSeriesData(
                    result.data['KDA'],
                    result.data['Win'],
                    result.data['Kills'],
                    result.data['Deaths'],
                    result.data['Assists']
                );
                $scope.clicked = true;
            });
        };

        $scope.queryForMonthlyKda = function(summoner) {
            $scope.chartOptions.xAxis.categories = [
                "January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December"
            ];
            $scope.chartOptions.title.text = "Performance per Month of Year";
            $scope.chartOptions.yAxis.min = 0;
            $scope.chartOptions.yAxis.max = 1;

            monthlyKdaFactory.get(summoner.name).then(function(result) {
                $scope.prepareKdaSeriesData(
                    result.data['KDA'],
                    result.data['Win'],
                    result.data['Kills'],
                    result.data['Deaths'],
                    result.data['Assists']
                );
                $scope.clicked = true;
            });
        };
    });