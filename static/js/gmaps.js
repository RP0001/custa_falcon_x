initMapSize();
window.onresize = function () {
    initMapSize();
}
//initialise map for specific zoom, location and name
function initMap() {
    var myLatLng = {lat: 55.873706, lng: -4.292585};

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 17,
        center: myLatLng
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'CUSTA'
    });

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });
}

//make map's height as its width
function initMapSize() {
    $("#map").height($("#map").width());
}