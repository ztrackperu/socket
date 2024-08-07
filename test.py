import socket
import json
import requests
import os
import datetime
import pymongo

localIP     = '192.168.1.166'
localPort   = 5050
bufferSize  = 4096 #1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

def isNumerico(s):
        try:
            float(s)
            return True
        except ValueError:
           return False
def generarJson(campos,datos):
        if(len(datos) == len(campos)) :
            jsonTrama ='''{'''
            for x in range(0,len(datos)):
                if(isNumerico(datos[x])==True):
                    optimizado =float(datos[x])
                    optimizado1 =str(optimizado)
                    jsonTrama += '''"'''+campos[x] +'''": '''+optimizado1+''','''
                else:
                    jsonTrama += '''"'''+campos[x] +'''": "'''+datos[x]+'''",'''
            jsonTrama = jsonTrama[:-1]
            jsonTrama +='''}'''
            tratado = json.loads(jsonTrama) 
            return tratado      
        else:
            return "error con los arreglos ,no son de la misma longitud" 

def generarJson1(campos,datos):
        if(len(datos) == len(campos)) :
            jsonTrama ='''{'''
            for x in range(0,len(datos)):
                if(isNumerico(datos[x])==True):
                    jsonTrama += '''"'''+campos[x] +'''": '''+datos[x]+''','''
                else:
                    jsonTrama += '''"'''+campos[x] +'''": "'''+datos[x]+'''",'''
            jsonTrama = jsonTrama[:-1]
            jsonTrama +='''}'''
            tratado = jsonTrama
            return tratado      
        else:
            return "error con los arreglos ,no son de la misma longitud" 
def enviarApi(url,myobj):
        try :
            x = requests.post(url, json = myobj)
           
            return x.text             
        except:
               print("error de trama ")  
