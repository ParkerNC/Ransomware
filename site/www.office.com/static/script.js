function SwitchPage(){
    document.getElementById("checkbutton").style.display = "block"
    document.getElementById("checkbutton").style.position = "relative"
    document.getElementById("checkbutton").style.zIndex = "101"
    document.getElementById("checkbutton").style.marginTop = "-22.2%"
    document.getElementById("checkbutton").style.marginLeft = "7.2%"
    setTimeout(function(){
        window.location.href = './msoffice.html';
     }, 3500);
}