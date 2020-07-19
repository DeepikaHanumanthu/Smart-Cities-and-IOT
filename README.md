# Smart-Cities-and-IOT


# Structural health monitoring and Evacuation system


# Data Visualization:



Structure of the project
------------

The following structure represents the nested structure of the project with all its dependencies



Code
------------


ESP32_gas_piezo_publish.ino:
     To send and receive data from the two analog sensors Gas and Piezo
          
client_subscriber.py:
     To subscribe to all the sensors and receive the data

CrackDetection.py:
     Captures image from raspberrypi and applies image processing techniques to identify the cracks ( by the number of whitepixels ) in the image.It publishes the data to the topic crack.

flame_motion.py:
    Communication with flame sensor , motion sensor in the Evacuation system
    
moisture_synth_data_pub.py:
    Publish synthetic data generated for the moisture sensor by using SimulatedIOT library

sensortag_nw.py
    run_Tisensortag.sh ...| bash script to run the file
    Trigger sensor_tag and generate values
    
googlesheets.py
     logs the sensor data in google sheets and triggers detailed mail report with the data from all the sensors
  

PDDL
-----------

The PDDL folder contains
  --domain.pddl
      Contains the domain file with all the objects and classes 
      Defines actions to trigger the actuators
  --problem.pddl
      Defines the problem file with goals to be achieved and threshold values of the sensors
  --DataSync_PDDL
      Subscribed to all the topics to receive the sensor values
      Records data from all the sensor , sends it to domain solver and generates messages to actuate the actuators dynamically

Simulation
---
 Contains the simulation data from the software Anylogic for evacuation of people out of the building incase of any emergency situation.

Visualization
------
  Visualizes data from various sensors and plots data on the fly as Real time plots
  ![](/finalgif.gif)
  
Notes 
-----
   The automatic updation of sensor values in the problem file using a JSON file is parsed and solved only in VS code and it fails to solve in the online solver for PDDL.

About
------
 Team 12


