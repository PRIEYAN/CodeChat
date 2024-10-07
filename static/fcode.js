
function room() {
    var chatCode = document.getElementById('fcode').value;
    if (chatCode) {
        window.location.href = "room";
    } else {
        alert("Please enter a chat code.");
    }
}