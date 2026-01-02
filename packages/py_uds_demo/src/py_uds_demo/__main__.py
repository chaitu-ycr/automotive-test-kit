import argparse
import sys
import subprocess
import os


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
            cli_file = os.path.join(os.path.dirname(__file__), 'interface', 'cli.py')
            subprocess.run([sys.executable, cli_file])
        case "gui":
            print("Starting GUI Mode...")
            gui_file = os.path.join(os.path.dirname(__file__), 'interface', 'gui.py')
            subprocess.run([sys.executable, gui_file])
        case "web":
            print("Starting Web Mode...")
            # Run web interface as a subprocess to allow NiceGUI to initialize properly
            web_file = os.path.join(os.path.dirname(__file__), 'interface', 'web.py')
            subprocess.run([sys.executable, web_file])
        case "api":
            print("Starting FastAPI server (API Mode)...")
            uvicorn.run("py_uds_demo.interface.api:app", host="127.0.0.1", port=8000, reload=True)
        case _:
            print("Unknown mode selected.")

if __name__ == "__main__":
    main()
