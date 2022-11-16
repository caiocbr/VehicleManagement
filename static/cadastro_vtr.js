const button = document.getElementById('SignUpButton');

button.addEventListener('click', function () {ClickButton()})

async function ClickButton(){
    response = await fetch(input='http://127.0.0.1:8000/vehicle/query');

}