var defaultLatLng = new google.maps.LatLng(37.7860099, -122.4025387);

var queryMarker = new google.maps.Marker({
    position: defaultLatLng,
    draggable: true
})

var resultMarkers = [];


// clear all of our bike markers
function clearMarkers() {
    for (var i = 0; i < resultMarkers.length; i++) {
        resultMarkers[i].setMap(null);
    }

    resultMarkers = [];
}

// try to update queryMarker with our user's location
function getUserLocation () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            defaultLatLng = new google.maps.LatLng(
                position.coords.latitude,
                position.coords.longitude
            );
            // move the queryMarker and re-run the query
            queryMarker.setPosition(defaultLatLng);
            queryMarker.map.setCenter(defaultLatLng);
            drawQueryResults(queryMarker.map)();
      });
    }
}


// hit /search and draw results
function drawQueryResults(map) {
    var myIcon = new google.maps.MarkerImage(
        "/images/bike-fullres.png", null, null, null,
        new google.maps.Size(30, 30)
    );


    function drawMarkers(response) {
        clearMarkers();

        results = JSON.parse(response).results;

        for (var i = 0; i < results.length; i++) {
            var result = results[i];
            var coords = result.loc.coordinates;
            var latLng = new google.maps.LatLng(coords[1], coords[0]);
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                icon: myIcon,
                optimized: false,
                clickable: false
            });
            resultMarkers.push(marker);
        }

    }

    // make the AJAX request
    return function() {
        var lng = queryMarker.position.A
        var lat = queryMarker.position.k
        fetch('/search?lat=' + lat + '&lng=' + lng, drawMarkers);
    }
}


// this is kinda nice if the user resizes their window
function recenterMap(map) {
    return function() {
        var center = map.getCenter();
        google.maps.event.trigger(map, "resize");
        map.setCenter(center);
    }
}


function initialize() {

    getUserLocation();

    var mapOptions = {
        center: queryMarker.position,
        zoom: 17,
        minZoom: 12,
        streetViewControl: false,
        mapTypeControl: false,
        styles: mapStyles
    };

    var map = new google.maps.Map(
        document.getElementById("map-canvas"),
        mapOptions
    );

    queryMarker.setMap(map);

    google.maps.event.addDomListener(window, "resize", recenterMap(map));
    google.maps.event.addListener(queryMarker, 'dragend', drawQueryResults(map));

    drawQueryResults(map)();
}


google.maps.event.addDomListener(window, 'load', initialize);

// adapted from
// http://snazzymaps.com/style/25/blue-water
var mapStyles = [
    {
        "featureType": "water",
        "stylers": [
            {
                "color": "#46bcec"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "landscape",
        "stylers": [
            {
                "color": "#f2f2f2"
            }
        ]
    },
    {
        "featureType": "road",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "lightness": 45
            }
        ]
    },
    {
        "featureType": "road.highway",
        "stylers": [
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#444444"
            }
        ]
    },
    {
        "featureType": "poi",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "stylers": [
            {
                "visibility": "on",
            },
            {
                "color": "#cccccc"
            }
        ]
    }
]
