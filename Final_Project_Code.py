#Developer - Dhairya Parikh
# Import required libraries, including python-requests 
import sys, time, requests, json
import pygatt
import geocoder
import struct

BLE_ADDRESS = '00:60:37:0A:06:2F'  #NXP device mac address
adapter = pygatt.GATTToolBackend()  #bluetooth adapter creation
locate = geocoder.ip('me')    #obtain location data from internet
locate1 = locate.latlng    #latitude and longitude data
        
print "Starting sensor value measurement! Press Ctrl+C to stop this script."
time.sleep(1)

adapter.start()     #Starting the BLE Adapter
device = adapter.connect("00:60:37:0A:06:2F")     #connect to the Rapid IoT prototying kit

while True:      #Loop to continuously fetch the vallues

    # Value fetching, can be done with a loop too but I did this for easy interpretation
        
    light_initial = device.char_read("1493dd8e-8c3e-4e79-a4ff-6f0cd50005f9")    #Ambient Light Value in bytearray     
    temp_initial = device.char_read("1493dd8e-8c3e-4e76-a4ff-6f0cd50005f9")    #Temperature Value in bytearray
    humidity_initial = device.char_read("1493dd8e-8c3e-4e77-a4ff-6f0cd50005f9")  #Humidity Value in bytearray
    air_initial = device.char_read("1493dd8e-8c3e-4e75-a4ff-6f0cd50005f9")      #Air Quality Value in bytearray
    pressure_initial = device.char_read("1493dd8e-8c3e-4e78-a4ff-6f0cd50005f9")  #Pressure Value in bytearray
    battery_initial = device.char_read("964bf77c-9f4d-4b27-9340-7eb81c1dfbd5")   #Battery Level value in bytearray
    state_initial = device.char_read("964bf77c-9f4d-4b27-9340-7eb81c1dfbd6")    #Charging state value in bytearray

    # Location information
    lat = locate1[0]
    lon = locate1[1]
    #converting bytearray to normal value and accessing the actual value(in Tuple)
        
    light_value = struct.unpack('i',light_initial)     
    light_value1 = light_value[0]     

    temp_value = struct.unpack('f',temp_initial)
    temp_value1 = temp_value[0]
    temp_value1 = round(temp_value1, 2)

    humidity_value = struct.unpack('f',humidity_initial)
    humidity_value1 = humidity_value[0]
    humidity_value1 = round(humidity_value1, 2)

    air_value = struct.unpack('i',air_initial)
    air_value1 = air_value[0]

    pressure_value = struct.unpack('i',pressure_initial)
    pressure_value1 = pressure_value[0]
        
    
    loop_start_time = time.time()
            
    if True:
            
        print "--------UQM - The Urban Quality Monitoring Device---------------"
        print "--------------- Rapid IoT Sensor Values-------------------------"
                
        print "Ambient Light Value:"+str(light_value1)
        print "Temperature Light Value:"+str(temp_value1)
        print "Humidity Value:"+str(humidity_value1)
        print "Air Quality Value(TVOC):"+str(air_value1)
        print "Pressure Value:"+str(pressure_value1)
        print "----------------------------------------------------------------"
                
    # Set the HTTP request header and payload content
    headers = {"Content-Type": "application/json"}

    payload = {
                  "Ambient Light Value": light_value1,
                  "Temperature" : temp_value1,
                  "Humidity" : humidity_value1,
                  "Air Quallity(ppm)" : air_value1,
                  "Pressure" : pressure_value1,
                  "coordinates" :
                   {
                        "Latitude" : lat,
                        "Longitude" : lon
                   }
               }

     # Send the HTTP request to Harvest
    print "Sending data %s to Funnel..." % (json.dumps(payload))
    try:
        response = requests.post("http://unified.soracom.io", data=json.dumps(payload), headers=headers, timeout=5)
    except requests.exceptions.ConnectTimeout:
        print "Error: Connection timeout. Is the modem connected?"

    # Display HTTP request response
    if response.status_code == 201:
        print "Response 201: Success!"
    elif response.status_code == 400:
        print "Error 400: Harvest did not accept the data. Is Harvest enabled?"
    time.sleep(3)

sys.exit(1)
