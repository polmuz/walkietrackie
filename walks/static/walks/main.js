
var myApp = angular.module('myApp',["ngResource", "ngCookies"]).run(
  function($http, $resource, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
  }
);

myApp.controller('WalksController', ['$scope', '$resource', function($scope, $resource) {
  var Walk = $resource(
    '/api/v1/walks/:pk', {pk: "@pk"},
    {
      'update': { method:'PUT' }
    }
  );



  $scope.refreshWalks = function() {
    var walks = Walk.query(function(){
      $scope.weekStats = {};
      for (var i = 0; i < walks.length; i++) {
        var walk = walks[i];
        var date = new Date(walk.date);
        var week = date.format("Y-\\WW");
        var stats = $scope.weekStats[week] || {distance:0, time:0, walks:0};
        $scope.weekStats[week] = {
          distance: stats.distance + walk.distance,
          time: stats.time + walk.time,
          walks: stats.walks + 1
        }
      }

      return true;
    });

    $scope.walks = walks;
    return true;
  };

  $scope.refreshWalks();
  $scope.newWalk = {};
  $scope.dateFilter = {};


  $scope.saveNewWalk = function() {
    var walk = new Walk($scope.newWalk);
    walk.$save(
      walk,
      function(){
        $scope.newWalk = {};
        $scope.refreshWalks();
      },
      function(r){
        $scope.newWalk.errors = r.data;
        console.log("error");
      });
  };

  $scope.removeWalk = function(walk) {
    walk.$remove(function(){
      $scope.refreshWalks();
    });

  };

  $scope.clearDateFilter = function() {
    $scope.dateFilter = {};
  };

  $scope.betweenFilter = function(prop, range){
    return function(item){
      if (range.from && range.to) {
        if (item[prop] >= range.from && item[prop] <= range.to) {
          return true;
        }

        return false;
      }

      if (range.from && !range.to && item[prop] >= range.from) {
        return true;
      }

      if (range.to && !range.from && item[prop] <= range.to) {
        return true;
      }

      if (!range.to && !range.from) {
        return true;
      }

      return false;
    }
}
}]);

myApp.controller("WalkController", ["$scope", function($scope){
  $scope.editMode = false;

  $scope.edit = function() {
    $scope.editMode = true;
  };

  $scope.save = function() {
    $scope.editMode = false;
    $scope.walk.$update(function(){
      $scope.refreshWalks();
    });
  };

  $scope.remove = function() {
    $scope.removeWalk($scope.walk);
  };
}]);