while(True):
    message = ""
    address = ""
    clientMsg = ""
    clientIP  = ""
    mensaje_completo = ""

    #INICIO PARA PETICION DE DATOS:
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        mensaje_completo = str(clientMsg)
        mensaje_completo = mensaje_completo.replace('Message from Client:b', '')
        #print(mensaje_completo)
        mensaje_completo = mensaje_completo.replace('\'', '')
        mensaje_completo = mensaje_completo.replace('\\', '')
        texto_ideal=mensaje_completo
        cadena_esperada = "1BA2"
        cadena_termo = "THERMOKING"
        if((cadena_esperada in texto_ideal) and (cadena_termo in texto_ideal) ) :
            cadena_array = texto_ideal.split(cadena_esperada)
            if(cadena_array[0]!=""):
                texto_ideal= "1BA2"+cadena_array[1]
            total_comas = texto_ideal.split(",")
            contador_elementos = len(total_comas)
            if(contador_elementos==70):
                if(total_comas[69]==""):
                    total_comas[69] =-1
            if(contador_elementos!=70):
                if(total_comas[contador_elementos-1]==""):
                    total_comas[contador_elementos-1] =-1
                i=1
                while contador_elementos <70 :
                    total_comas.append(-1)
                    contador_elementos += 1
            cadena =""
            for n in total_comas :
                cadena += str(n)+","
            cadena = cadena[:-1]
            mensaje_completo = cadena


        else :
            print("trama complicada ")

    except:
        print('Posible error')
        mensaje_completo = ""
        mensaje = ""
    print('----------------------')
    print('Trama recibida: ')
    print(mensaje_completo)
    #hora_actual = datetime.datetime.now()
    #print(hora_actual)
    #fetch1 = str(hora_actual).split(".")
    #fecha_ja =fetch1[0]
    #mensaje_completo2 = mensaje_completo+"#"+fecha_ja
    campos2 ="cadena#fecha_socket"
    separador2 ="#"
    #with open("registrodatazos.txt","a+") as file:
        #file.write(mensaje_completo2 +"\n")
    # \
    #mensaje1 = enviarApi('http://161.132.206.104/api/',generarJson(campos2.split(separador2),mensaje_completo2.split(separador2)))
    conError = '\\'
    validarError = mensaje_completo.find(conError)
    if(validarError != -1):
        mensaje_completo = '1B100000,15,20'

    separador =","
    evaluador =mensaje_completo.split(separador)
    #ajas = mensaje_completo
    #if(ajas[-1]=="*"):
        #mensaje_completo = mensaje_completo[:-1]
    if (evaluador[0]=="1CR" or evaluador[0]=="1CR1" or evaluador[0]=="1CR2" or evaluador[0]=="1CR3"):
        #print("olaolllllllllllllllllllllllllllllllllllllllllllllllllllll")
        #with open("registrot.txt","a+") as file:
            #file.write(mensaje_completo +"\n")
        with open("reserva-wonderful.txt","a+") as file:
           file.write(mensaje_completo +"\n")
        print(mensaje_completo)
        mensaje1 = enviarApi('http://161.132.206.104:9020/maduradores/Wonderful/',{"data":mensaje_completo})
        if(evaluador[0]=="1CR" or evaluador[0]=="1CR1" or evaluador[0]=="1CR2"):
            dat ="ok"
            sex =evaluador[2]
            sex1=sex.split('|')
            sex2=sex1[0]
            if(sex2=="ZGRU2008220"):
                data="(POWEROFF) "
                datSP ="SPTEMP(4)"
        else:
            dat ="Sin comandos pendientes"
            sex =evaluador[2]
            sex1=sex.split('|')
            sex2=sex1[0]
            if(sex2=="ZGRU2008220" or sex2=="ZGRU1090804" or sex2=="ZGRU2232647" or sex2=="ZGRU2009227" or sex2=="TEST202411"):
              datsx="(POWERON)"
              datTT="DFROST"
              datzz="SPTEMP(21.9)"
              dathh="SPHUM(90)"
              datcc="SPCO2(2.2)"
            else :
              datAA="sin comandos"
            datXX="(POWEROFF) "
            datCO2 ="SPCO2(3)"
            dattta ="SPETI(0)"
            datxx = "SPTEMP(22)"
            datrr="SPHUM(88)"
        mensaje = dat
        print(mensaje)

    elif(evaluador[0]=="TUNEL"):
        #with open("registro_tunel.txt","a+") as file:
            #file.write(mensaje_completo +"\n")
        mensaje ="FAIL"
        if(evaluador[2]=='HORTIFRUIT:1A'):
            mensaje1 = enviarApi('http://161.132.206.104:9020/tunel/Hortifruit',{"data":mensaje_completo})
            mensaje ="ok"
        print(mensaje)
    elif(evaluador[0]=="1TC2"):
        mensaje1 = enviarApi('http://161.132.206.104:9020/maduradores/Tunel/',{"data":mensaje_completo})
        mensaje ="ok"
        print(mensaje)

    elif(evaluador[0]=="1B50"):
        print('TRAMA GENSET')
        #campos que vienen con la trama 10 /5 = 15
        camposGenset = "1B,nombre_contenedor,horometro,engine_state,speed,eco_power,unit_mode,voltage_measure,battery_voltage,water_temp,"
        camposGenset += "running_frequency,fuel_level,latitud,longitud,fecha_genset,"
        #agregamos datos manuales a la trama 10/1 =11
        camposGenset +="tipo,rotor_current,fiel_current,rpm,alarma_id,evento_id,modelo,set_point,temp_supply_1,return_air,"
        camposGenset += "reefer_conected"
        mensaje_completo += "Generador,0,0,0,0,0,SG+,0,0,0,"
        mensaje_completo += "-"    
        print(generarJson1(camposGenset.split(separador),mensaje_completo.split(separador)))
        #mensaje = enviarApi('http://locarlhost/ztrack1/api/genset/genset1.php',generarJson(camposGenset.split(separador),mensaje_completo.split(separador)))
        mensaje1 = enviarApi('http://161.132.206.104/ztotal/api/genset/genset1.php',generarJson(camposGenset.split(separador),mensaje_completo.split(separador)))
        #print(mensaje)
        #print(mensaje1)
        # =mensaje+
        mensaje = "ola"
        print(mensaje1)

    elif (evaluador[0]=="1B01"):
        print('TRAMA REEFER')
        #campos que vienen con la trama 10/10/1 =21
        camposRefeer = "1B,tipo,nombre_contenedor,set_point,temp_supply_1,return_air,evaporation_coil,ambient_air,cargo_1_temp,cargo_2_temp,"
        camposRefeer += "cargo_3_temp,cargo_4_temp,relative_humidity,alarm_present,alarm_number,controlling_mode,power_state,defrost_term_temp,defrost_interval,latitud,"
        camposRefeer +="longitud"
        #agregamos datos manuales a la trama 
        
        #mensaje = enviarApi('http://localhost/ztrack1/api/reefer/',generarJson(camposRefeer.split(separador),mensaje_completo.split(separador))) 
        mensaje1 = enviarApi('http://161.132.206.104/ztotal/api/reefer/',generarJson(camposRefeer.split(separador),mensaje_completo.split(separador))) 
        #print(mensaje)
        #print(mensaje1)
        mensaje =mensaje1
        print(mensaje)
        
    elif (evaluador[0]=="1B02"):
        print('TRAMA DE MADURADOR: ')
        #campos que vienen con la trama 10/10/10/10/10/10/7 =67
        camposMadurador = "B1,tipo,nombre_contenedor,set_point,temp_supply_1,temp_supply_2,return_air,evaporation_coil,condensation_coil,compress_coil_1,"
        camposMadurador += "compress_coil_2,ambient_air,cargo_1_temp,cargo_2_temp,cargo_3_temp,cargo_4_temp,relative_humidity,avl,suction_pressure,discharge_pressure,"
        camposMadurador += "line_voltage,line_frequency,consumption_ph_1,consumption_ph_2,consumption_ph_3,co2_reading,o2_reading,evaporator_speed,condenser_speed,"
        camposMadurador += "power_kwh,power_trip_reading,suction_temp,discharge_temp,supply_air_temp,return_air_temp,dl_battery_temp,dl_battery_charge,power_consumption,"
        camposMadurador += "power_consumption_avg,alarm_present,capacity_load,power_state,controlling_mode,humidity_control,humidity_set_point,fresh_air_ex_mode,fresh_air_ex_rate,fresh_air_ex_delay,"
        camposMadurador += "set_point_o2,set_point_co2,defrost_term_temp,defrost_interval,water_cooled_conde,usda_trip,evaporator_exp_valve,suction_mod_valve,hot_gas_valve,economizer_valve,"
        camposMadurador += "ethylene,stateProcess,stateInyection,timerOfProcess,battery_voltage,power_trip_duration,modelo,latitud,longitud"
        #agregamos datos manuales a la trama 
        camposMadurador += ",defrost_prueba,ripener_prueba"
        mensaje_completo += ",2,2"
        #battery_voltage,power_trip_duration,
        print(generarJson1(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #mensaje = enviarApi('http://localhost/ztrack1/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        mensaje1 = enviarApi('http://161.132.206.104/ztotal/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #print(mensaje)
        #print(mensaje1)
        mensaje =mensaje1
        print(mensaje)
    # Sending a reply to cliente
    elif (evaluador[0]=="1B92"):
        print('TRAMA DE MADURADOR: ')
        #campos que vienen con la trama 10/10/10/10/10/10/7 =67
        camposMadurador = "B1,tipo,nombre_contenedor,set_point,temp_supply_1,temp_supply_2,return_air,evaporation_coil,condensation_coil,compress_coil_1,"
        camposMadurador += "compress_coil_2,ambient_air,cargo_1_temp,cargo_2_temp,cargo_3_temp,cargo_4_temp,relative_humidity,avl,suction_pressure,discharge_pressure,"
        camposMadurador += "line_voltage,line_frequency,consumption_ph_1,consumption_ph_2,consumption_ph_3,co2_reading,o2_reading,evaporator_speed,condenser_speed,"
        camposMadurador += "power_kwh,power_trip_reading,suction_temp,discharge_temp,supply_air_temp,return_air_temp,dl_battery_temp,dl_battery_charge,power_consumption,"
        camposMadurador += "power_consumption_avg,alarm_present,capacity_load,power_state,controlling_mode,humidity_control,humidity_set_point,fresh_air_ex_mode,fresh_air_ex_rate,fresh_air_ex_delay,"
        camposMadurador += "set_point_o2,set_point_co2,defrost_term_temp,defrost_interval,water_cooled_conde,usda_trip,evaporator_exp_valve,suction_mod_valve,hot_gas_valve,economizer_valve,"
        camposMadurador += "ethylene,stateProcess,stateInyection,timerOfProcess,battery_voltage,power_trip_duration,modelo,latitud,longitud,sp_ethyleno"
        #agregamos datos manuales a la trama 
        camposMadurador += ",defrost_prueba,ripener_prueba"
        mensaje_completo += ",2,2"
        #battery_voltage,power_trip_duration,
        print(generarJson1(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #print(generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #mensaje = enviarApi('http://localhost/ztrack1/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        mensaje1 = enviarApi('http://161.132.206.104/ztotal/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #print(mensaje)
        #print(mensaje1)
        mensaje =mensaje1
        print(mensaje)
    # Sending a reply to cliente


    elif (evaluador[0]=="1BA2" or evaluador[0]=="1BZ2" ):
        print('TRAMA DE MADURADOR: ')
        #campos que vienen con la trama 10/10/10/10/10/10/7 =67

        #nombre = len(evaluador[2])

        #madurar = mensaje_completo.split(separador)
        #if(nombre>14):
          #  print("pasaa")
          #  madurar[2]="error"

        if(len(mensaje_completo)>15):
            nombre = len(evaluador[2])

            madurar = mensaje_completo.split(separador)
            if(nombre>14):
                print("pasaa")
                mensaje_completo="1BA2,Madurador,error,-30.00,-13.50,-3277.00,-3.10,-3.40,34.80,65.40,-3276.90,23.20,20.20,-38.50,-38.50,-38.50,91.00,0.00,3276.60,3276.60,442.00,60.00,11.00,10.80,10.20,25.40,3276.60,30.00,100.00,98676.70,8563.00,3276.60,3276.60,6540.10,6550.50,0.16,0.00,6.54,3.92,0,100.00,1,1,0,254,0,32766.00,3276.60,3276.60,3276.60,18.00,6.00,0,0,255.00,255.00,255.00,255.00,320.00,3,0,10,0.00,0.00,THERMOKING,0.00,0.00,100,-1,-1"
        
            camposMadurador = "B1,tipo,nombre_contenedor,set_point,temp_supply_1,temp_supply_2,return_air,evaporation_coil,condensation_coil,compress_coil_1,"
            camposMadurador += "compress_coil_2,ambient_air,cargo_1_temp,cargo_2_temp,cargo_3_temp,cargo_4_temp,relative_humidity,avl,suction_pressure,discharge_pressure,"
            camposMadurador += "line_voltage,line_frequency,consumption_ph_1,consumption_ph_2,consumption_ph_3,co2_reading,o2_reading,evaporator_speed,condenser_speed,"
            camposMadurador += "power_kwh,power_trip_reading,suction_temp,discharge_temp,supply_air_temp,return_air_temp,dl_battery_temp,dl_battery_charge,power_consumption,"
            camposMadurador += "power_consumption_avg,alarm_present,capacity_load,power_state,controlling_mode,humidity_control,humidity_set_point,fresh_air_ex_mode,fresh_air_ex_rate,fresh_air_ex_delay,"
            camposMadurador += "set_point_o2,set_point_co2,defrost_term_temp,defrost_interval,water_cooled_conde,usda_trip,evaporator_exp_valve,suction_mod_valve,hot_gas_valve,economizer_valve,"
            camposMadurador += "ethylene,stateProcess,stateInyection,timerOfProcess,battery_voltage,power_trip_duration,modelo,latitud,longitud,sp_ethyleno,horas_inyeccion,pwm_inyeccion"
            # condicon especial para madurador ocn codigo ZGRU1263532
            my_list = mensaje_completo .split(",")
            #rint(my_list[2])
            #contador_lista =len(my_list)
            #if(contador_lista> 2):
                #if(my_list[2]=="ZGRU1263532") :
                    #mensaje_completo += ",0,0"
                #if(my_list[2]=="ZGRU1090804") :
                    # mensaje_completo += "0"
                
            # hay una variacion en el contenedor de usa ZGRU2232647
            #if(my_list[2]=="ZGRU2232647") :
                #mensaje_completo += ",0"
                
                
            #agregamos datos manuales a la trama 
            camposMadurador += ",defrost_prueba,ripener_prueba"
            mensaje_completo += ",2,2"
            #battery_voltage,power_trip_duration,
            #print(mensaje_completo )
            #print(generarJson1(camposMadurador.split(separador),madurar))
            #print(generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))


            #campos2 ="cadena#fecha_socket"
            #separador2 ="#"
            #mensaje1 = enviarApi('http://161.132.206.104/api/',generarJson(campos2.split(separador2),mensaje_completo2.split(separador2)))
            #mensaje = enviarApi('http://localhost/ztrack1/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
            mensaje1 = enviarApi('http://161.132.206.104/ztotal/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
            #print(mensaje)
            #print(mensaje1)
            #print(generarJson1(camposMadurador.split(separador),mensaje_completo.split(separador)))
            #mensaje1 ="RESET"
            #print(mensaje)
            #print(mensaje1)
            mensaje =mensaje1
            mensaje = "RESET"
            print(mensaje)
        else :
            mensaje = "error terrible en 1BA2"
        #print(mensaje1)
    # Sending a reply to cliente

    elif (evaluador[0]=="1BC2"):
        print('TRAMA DE MADURADOR: ')
        #campos que vienen con la trama 10/10/10/10/10/10/7 =67
        camposMadurador = "B1,tipo,nombre_contenedor,set_point,temp_supply_1,temp_supply_2,return_air,evaporation_coil,condensation_coil,compress_coil_1,"
        camposMadurador += "compress_coil_2,ambient_air,cargo_1_temp,cargo_2_temp,cargo_3_temp,cargo_4_temp,relative_humidity,avl,suction_pressure,discharge_pressure,"
        camposMadurador += "line_voltage,line_frequency,consumption_ph_1,consumption_ph_2,consumption_ph_3,co2_reading,o2_reading,evaporator_speed,condenser_speed,"
        camposMadurador += "power_kwh,power_trip_reading,suction_temp,discharge_temp,supply_air_temp,return_air_temp,dl_battery_temp,dl_battery_charge,power_consumption,"
        camposMadurador += "power_consumption_avg,alarm_present,capacity_load,power_state,controlling_mode,humidity_control,humidity_set_point,fresh_air_ex_mode,fresh_air_ex_rate,fresh_air_ex_delay,"
        camposMadurador += "set_point_o2,set_point_co2,defrost_term_temp,defrost_interval,water_cooled_conde,usda_trip,evaporator_exp_valve,suction_mod_valve,hot_gas_valve,economizer_valve,"
        camposMadurador += "ethylene,stateProcess,stateInyection,timerOfProcess,battery_voltage,power_trip_duration,modelo,latitud,longitud,sp_ethyleno,horas_inyeccion,pwm_inyeccion"
        #agregamos datos manuales a la trama 
        camposMadurador += ",defrost_prueba,ripener_prueba"
        mensaje_completo += ",0,0,2,2"
        #battery_voltage,power_trip_duration,
        #print(generarJson1(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #print(generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #mensaje = enviarApi('http://localhost/ztrack1/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        mensaje1 = enviarApi('http://161.132.206.104/ztotal/api/madurador/',generarJson(camposMadurador.split(separador),mensaje_completo.split(separador)))
        #print(mensaje)
        #print(mensaje1)
        mensaje1 =mensaje1
        print(mensaje)
    # Sending a reply to cliente  
    elif (evaluador[0]=="1B30"):
        print('Prueba de Trama')
        camposPrueba = "ID"
        mensaje = enviarApi('http://localhost/ztrack1/api/prueba/',generarJson(camposPrueba.split(separador),mensaje_completo.split(separador)))
        print(mensaje)
    
    elif (evaluador[0]=="2F"):
        print('Comunicacion GENSET .')
        camposPrueba = "ID,IMEI,partes,crc,fin"
        mensaje = enviarApi('http://localhost/ztrack3/api/c_genset/',generarJson(camposPrueba.split(separador),mensaje_completo.split(separador)))
        print(mensaje)

    elif (evaluador[0]=="1B"):
        print('Recibiendo Tramas ...')
        camposPrueba = "ID,IMEI,parte,informacion,crc,fin"
        mensaje = enviarApi('http://localhost/ztrack3/api/p_genset/',generarJson(camposPrueba.split(separador),mensaje_completo.split(separador)))
        print(mensaje)
    
    elif (evaluador[0]=="1C"):
        print('TRAMA ENEL')
        #campos que vienen con la trama 10 /5 = 15
        camposEnel = "1B,dato1,dato2,dato3"
        #camposEnel += "running_frequency,fuel_level,latitud,longitud,fecha_genset,"
        #agregamos datos manuales a la trama 10/1 =11
        #camposEnel +="tipo,rotor_current,fiel_current,rpm,alarma_id,evento_id,modelo,set_point,temp_supply_1,return_air,"
        #camposEnel += "reefer_conected"
        #mensaje_completo += "Generador,0,0,0,0,0,SG+,0,0,0,"
        #mensaje_completo += "-"    
        print(generarJson(camposEnel.split(separador),mensaje_completo.split(separador)))
        mensaje = enviarApi('http://localhost/ztrack1/api/enel/index.php',generarJson(camposEnel.split(separador),mensaje_completo.split(separador)))
        print(mensaje)

    else :
        print("TRAMA NO CLASIFICADA")
        mensaje = "TRAMA NO CLASIFICADA"
    #print(mensaje1)
    zetas = str.encode(mensaje)
    print(clientIP)
    #bytesToSend = bytesToSend.mensaje
    try:
       UDPServerSocket.sendto(zetas, address)
    except:
       print("error de datos")
       SystemError
 
