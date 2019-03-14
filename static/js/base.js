$(document).ready(function(){
      $('.parallax').parallax();
    });
var pathname = window.location.pathname;
M.AutoInit();
initNavbar();
initParallax();
function initNavbar() {
    var idSegment = "";
    if(pathname==="/custa/" || pathname==="/"){
        idSegment = "index";
    } else {
        idSegment = pathname.substring(7,pathname.length-1);
    }
    document.getElementById("nav-"+idSegment).className = "active";
}

function initParallax() {
    if(pathname==="/custa/" || pathname==="/"){
        $("#parallax-1").css("height", "550px");
    }
}
