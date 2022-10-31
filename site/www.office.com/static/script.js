function SwitchPage(){
    document.getElementById("checkbutton").style.display = "block"
    document.getElementById("checkbutton").style.zIndex = "101"
    document.getElementById("checkbutton").style.top = "42%"
    document.getElementById("checkbutton").style.marginLeft = "2%"
    setTimeout(function(){
        window.location.href = './msoffice.html';
     }, 3500);
}