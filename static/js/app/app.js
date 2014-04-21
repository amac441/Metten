

var years = angular.module("years", ["ui.bootstrap", "ngCookies", 'shoppinpal.mobile-menu'], function ($interpolateProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    }
);

years.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
})

years.config(function ($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl: "../static/js/app/views/feed.html",
            controller: "FeedController",

        })

        .when("/jobs", {
            templateUrl: "../static/js/app/views/jobs.html",
            controller: "FeedController",
            // resolve: {
            //         posts: function (PostService) {
            //         return PostService.list();  }
            // }
        })

        .when("/performance", {
            templateUrl: "../static/js/app/views/performance.html",
            controller: "FeedController",
            // resolve: {
            //         posts: function (PostService) {
            //         return PostService.list();  }
            // }
        })

        .when("/calendar", {
            templateUrl: "../static/js/app/views/calendar.html",
            controller: "FeedController",
            // resolve: {
            //         posts: function (PostService) {
            //         return PostService.list();  }
            // }
        })


        .when("/add", {
                    templateUrl: "../static/js/app/views/add_items.html",
                    controller: "AdderController",
                    resolve: {
                        adder: function (AdderService) {
                            return AdderService.list();
                        }
                    }
                })



        .otherwise({
            redirectTo: '/'
        })
})