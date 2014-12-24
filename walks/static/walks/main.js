
var myApp = angular.module('myApp',["ngResource", "ngCookies"]).run(
  function($http, $resource, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
  }
);

myApp.controller('WalksController', ['$scope', '$resource', function($scope, $resource) {
  var Walk = $resource(
    '/api/v1/walks/', null,
    {
      'update': { method:'PUT' }
    }
  );

  $scope.walks = Walk.query();
  $scope.newWalk = {};

  $scope.saveNewWalk = function() {
    var walk = new Walk($scope.newWalk);
    walk.$save(function(){
      $scope.newWalk = {};
      $scope.walks = Walk.query();
    });
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
}]);
