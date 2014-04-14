

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
            // resolve: {
            //     posts: function (PostService) {
            //         return PostService.list();
            //     }
        })
        // .when("/post/:id", {
        //     templateUrl: "static/js/app/views/view.html",
        //     controller: "PostController",
        //     resolve: {
        //         post: function ($route, PostService) {
        //             var postId = $route.current.params.id
        //             return PostService.get(postId);
        //         }
        //     }
        // })

        .otherwise({
            redirectTo: '/'
        })
})