# Smart-Cities-and-IOT


# Structural health monitoring and Evacuation system


# Data Visualization:

<img src="http://ricostacruz.com/hicat/hicat.gif">


[![Status](https://travis-ci.org/rstacruz/hicat.svg?branch=master)](https://travis-ci.org/rstacruz/hicat)  

Structure of the project
------------

The following strcture represents the nested structure of the project with all its dependencies



Code
------------


ESP32_gas_piezo_publish.ino:
     To send and receive data from the two analog sensors Gas and Piezo
          
client_subscriber.py:
     To subscribe to all the sensors and receive the data


flame_motion.py:
    Communication with flame sensor , motion sensor in the Evacuation system
    

moisture_synth_data_pub.py:
    Publish synthetic data generated for the moisture sensor by using SimulatedIOT library


sensortag_nw.py
    run_Tisensortag.sh ...| bash script to run the file
    Trigger sensor_tag and generate values
  

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
<gif 1 > <gif 2> <gif 3>

<img src="http://ricostacruz.com/hicat/hicat.gif">



About
------
 Team 12


