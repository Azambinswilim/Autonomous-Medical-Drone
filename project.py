import asyncio
from mavsdk import System
from mavsdk.telemetry import LandedState
import math


async def check_connection(drone: System):
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone connected!")
            break


async def check_gps(drone: System):
    async for gps in drone.telemetry.position():
        if gps.latitude_deg !=0.0 and gps.longitude_deg !=0.0: 
            print(f"Drone gps!{gps.longitude_deg}")
            break


async def check_battery_before_takeoff(drone: System, min_takeoff_battery = 50): 
    print("Checking battery level before takeoff...")
    async for battery in drone.telemetry.battery():
        battery_percent = int(battery.remaining_percent * 100)
        if battery_percent < min_takeoff_battery:
            print(f"Cannot takeoff! Battery is too low:{battery_percent} % Required:{min_takeoff_battery}")
            return False
        else:
            print(f"Battery check passed: {battery_percent}%")
            return True
        

async def check_battery(drone: System, target_distance_meters = 0):
    print("check_battery")
    async for battery in drone.telemetry.battery():
        battery_percent = int(battery.remaining_percent * 100)
        print(f"Current battery: {battery_percent}%")
        if target_distance_meters > 0:
            expected_consumption =(target_distance_meters / 10) * 0.5 
            remaining_after_trip = battery_percent - expected_consumption 
            print(f"Expected: {expected_consumption}%")
            if remaining_after_trip < 20:
                print("Warning: Battery low for trip!")
                if battery_percent <= 5 :
                    print("The battery charge 5%, and will begin to landing")
                    await landing(drone)
                    break
    await asyncio.sleep(5)


async def arm_drone (drone: System):
    print("Arming drone...")
    await drone.action.arm()
    async for armed in drone.telemetry.armed():
        print(f"armed: {armed}")
        if armed:
            print("Drone armed!")
            break


async def takeoff(drone: System):
    await drone.action.takeoff()
    async for state in drone.telemetry.landed_state():
        print(f"after takeoff state: {state}")
        if state == LandedState.IN_AIR:
            print("Drone took off!")
            break

async def landing(drone: System):
    await drone.action.land()
    async for state in drone.telemetry.landed_state():
        print(f"after landing state: {state}")
        if state == LandedState.ON_GROUND:
            print("Drone landed!")
            break


async def wait_until_reached(drone: System, target_lat, target_lon):
    print("Waiting to reach destination...")
    async for position in drone.telemetry.position():
        lat_diff = target_lat - position.latitude_deg 
        lon_diff = target_lon - position.longitude_deg
        distance = math.sqrt((lat_diff * 111000) ** 2 + (lon_diff * 111000) ** 2) 
        if distance < 0.5: 
            print("Destination reached successfully!")
            break
    await asyncio.sleep(1)


async def run():

    drone = System()

    await drone.connect(system_address="udp://:14540")
    await check_connection(drone)


    await check_gps(drone)

    battery_ok = await check_battery_before_takeoff(drone)
    if not battery_ok:
        print("Stopping missing execution... Drone will not takeoff.")
        return
    
    await arm_drone(drone)

    await takeoff(drone)

    home = await anext(drone.telemetry.home())
    z = home.absolute_altitude_m 
    lat = home.latitude_deg 
    lon = home.longitude_deg 

    alt = z + 5.0
    print(f"Flight altiude is: {alt}")

    target_lat = 24.549431
    target_lon = 46.659694
    await drone.action.goto_location(target_lat ,target_lon , alt , 0)

    battery_task = asyncio.create_task(check_battery(drone, target_distance_meters = 100))
    print("Drone is traveling to the destination...")
    await wait_until_reached(drone, target_lat, target_lon)
    print("dron lading now...")
    await landing(drone)
    await asyncio.sleep(5)

    print("Return to home...")
    await arm_drone(drone)
    await takeoff(drone)
    await drone.action.goto_location(lat ,lon , alt , 0)
    await wait_until_reached(drone, lat, lon)
    print("Arrived at home. Initiating final landing...")
    await landing(drone)
    battery_task.cancel()
    print("Mission completed successfully. Battery monitoring stopped.")

  
asyncio.run(run())