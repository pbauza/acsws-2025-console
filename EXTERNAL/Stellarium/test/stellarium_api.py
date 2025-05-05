import time

from stellarium.api import StellariumAPI

def main():
    s = StellariumAPI()
    print("Current RaDec:", s.get_radec())
    print("Current AltAz:", s.get_altaz())
    time.sleep(5)
    #zoom_in()
    s.zoom_out()
    #time.sleep(1)
    s.fov(60.0)
    time.sleep(1)
    s.move_to_radec(0.712266667, 41.269) # Move to coordinates (RA, Dec) of the Andromeda galaxy
    print("Current RaDec:", s.get_radec())
    print("Current AltAz:", s.get_altaz())
    #move_to_altaz(45, 40) # Move to coordinates (RA, Dec) of the Andromeda galaxy
    time.sleep(2)  # Wait for 2 seconds
    s.fov(5.0)
    time.sleep(2)  # Wait for 2 seconds
    #set_time(2025, 4, 29, 12, 30, 0)  # Set time to April 29, 2025, at 12:30:00
    print("Current RaDec:", s.get_radec())
    print("Current AltAz:", s.get_altaz())

if __name__ == "__main__":
    main()
