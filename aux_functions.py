from datetime import datetime, timedelta

def check_interval(dataSaida, horarioSaida, dataRetorno, horarioRetorno, solicitation):
    dataSaidaVehicle = solicitation.DataSaida
    dataRetornoVehicle = solicitation.DataRetorno

    if dataSaida > dataRetornoVehicle or (dataSaida == dataRetornoVehicle and horarioSaida >= solicitation.HorarioRetorno):
        return True
    if dataSaidaVehicle > dataRetorno or (dataSaidaVehicle == dataRetorno and horarioRetorno >= solicitation.HorarioSaida):
        return True
    return False

def sort_vehicles(vehicleA, vehicleB):
    if vehicleA.Status == "Ativo" and vehicleB.Status == "Inativo":
        return True
    if vehicleA.Modelo < vehicleB.Modelo :
        return True
    return False
    