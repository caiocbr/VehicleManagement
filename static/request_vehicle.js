const button = document.getElementById('ConsultingButton');

button.addEventListener('click', function () {ClickButton()});

$("#diaSaida").change(function() {ChangeAction()});
$("#horaSaida").change(function() {ChangeAction()});
$("#diaRet").change(function() {ChangeAction()});
$("#horaRet").change(function() {ChangeAction()});
$("#inputQtdPass").change(function() {ChangeAction()});
$("#TipoViatura").change(function() {ChangeAction()});

async function ClickButton(){
    dataSaida = document.getElementById("diaSaida").value;
    horarioSaida = document.getElementById("horaSaida").value;
    dataRetorno = document.getElementById("diaRet").value;
    horarioRetorno = document.getElementById("horaRet").value;
    qtdPassageiros = document.getElementById("inputQtdPass").value;
    tipoViatura = document.getElementById("TipoViatura").value;

    var body = {
        "DataSaida": dataSaida,
        "HorarioSaida": horarioSaida,
        "DataRetorno": dataRetorno,
        "HorarioRetorno": horarioRetorno,
        "TipoViatura": tipoViatura,
        "QtdPassageiros": qtdPassageiros
    };
    response = await fetch('http://localhost:8000/vehicle/query', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });

    if(response.status == 200){
        vehicles = await response.json();

        vehiclesDiv = document.getElementById("vehiclesInformation");
        var child = vehiclesDiv.lastElementChild; 
        while (child) {
            vehiclesDiv.removeChild(child);
            child = vehiclesDiv.lastElementChild;
        }

        if(vehicles.length == 0){
            // Deleting Solicitation Button
            if(document.getElementById("solicitationButton") != null){
                document.getElementById("solicitationButton").remove();
            }

            para = document.createElement("p");
            node = document.createTextNode("Nenhum veículo disponível!");
            para.setAttribute("id", "WarningText")
            para.appendChild(node);
            vehiclesDiv.appendChild(para)
        }
        else{
            // Creating Solititation Button
            if(document.getElementById("solicitationButton") == null){
                buttonSolicitation = document.createElement("button");
                buttonSolicitation.setAttribute("type", "submit");
                buttonSolicitation.setAttribute("form", "formSolicitation")
                buttonSolicitation.setAttribute("id", "solicitationButton")
                node = document.createTextNode("Fazer Pedido");
                buttonSolicitation.appendChild(node);
                buttonSolicitation.className = "btn btn-success";
    
                buttonsDiv = document.getElementById("buttons")
                buttonsDiv.appendChild(buttonSolicitation)
            }

            label = document.createElement("label");
            node = document.createTextNode("Veículos Disponíveis:");
            label.appendChild(node);
            select = document.createElement("select");
            select.className = "form-control form-control-sm";
            select.setAttribute("name", "Viatura")

            for(var i = 0; i < vehicles.length; i++){
                para = document.createElement("option");
                node = document.createTextNode(vehicles[i]["Modelo"] + " " + vehicles[i]["Placa"]);
                para.appendChild(node);
                select.appendChild(para)
            }

            vehiclesDiv.appendChild(label);
            vehiclesDiv.appendChild(select);
        }
    }
}

function ConsultingVehicles(response){
    console.log(response);
    vehicles = response.json();
    console.log(vehicles);
    console.log(vehicles[0]);
    for(var i = 0; i < vehicles.length; i++){
        console.log(vehicles[i]);
    }
}

function ChangeAction(){
    if(document.getElementById("solicitationButton") != null){
        document.getElementById("solicitationButton").remove();
    }

    vehiclesDiv = document.getElementById("vehiclesInformation");
        var child = vehiclesDiv.lastElementChild; 
        while (child) {
            vehiclesDiv.removeChild(child);
            child = vehiclesDiv.lastElementChild;
        }
}