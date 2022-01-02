# Bebop ROS packages compilation - SLAM, configs and launches  

A compilation of differents ros packages useful for controlling and simulating a Bebop drone.  
The packages are configured for the Bebop 2, and there are slighly modifications when convenient.  
As an example, ORB SLAM 2 takes the ODOM values from Bebop and uses it to scale the map at take off. Kinda works most of the time.
There is a .launch that does this.  


[@MikeMakes](https://github.com/MikeMakes)  
[@Abathar](https://github.com/Abathar)  
[@DonDanie](https://github.com/DonDanie)  
[@franRonzalez](https://github.com/franRgonzalez)  
[@JoseRomeroF](https://github.com/JoseRomeroF)  



# Installation  
Sphinx y dependencias de BebopS: (Hasta el paso 4 inclusive de):  
https://github.com/MikeMakes/BebopS/tree/dev/sphinx#installation-instructions---ubuntu-1604-with-ros-kinetic-and-sphinx  

Copiar repo:
```
$ sudo apt-get install build-essential python-rosdep python-catkin-tools
$ git clone --recurse-submodules https://github.com/MikeMakes/bebop.git  
$ pushd bebop/src/BebopS
$ git checkout -b dev/sphinx
$ popd
```
[Probablemente no necesitais este paso] Instalar RotorS (base de BebopS), lo borraremos despues pq solo necesitamos las dependencias:  
```
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/src
$ catkin_init_workspace  # initialize your catkin workspace
$ cd ..
$ catkin init
$ git clone https://github.com/gsilano/rotors_simulator.git
$ cd ..
$ rosdep update
$ cd ~/catkin_ws
$ rosdep install --from-paths src -i
$ cd .. && rm -rf ~/catkin_ws
```
Actualizar las dependencias de nuestros repos:  
```
$ cd bebop
# Update rosdep database and install dependencies (including parrot_arsdk)
$ rosdep update
$ rosdep install --from-paths src -i
$ catkin_make
```
Then, the access permissions for the files listed in the scripts folder have to be changed. It can be done, using the commands:  
```
# To install the unbuffer command required for the script
$ sudo apt install expect
$ cd ~/bebop/src/BebopS/scripts/
# Sh script to start recording data from the Parrot-Sphinx simulator
$ sudo chmod 777 data_logger.sh
# Awk script in charge of publishing the Parrot-Sphinx simulator data
$ sudo chmod 777 data_logger_publishing.awk
```

Finally, the simulation can be performed through the commands listed below (they have to be runned in three different terminals):  
```
# A collection of nodes and programs that are pre-requisites of a ROS-based system
$ roscore
```

```
# Sh script to enable the publication of the data logger
$ rosrun bebop_simulator data_logger.sh
```

```
# Hovering example
$ roslaunch bebop_simulator task1_world_with_sphinx.launch
# Trajectory tracking example
$ roslaunch bebop_simulator task2_world_with_sphinx.launch
```

# Docs
Más links https://github.com/topics/bebop2  
PlotJuggler https://github.com/facontidavide/PlotJuggler  
rqt_image_view http://wiki.ros.org/rqt_image_view  
Parrot-Sphinx Simulation https://developer.parrot.com/docs/sphinx/whatissphinx.html  
BebopSimulation https://github.com/gsilano/BebopS  
Autonomous take off and land https://github.com/cesarhcq/control_bebop_teleop  
Keyboard teleop http://wiki.ros.org/teleop_twist_keyboard   
Bebop teleop https://github.com/Michionlion/bebop_teleop   
PS4 Controller Driver http://wiki.ros.org/ds4_driver   
Visual Servoing http://wiki.ros.org/visp_ros/Tutorials/How%20to%20do%20visual%20servoing%20with%20Parrot%20Bebop%202%20drone%20and%20visp_ros  
