import google.maps.*;

function initMap() {
    const borr = {lat: 55.873730, lng: -4.292607};
    var map = new google.maps.Map(document.getElementById('map'), {zoom: 17, center: borr});
    var marker = new google.maps.Marker({position: borr, map: map});
    }