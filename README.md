# Autonomous Medical Drone Project

## 1. Installation and Setup Instructions 
To get this project running on your computer, follow these steps strictly:

1. **Download the project:**
   Open your terminal in the folder where you want to keep the project and run:
   `git clone https://github.com/Azambinswilim/Autonomous-Medical-Drone.git`
   `cd Autonomous-Medical-Drone`

2. **Setup the Gazebo Models:**
   For the drone and buildings to appear in the simulation, Gazebo must know their location:
   - Copy the `models` folder to your local Gazebo directory:
     `cp -r models/* ~/.gazebo/models/`
   - If the folder `~/.gazebo/models/` does not exist, create it first: `mkdir -p ~/.gazebo/models/`

3. **Install Dependencies:**
   Ensure you have Gazebo and Python3 installed on your system.

---

## 2. Launch Commands 
The project runs in two stages. Follow them in order:

1. **Start the World:**
   In your terminal, navigate to the project folder and run:
   `PX4_SYS_AUTOSTART=4001 PX4_GZ_WORLD=project PX4_GZ_MODEL_POSE="4.74,7,2,0,0,0" PX4_SIM_MODEL=gz_x500_azam ./build/px4_sitl_default/bin/px4`
   *Wait until the world is fully loaded and you can see the buildings.*

---

## 3. World and Drone Design 
* **World Design:** A custom simulation map designed to mimic a medical delivery zone. It contains key landmarks and a "Landing Pad" identified by specific markings for the drone to detect.
* **Drone Design:** The drone model is a quadcopter specifically configured with the necessary mass and aerodynamic properties for carrying medical payloads. Its movement logic is handled by the Python script in the `code/` folder.
