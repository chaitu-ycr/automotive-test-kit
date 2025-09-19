import argparse
import sys


from py_uds_demo.interface.cli import Cli
from py_uds_demo.interface.gui import Gui
from py_uds_demo.interface.web import Web
import uvicorn

def main():
    parser = argparse.ArgumentParser(
        description="UDS Simulator\n\nThis tool runs the UDS Simulator in different modes.\n\n"
                    "Modes available:\n"
                    "  cli - Command Line Interface mode (default)\n"
                    "  gui - Graphical User Interface mode\n"
                    "  web - Web Server mode\n",
        epilog="Example usage:\n"
               "  python -m py_uds_demo --mode cli\n"
               "  python -m py_uds_demo --mode gui\n"
               "  python -m py_uds_demo --mode web\n"
               "You can also use '?' instead of --help to display this message.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--mode",
        choices=["cli", "gui", "web", "api"],
        default="cli",
        help="Select mode to run: cli (default), gui, web, or api (FastAPI server)"
    )

    if "?" in sys.argv:
        sys.argv[sys.argv.index("?")] = "--help"

    args = parser.parse_args()

    match args.mode:
        case "cli":
            print("Starting CLI Mode...")
            cli = Cli()
            cli.run()
        case "gui":
            print("Starting GUI Mode...")
            gui = Gui()
            gui.run()
        case "web":
            print("Starting Web Mode...")
            web = Web()
            web.run()
        case "api":
            print("Starting FastAPI server (API Mode)...")
            uvicorn.run("py_uds_demo.interface.api:app", host="127.0.0.1", port=8000, reload=True)
        case _:
            print("Unknown mode selected.")

if __name__ == "__main__":
    main()
