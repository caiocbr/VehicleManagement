from datetime import datetime, timedelta

def check_interval(dataSaida, horarioSaida, dataRetorno, horarioRetorno, solicitation):
    #dataSaida = datetime.strptime(dataSaida, "%Y-%M-%D")
    #dataRetorno = datetime.strptime(dataSaida, "%Y-%M-%D")
    dataSaidaVehicle = solicitation.DataSaida
    dataRetornoVehicle = solicitation.DataRetorno

    if dataSaida < dataRetornoVehicle and dataSaida >= dataSaidaVehicle:
        return False
    elif dataSaida == dataRetornoVehicle and horarioSaida < solicitation.HorarioRetorno and dataSaida >= dataSaidaVehicle:
        return False
    elif dataRetorno <= dataRetornoVehicle and dataRetorno > dataSaidaVehicle:
        return False
    elif dataRetorno <= dataRetornoVehicle and horarioRetorno > solicitation.HorarioSaida and dataRetorno >= dataSaidaVehicle:
        return False
    else:
        return True

def sort_vehicles(vehicleA, vehicleB):
    if vehicleA.Status == "Ativo" and vehicleB.Status == "Inativo":
        return True
    if vehicleA.Modelo < vehicleB.Modelo :
        return True
    return False
    