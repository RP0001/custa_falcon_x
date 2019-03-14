M.AutoInit();
initNavbar();
function initNavbar() {
    var pathname = window.location.pathname;
    var idSegment = "";
    if(pathname==="/custa/" || pathname==="/"){
        idSegment = "index";
    } else {
        idSegment = pathname.substring(7,pathname.length-1);
    }
    document.getElementById("nav-"+idSegment).className = "active";
}