import time
import math
import json
import requests

class StellariumAPI:
    # Base URL for the HTTP API
    STELLARIUM_URL = "http://localhost:8090/api"

    def __init__(self, url=None):
        self.url = url
        if self.url is None:
            self.url = StellariumAPI.STELLARIUM_URL

    def radec_to_xyz(self, ra, dec):
        ra = math.radians(ra*15)
        dec = math.radians(dec)
        return [math.cos(dec)*math.cos(ra), math.cos(dec)*math.sin(ra), math.sin(dec)]

    def xyz_to_radec(self, x, y, z):
        dec = math.asin(z)
        ra = math.asin(y/math.cos(dec))
        return [math.degrees(ra)/15.0, math.degrees(dec)]

    def altaz_to_xyz(self, alt, az):
        alt = math.radians(alt)
        az = math.radians(az)
        return [math.cos(alt)*math.cos(az), math.cos(alt)*math.sin(az), math.sin(alt)]

    def xyz_to_altaz(self, x, y, z):
        alt = math.asin(z)
        az = math.atan2(y, -x)
        return [math.degrees(alt), math.degrees(az)%360]

    def send_http_request(self, endpoint, payload=None, json=False):
        """Sends a GET or POST request to Stellarium's HTTP API."""
        url = f"{self.url}/{endpoint}"
        try:
            if payload is None:
                response = requests.get(url)
            else:
                if json:
                    response = requests.post(url, json=payload)
                else:
                    response = requests.post(url, data=payload)
            if response.status_code == 200:
                #print(f"Success: {response.text}")
                return response.text
            else:
                print(f"Error: {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")

    def set_time(self, year, month, day, hour, minute, second):
        """Sets the time in Stellarium."""
        endpoint = f"set_time/{year}/{month}/{day}/{hour}/{minute}/{second}"
        #self.send_http_request(endpoint)

    def zoom_in(self):
        """Zoom in in Stellarium."""
        endpoint = "main/focus"
        zoom = {"mode": "zoom"}
        zoom = {"target":"Moon", "mode": "zoom"}
        self.send_http_request(endpoint, zoom)

    def zoom_out(self):
        """Zoom out in Stellarium."""
        endpoint = "main/focus"
        zoom = {}
        self.send_http_request(endpoint, zoom)

    def fov(self, val=5.0):
        """Zoom out in Stellarium."""
        endpoint = "main/fov"
        fov_val = {"fov": val}
        self.send_http_request(endpoint, fov_val)

    def get_fov(self):
        """Zoom out in Stellarium."""
        return self.get_status()["view"]["fov"]

    def get_status(self):
        """Zoom out in Stellarium."""
        endpoint = f"main/status"
        status = json.loads(self.send_http_request(endpoint))
        return status

    def get_radec(self):
        """Get Stellarium's current RA and DEC coordinates."""
        endpoint = f"main/view"
        pos = self.send_http_request(endpoint)
        if pos is None:
            return [0, 0]
        pos = json.loads(json.loads(pos)["jNow"])
        return self.xyz_to_radec(pos[0], pos[1], pos[2])

    def get_altaz(self):
        """Move Stellarium to given RA and DEC coordinates."""
        endpoint = f"main/view"
        pos = self.send_http_request(endpoint)
        if pos is None:
            return [0, 0]
        pos = json.loads(json.loads(pos)["altAz"])
        return self.xyz_to_altaz(pos[0], pos[1], pos[2])

    def move_to_radec(self, ra, dec):
        """Move Stellarium to given RA and DEC coordinates."""
        endpoint = f"main/view"
        pos = {"jNow": json.dumps(self.radec_to_xyz(ra, dec))}
        self.send_http_request(endpoint, pos)

    def move_to_altaz(self, alt, az):
        """Move Stellarium to given ALT and AZ coordinates."""
        endpoint = f"main/view"
        pos = {"altAz": json.dumps(self.altaz_to_xyz(alt, az))}
        self.send_http_request(endpoint, pos)

    def delta_altaz(self, delta_alt, delta_azm, fov):
        endpoint = f"main/move"

    def delta_azm(self, cmd, cur):
        cur %= 360
        cmd %= 360
    
        delta = (cmd - cur) % 360

        return delta - 360 if delta > 180 else delta

    def slew_to_altaz(self, cmd_alt, cmd_azm):
        endpoint = f"main/move"

        tol = 0.02
        slp = 0.10
        fov = self.get_fov()

        act_pos = self.get_altaz()
        delta_alt = cmd_alt - act_pos[0]
        delta_azm = self.delta_azm(cmd_azm, act_pos[1])

        while math.fabs(delta_alt) > tol or math.fabs(delta_azm) > tol:
            delta_alt = math.copysign(min(math.fabs(delta_alt), 10), delta_alt)
            delta_azm = math.copysign(min(math.fabs(delta_azm), 10), delta_azm)
            slew_x = delta_azm / fov
            slew_y = delta_alt / fov
            slew_pos = {"x": slew_x, "y": slew_y}
            self.send_http_request(endpoint, slew_pos)
            time.sleep(slp)
            act_pos = self.get_altaz()

            delta_alt = cmd_alt - act_pos[0]
            delta_azm = self.delta_azm(cmd_azm, act_pos[1])

    def gradual_fov(self, cmd_fov, tm = 0.5):
        step_tm = 0.01
        steps = tm / step_tm
        fov = self.get_fov()
        dfov = (cmd_fov - fov) / steps
        tol = 0.01
        while math.fabs(cmd_fov - fov) > tol:
            fov += dfov
            self.fov(fov)
            time.sleep(step_tm)
