//initialise parralax height
$(document).ready(function () {
    $('.parallax').parallax();
    if (!isAtHomePage()) {
        initContainerHeight();
    }
});
var pathname = window.location.pathname;
M.AutoInit();  //init materialize
initNavbar();
initParallax();


//initialise navbar's different active components depend on the url of the current page
function initNavbar() {
    var idSegment = "";
    if (isAtHomePage()) {
        idSegment = "index";
    } else {
        idSegment = pathname.substring(7, pathname.length - 1);
    }
    if (idSegment === "my-account" || idSegment === "order-history")
        idSegment = "username";
    document.getElementById("nav-" + idSegment).className = "active";
}

// initialise corresponding parallax height for home page
function initParallax() {
    if (isAtHomePage()) {
        $("#parallax-1").css("height", "500px");
    }
}

// check if home page
function isAtHomePage() {
    if (pathname === "/custa/" || pathname === "/")
        return true;
    else
        return false;
}

//initialise the height of each page in case there is not enough content to fulfill the page
function initContainerHeight() {
    var topHeight = $("#parallax-1").height();
    var btmHeight = $("#footer").height();
    var windowHeight = $(document).height();
    //calculate height difference and append it later into the DOM styling
    var diff = windowHeight - topHeight - btmHeight;
    if (diff > 0)
        $("#base-container").css("min-height", diff + "px");
}
//when the toast vanishes, redirect the page to login
function noticeLogin(loginUrl) {
    M.toast({
        html: 'You need to login first! Direct you to login in 3 seconds...',
        completeCallback: function () {
            window.location.replace(loginUrl);
        },
        // set the time of the toast staying
        displayLength: 2200
    },);
}