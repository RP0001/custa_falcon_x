$(document).ready(function () {
    $('.parallax').parallax();
    if (!isAtHomePage()) {
        initContainerHeight();
    }
});
var pathname = window.location.pathname;
M.AutoInit();
initNavbar();
initParallax();


function initNavbar() {
    var idSegment = "";
    if (isAtHomePage()) {
        idSegment = "index";
    } else {
        idSegment = pathname.substring(7, pathname.length - 1);
    }
    if (idSegment === "my-account" || idSegment ==="order-history")
        idSegment = "username";
    document.getElementById("nav-" + idSegment).className = "active";
}

function initParallax() {
    if (isAtHomePage()) {
        $("#parallax-1").css("height", "500px");
    }
}

function isAtHomePage() {
    if (pathname === "/custa/" || pathname === "/")
        return true;
    else
        return false;
}

function initContainerHeight() {
    var topHeight = $("#parallax-1").height();
    var btmHeight = $("#footer").height();
    var windowHeight = $(document).height();
    var diff = windowHeight - topHeight - btmHeight;
    if (diff > 0)
        $("#base-container").css("min-height", diff + "px");
}
