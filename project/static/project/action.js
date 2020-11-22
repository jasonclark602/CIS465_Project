function getValue (slider, id) {
  var span = document.getElementById(id);
  span.innerText = slider.value;

}


function changeInnerText(btnGray) {
  if (btnGray.innerText != "GrayScale"){
    btnGray.innerText = "GrayScale";
  }
  else {
    btnGray.innerText = "RGB";
  }
}  
