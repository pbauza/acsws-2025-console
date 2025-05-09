import asyncio
from Acspy.Clients.SimpleClient import PySimpleClient

from matplotlib import pyplot as plt
import os

from TYPES import Position, RGB, ImageType 

async def tui_console(console):
    print("Debug Console Started. Type commands to interact with sensors.")
    print("Commands:")
    print("  printHello")
    print("  setMode <auto | manual>")
    print("  cameraOn")
    print("  cameraOff")
    print("  moveTelescope <az> <el>")
    print("  getTelescopePosition")
    print("  getCameraImage")
    print("  setRGB <r> <g> <b>")
    print("  setPixelBias <bias>")
    print("  setResetLevel <level>")
    print("  addProposals <number of proposals>")
    print("  exit")
    while True:
        command = await asyncio.to_thread(input, "Enter TUI command: ")
        cmd = command.strip().split()
        if not cmd:
            continue
        if cmd[0].lower() == "exit":
            print("Exiting tui console.")
            break
        try:
            # SensorStatus-specific commands
            if cmd[0].lower() in [
                "printhello",
                "setmode",
                "cameraon",
                "cameraoff",
                "getcamerimage",
                "setrgb",
                "setpixelbias",
                "setresetlevel",
                "movetelescope",
                "gettelescopeposition",
                "addproposals",
            ]:
                match cmd[0].lower():
                    case "printhello":
                        print(console.printHello())
                    case "setmode":
                        if len(cmd) != 2 or cmd[1].lower() not in ["auto", "manual"]:
                            print("Usage: setmode <auto | manual>")
                            continue
                        if cmd[1].lower() == "auto":
                            console.setMode(True)
                            print("Mode set to Automatic.")
                        else:
                            console.setMode(False)
                            print("Mode set to Manual.")
                    case "cameraon":
                        console.cameraOn()
                    case "cameraoff":
                        console.cameraOff()
                    case "getcamerimage":
                        if len(cmd) != 2:
                            print("Usage: getCameraImage <exposure_time>")
                            continue
                        exposure_time = int(cmd[1])
                        image = console.getCameraImage(exposure_time)
                        print(f"Image received: {image}") # TODO: Handle image data
                    case "setrgb":
                        if len(cmd) != 4:
                            print("Usage: setRGB <r> <g> <b>")
                            continue
                        r = int(cmd[1])
                        g = int(cmd[2])
                        b = int(cmd[3])
                        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                            print("RGB values must be between 0 and 255.")
                            continue
                        console.setRGB(RGB(r, g, b))
                    case "setpixelbias":
                        if len(cmd) != 2:
                            print("Usage: setPixelBias <bias>")
                            continue
                        bias = int(cmd[1])
                        console.setPixelBias(bias)
                    case "setresetlevel":
                        if len(cmd) != 2:
                            print("Usage: setResetLevel <level>")
                            continue
                        level = int(cmd[1])
                        console.setResetLevel(level)
                    case "movetelescope":
                        if len(cmd) != 3:
                            print("Usage: moveTelescope <az> <el>")
                            continue
                        az = float(cmd[1])
                        el = float(cmd[2])
                        console.moveTelescope(Position(az, el))
                    case "gettelescopeposition":
                        print("Getting telescope position...")
                        pos = console.getTelescopePosition()
                        print(f"Telescope Position: Azimuth: {pos.az}, Elevation: {pos.el}")
                    case "addproposals":
                        if len(cmd) != 2:
                            print("Usage: addProposals <number of proposals>")
                            continue
                        n_proposals = int(cmd[1])
                        # Assuming a function to generate proposals
                        os.system("python /home/almamgr/acsws-2025/populate-db/populate-db.py -n " + str(n_proposals))
                        
                        print(f"Generated {n_proposals} proposals.")
                    case _:
                        print("Not implemented.")
            else:
                print("Unknown command.")
        except Exception as e:
            print("Error processing command:", e)


async def debug_main():
    client = PySimpleClient()
    console = client.getComponent("CONSOLE")
    # Run both the OPC-UA server and the debug console concurrently.
    await asyncio.gather(
        tui_console(console),
    )


if __name__ == "__main__":
    try:
        asyncio.run(debug_main())
    except KeyboardInterrupt:
        print("TUI console terminated.")
    except Exception as e:
        print("Error:", e)