
var myApp = angular.module('myApp',["ngResource"]);

myApp.controller('WalksController', ['$scope', '$resource', function($scope, $resource) {
  var Walks = $resource('/api/v1/walks/');

  $scope.walks = Walks.query();
}]);
