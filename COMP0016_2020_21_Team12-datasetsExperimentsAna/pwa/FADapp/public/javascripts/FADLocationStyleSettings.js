function changeHeaderColor() {
    var headerStyles = document.getElementsByTagName("header").item(0).style;
    var selectedColour = document.getElementById("header-color-selector").value;
    headerStyles.setProperty('background-color', selectedColour);
    console.log("change color");
}