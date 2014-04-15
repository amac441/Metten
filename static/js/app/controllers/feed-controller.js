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


   // ------------TABBING----------------- //


    $scope.tabs = 
    [
    { title:"Dynamic Title 1", content:"Dynamic content 1" },
    { title:"Dynamic Title 2", content:"Dynamic content 2"}
    ];


    // -------- MISC -------------------

    $scope.toggleActive = function (s) {
        s.active = !s.active;
    };

    // need to refactor all of these

    $scope.oneAtATime = false;


    // --------- JOB SEARCH -----------

    $scope.searchFor = function () {
        SearchService.get_jobs($scope.searched).then(function (data) {
            $scope.search = data;
        }
        )
    };


    // -------- SITE SEARCHES ----------

    $scope.searchStay = function () {


            var sites = [
            'LinkedIn', 'UNL', 'Meetup', 'Alltop', 'ItunesU', 'Amazon', 'Coursera'
             ]

        var range = [];
        for (var x in sites) {

            SearchService.get_stay($scope.stay_search, sites[x]).then(function (data) {

            $scope.daters_meet = data['Meetup'];
            $scope.daters_unl = data['UNL'];
            $scope.daters_linked = data['LinkedIn'];
            $scope.daters_alltop = data['Alltop'];
            $scope.daters_tunes = data['ItunesU'];
            $scope.daters_amazon = data['Amazon'];
            $scope.daters_coursera = data['Coursera'];
          
                
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