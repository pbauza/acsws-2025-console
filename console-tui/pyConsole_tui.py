import asyncio
from Acspy.Clients.SimpleClient import PySimpleClient

async def tui_console(console):
    print("Debug Console Started. Type commands to interact with sensors.")
    print("Commands:")
    print("  printHello")
    print("  setMode <mode>")
    print("  cameraOn")
    print("  cameraOff")
    print("  moveTelescope <x> <y>")
    print("  getTelescopePosition")
    print("  getCameraImage")
    print("  setRGB <r> <g> <b>")
    print("  setPixelBias <bias>")
    print("  setResetLevel <level>")
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
                "movetelescope",
                "gettelescopeposition",
                "getcamerimage",
                "setrgb",
                "setpixelbias",
                "setresetlevel",
            ]:
                match cmd[0].lower():
                    case "printhello":
                        print(console.printHello())
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
        print("Debug console terminated.")
    except Exception as e:
        print("Error:", e)