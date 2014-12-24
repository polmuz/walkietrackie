
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

  $scope.walks = Walk.query();
  $scope.newWalk = {};
  $scope.dateFilter = {};

  $scope.refreshWalks = function() {
    $scope.walks = Walk.query();
  };

  $scope.saveNewWalk = function() {
    var walk = new Walk($scope.newWalk);
    walk.$save(function(){
      $scope.newWalk = {};
      $scope.refreshWalks();
    });
  }

  $scope.removeWalk = function(walk) {
    walk.$remove();
    $scope.refreshWalks();
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
    $scope.walk.$update();
  };

  $scope.remove = function() {
    $scope.removeWalk($scope.walk);
  };
}]);
