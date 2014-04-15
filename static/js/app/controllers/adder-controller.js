years.controller('AdderController', function ($scope, $routeParams, $location, AdderService, GlobalService, adder) {
    $scope.adder = adder;
    $scope.globals = GlobalService;
    var failureCb = function (status) {
        console.log(status);
    }
    //options for modals
    $scope.opts = {
        backdropFade: true,
        dialogFade: true
    };

    // --------- ADD ITEM -----------

    $scope.addItem = function () {
        SearchService.add_item($scope.sender, $scope.recipient, $scope.subject, $scope.details).then(function (data) {
            $scope.items = data;
        }
        )
    };
});
