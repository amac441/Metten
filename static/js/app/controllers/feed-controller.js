years.controller('FeedController', function ($scope, GlobalService, SearchService, TagService) {

    $scope.globals = GlobalService;
    //options for modals
    $scope.opts = {
        backdropFade: true,
        dialogFade: true
    };

    $scope.toggleActive = function (s) {
        s.active = !s.active;
    };

    // need to refactor all of these

    $scope.oneAtATime = false;

    $scope.searchFor = function () {
        SearchService.get_jobs($scope.searched).then(function (data) {
            $scope.search = data;
        }
        )
    };

    $scope.searchStay = function () {

        // eventually this will come from the back end!
        var sites = [
            'UNL', 'Amazon', 'Alltop',
            'Meetup', 'Coursera',
            'ItunesU', 'LinkedIn']
            // 'Indeed', 

        var range = [];
        for (var x in sites) {

            SearchService.get_stay($scope.stay_search, sites[x]).then(function (data) {

               for (key in data) {
                       $scope.stays = data[key];
                       $scope.daters = data;
               }
                
            }
         )
        }
    };

    $scope.refreshSites = function (s) {

        SearchService.get_stay($scope.stay_search, s).then(function (data) {

            for (key in data) {
                $scope.stays = data[key];
                $scope.daters = data;
            }

        }
     )
     };
});


//<form class="well form-search" >
//    <h3>{[{site_name}]}</h3>
//    <ul>
//        <li ng-class="{active:stay.active}" ng-repeat="(key,stay) in stays" ng-click="toggleActive(stay)">{[{stay}]}</li>
//    </ul>
//</form>