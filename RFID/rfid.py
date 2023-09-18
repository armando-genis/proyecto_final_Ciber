import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import time

def hex_array_str(arr):
    my_str = ""
    for i in range(len(arr)):
        val = arr[i]
        if val < 16:
            my_str = my_str + "0"
        my_str = my_str + str('{0:x}'.format(arr[i])) + " "
    return my_str

def hex_to_text(hex_str):
    try:
        byte_data = bytes.fromhex(hex_str)
        text_data = byte_data.decode('utf-8')
        return text_data
    except UnicodeDecodeError:
        return "No se pudo decodificar como texto"

key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

MIFAREReader = MFRC522()
block_num = 1

block_num1 = 12
block_num2 = 13
block_num3 = 14

dato_str_nom = str("45515549504f20332054454320434942")
dato_str_inv = str("494e56454e544152494f202020202020")
dato_str_can = str("43414e5449444144202020202020200a")

mensaje_impreso = False

data = []
data2 = []
data3 = []
continue_reading = True
input_valid = False

# Data read        
backdata = []

try:
    while True:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print("¡Tag detectado!")
            mensaje_impreso = False
        elif not mensaje_impreso:
            print("Acerque el tag al lector")
            mensaje_impreso = True

        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print("UID del tag: %s %s %s %s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))

            MIFAREReader.MFRC522_SelectTag(uid)
            
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num, key, uid)
            
            if status == MIFAREReader.MI_OK:
                backdata = MIFAREReader.MFRC522_Read(block_num)
                
                if backdata is not None:
                    hex_str = hex_array_str(backdata)
                    print("El bloque " + str(block_num) + " tiene el dato en hexadecimal: " + hex_array_str(backdata))
                    text_data = hex_to_text(hex_str)
                    print("Texto decodificado: " + text_data)
                    if "Equipo 3 TEC CIB" in text_data:
                        print("Estación encontrada, escribiendo en los sectores correspondientes.")
                                        # Agregar un retraso antes de la siguiente lectura
                        time.sleep(2)
                        MIFAREReader.MFRC522_StopCrypto1()
                        while not(input_valid):
                            # Input block number
                            backdata = []
                            input_valid = True
                            if (block_num1 + 1)%4 == 0:
                                print("¡El Sector Trailer " + str(block_num1//4) + " no se debe modificar!")
                                input_valid = False

                        input_valid = False
                        while not(input_valid):
                            # Input data number
                            if len(dato_str_nom) != 32:
                                print("¡El dato a escribir debe tener 32 caracteres hex!")
                                input_valid = False
                            else:
                                for i in range(0, len(dato_str_nom), 2):
                                    data.append(int(dato_str_nom[i:i+2],16))
                                input_valid = True
                        
                        while continue_reading:

                            # Scan for cards    
                            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                                # Get the UID of the card
                            (status,uid) = MIFAREReader.MFRC522_Anticoll()
                            

                            # If we have the UID, continue
                            if status == MIFAREReader.MI_OK:
                                
                                # Select the scanned tag
                                MIFAREReader.MFRC522_SelectTag(uid)

                                # Authenticate
                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num1, key, uid)

                                # Check if authenticated
                                if status == MIFAREReader.MI_OK:
                                    
                                    # Write the data
                                    MIFAREReader.MFRC522_Write(block_num1, data)
                                    
                                    print("¡Escritura exitosa al bloque %s!" % block_num1)

                                    # Check to see if it was written
                                    backdata = MIFAREReader.MFRC522_Read(block_num1)
                                    
                                    if backdata != None:
                                        hex_str = hex_array_str(backdata)
                                        print("Ahora el bloque " + str(block_num1) + " tiene el dato: " + hex_array_str(backdata))
                                        text_data = hex_to_text(hex_str)
                                        print(text_data)
                                    else:
                                        print("¡No se pudo verificar lectura del bloque!")            


                                    # Make sure to stop reading for cards
                                    continue_reading = False
                                    
                                else:
                                    print("Error de autentificación")
                                    
                        continue_reading = True
                        MIFAREReader.MFRC522_StopCrypto1()
                        backdata = []
                        while not(input_valid):
                            # Input block number
                            backdata = []
                            input_valid = True
                            if (block_num2 + 1)%4 == 0:
                                print("¡El Sector Trailer " + str(block_num2//4) + " no se debe modificar!")
                                input_valid = False

                        input_valid = False
                        while not(input_valid):
                            # Input data number
                            if len(dato_str_inv) != 32:
                                print("¡El dato a escribir debe tener 32 caracteres hex!")
                                input_valid = False
                            else:
                                for i in range(0, len(dato_str_inv), 2):
                                    data2.append(int(dato_str_inv[i:i+2],16))
                                input_valid = True
                        
                        while continue_reading:

                            # Scan for cards    
                            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                                # Get the UID of the card
                            (status,uid) = MIFAREReader.MFRC522_Anticoll()
                            

                            # If we have the UID, continue
                            if status == MIFAREReader.MI_OK:
                                
                                # Select the scanned tag
                                MIFAREReader.MFRC522_SelectTag(uid)

                                # Authenticate
                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num2, key, uid)

                                # Check if authenticated
                                if status == MIFAREReader.MI_OK:
                                    
                                    # Write the data
                                    MIFAREReader.MFRC522_Write(block_num2, data2)
                                    
                                    print("¡Escritura exitosa al bloque %s!" % block_num2)

                                    # Check to see if it was written
                                    backdata = MIFAREReader.MFRC522_Read(block_num2)
                                    
                                    if backdata != None:
                                        hex_str = hex_array_str(backdata)
                                        print("Ahora el bloque " + str(block_num2) + " tiene el dato: " + hex_array_str(backdata))
                                        text_data = hex_to_text(hex_str)
                                        print(text_data)
                                    else:
                                        print("¡No se pudo verificar lectura del bloque!")            


                                    # Make sure to stop reading for cards
                                    continue_reading = False
                                    
                                else:
                                    print("Error de autentificación")
                        continue_reading = True
                        MIFAREReader.MFRC522_StopCrypto1()
                        backdata = []
                        while not(input_valid):
                            # Input block number
                            backdata = []
                            input_valid = True
                            if (block_num3 + 1)%4 == 0:
                                print("¡El Sector Trailer " + str(block_num3//4) + " no se debe modificar!")
                                input_valid = False

                        input_valid = False
                        while not(input_valid):
                            # Input data number
                            if len(dato_str_can) != 32:
                                print("¡El dato a escribir debe tener 32 caracteres hex!")
                                input_valid = False
                            else:
                                for i in range(0, len(dato_str_can), 2):
                                    data3.append(int(dato_str_can[i:i+2],16))
                                input_valid = True
                        
                        while continue_reading:

                            # Scan for cards    
                            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                                # Get the UID of the card
                            (status,uid) = MIFAREReader.MFRC522_Anticoll()
                            

                            # If we have the UID, continue
                            if status == MIFAREReader.MI_OK:
                                
                                # Select the scanned tag
                                MIFAREReader.MFRC522_SelectTag(uid)

                                # Authenticate
                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num3, key, uid)

                                # Check if authenticated
                                if status == MIFAREReader.MI_OK:
                                    
                                    # Write the data
                                    MIFAREReader.MFRC522_Write(block_num3, data3)
                                    
                                    print("¡Escritura exitosa al bloque %s!" % block_num3)

                                    # Check to see if it was written
                                    backdata = MIFAREReader.MFRC522_Read(block_num3)
                                    
                                    if backdata != None:
                                        hex_str = hex_array_str(backdata)
                                        print("Ahora el bloque " + str(block_num3) + " tiene el dato: " + hex_array_str(backdata))
                                        text_data = hex_to_text(hex_str)
                                        print(text_data)
                                    else:
                                        print("¡No se pudo verificar lectura del bloque!")            
                                    # Make sure to stop reading for cards
                                    continue_reading = False
                                    
                                    
                                else:
                                    print("Error de autentificación")
                        break
                        
                    else:
                        print("Esta estación no es la correcta")
                else:
                    print("¡No se pudo leer el bloque!")

                # Detener la autenticación de la tarjeta
                MIFAREReader.MFRC522_StopCrypto1()


            else:
                print("¡Error de autenticación!")

except KeyboardInterrupt:
    print("Lectura de tarjetas detenida manualmente")
finally:
    GPIO.cleanup()
