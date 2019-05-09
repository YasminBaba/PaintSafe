# PaintSafe

PaintSafe is an embedded system that has been marketed towards professional painters. It measures total volatile organics compounds every 5 seconds using air quality and temperature sensors. Via our website, which is additonallly our marketing website, users are able to set up their sensor. Depending on what type of ventilation system they have and which VOCs are present in their paint, they will recieve notifications to turn on their ventilation system when the level of VOC has been above their personalised threshold for some time. Ideally, PaintSafe would be able to connect to smart ventilation systems and turn it on for them. 

In this repository you will find our python code used our raspberry pi in addition to the code for our website. Open the 'HomePage.html' on your browser to view our marketing page and explore the different pages to grasp what PaintSafe is about. Finally, connect your sensor to the broker using test.mosquitto.org. If it cannot connect, you can change the code in the FormAndSensorData.html file to another broker (ee-estott-octo.ee.ic.ac.uk). Moreover, on this same page, you will find our topic, IC.embedded/leshabibis/1. Again, if need be this can be easily changed. 

Without the pi, test it out using: http://www.hivemq.com/demos/websocket-client/? with the format: {"TVOC": 700, "CO2": 900}.
