(function() {
  'use strict';

  var app = angular.module('dataleek', ['ui.bootstrap', 'highcharts-ng']);

  app.controller('AppController', ['$scope', '$http',
    function($scope, $http) {
    $scope.all_data = [];
    $scope.filter = {sigma: 1.0, min: 1, max: 200};
    $scope.chartSeries = [
      {
        name: 'Force',
        data: [],
        color: 'rgb(144, 237, 125)',
      },
      {
        name: 'Agilité',
        data: [],
        color: 'rgb(124, 181, 236)',
      },
      {
        name: 'Vie',
        data: [],
        color: 'rgb(241, 92, 128)',
      }
    ];

    var fetchFilteredSeries = function() {
      $scope.chartConfig.loading = true;
      return $http({method: 'GET', url: '/api/levels/filtered?sigma=' + $scope.filter.sigma})
      .success(function(data) {
        $scope.chartConfig.loading = false;
        $scope.all_data = data.levels;
      });
    };

    var reloadFilteredSeries = function() {
      var str = $scope.chartSeries[0]['data'];
      var agi = $scope.chartSeries[1]['data'];
      var life = $scope.chartSeries[2]['data'];

      // Empty current series
      while(str.length > 0) {
        str.pop();
        agi.pop();
        life.pop();
      }

      // Fill it
      for (var i in $scope.all_data) {
        var level = $scope.all_data[i];
        if (level.level > $scope.filter.max) break;
        if (level.level < $scope.filter.min) continue;

        str.push([level.level, level.str]);
        agi.push([level.level, level.agi]);
        life.push([level.level, level.life]);
      };
    };

    $scope.$watch('filter.sigma', function() {
      fetchFilteredSeries().then(reloadFilteredSeries);
    });
    $scope.$watch('filter.min', reloadFilteredSeries);
    $scope.$watch('filter.max', reloadFilteredSeries);

    $scope.chartConfig = {
      options: {
        chart: {
          type: 'line'
        },
        plotOptions: {
          line: {
            lineWidth: 4,
            states: {
              hover: {
                lineWidth: 5
              }
            },
            marker: {
              enabled: false
            },
          }
        },
        title: {
          text: 'Stat pondéré par les taux de victoire'
        },
      },
      series: $scope.chartSeries,
      loading: false,
    }
  }]);
})();
