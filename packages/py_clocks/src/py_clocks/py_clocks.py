import customtkinter as ctk
from datetime import datetime
import pytz
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class PyClocks:
    """
    A class that encapsulates the clock application logic and individual clock widgets.
    """

    # Constants for the application
    WINDOW_WIDTH = 220
    WINDOW_HEIGHT = 420
    CLOCK_PADDING = 10
    WINDOW_BOTTOM_HEIGHT_OFFSET = 100
    WINDOW_BOTTOM_WIDTH_OFFSET = 15
    WINDOW_TRANSPARENCY = 1.0

    # Constants for clock widgets
    TITLE_FONT = ("Arial", 20)
    TIME_FONT = ("Arial", 14)
    UPDATE_INTERVAL = 1000
    INVALID_TIMEZONE_MSG = "Invalid Timezone"
    GENERIC_ERROR_MSG = "Error"

    def __init__(self):
        """
        Initializes the PyClocks application.
        """
        self.root = ctk.CTk()
        logging.info("PyClocks application initialized.")

    def configure_window(self):
        """
        Configures the main application window and positions it at the bottom-right corner of the screen.
        """
        self.root.title("py_clocks")
        self.root.attributes("-alpha", self.WINDOW_TRANSPARENCY)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - self.WINDOW_WIDTH - self.WINDOW_BOTTOM_WIDTH_OFFSET
        y = screen_height - self.WINDOW_HEIGHT - self.WINDOW_BOTTOM_HEIGHT_OFFSET
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
        logging.info("Main application window configured.")

    def add_clock_widget(self, timezone, label_text, bg_color, text_color):
        """
        Adds a clock widget to the application window.

        Args:
            timezone (str): The timezone for the clock.
            label_text (str): The label text displayed above the clock.
            bg_color (str): The background color of the widget.
            text_color (str): The text color for the labels.
        """
        frame = ctk.CTkFrame(self.root, fg_color=bg_color)
        frame.pack(padx=20, pady=self.CLOCK_PADDING)

        ctk.CTkLabel(frame, text=label_text, font=self.TITLE_FONT, text_color=text_color).pack(pady=(10, 5))
        time_label = ctk.CTkLabel(frame, text="", font=self.TIME_FONT, text_color=text_color)
        time_label.pack(padx=20, pady=(10, 0))
        date_label = ctk.CTkLabel(frame, text="", font=("Arial", 12), text_color=text_color)
        date_label.pack(padx=20, pady=(0, 10))

        self.start_clock_update(time_label, date_label, timezone, label_text)
        logging.info(f"Clock widget added for timezone: {timezone} ({label_text}).")

    def start_clock_update(self, time_label, date_label, timezone, label_text):
        """
        Starts the periodic update of the clock display.

        Args:
            time_label (CTkLabel): The label to update with the current time.
            date_label (CTkLabel): The label to update with the current date.
            timezone (str): The timezone for the clock.
            label_text (str): The label text for logging purposes.
        """
        def update_clock():
            try:
                tz = pytz.timezone(timezone)
                now = datetime.now(tz)
                current_time = now.strftime("%I:%M:%S %p")
                iso_week = f"CW {now.isocalendar()[1]}"
                time_label.configure(text=f"{current_time} ({iso_week})")
                date_str = now.strftime("%A, %Y-%m-%d")
                date_label.configure(text=date_str)
            except pytz.UnknownTimeZoneError:
                time_label.configure(text=self.INVALID_TIMEZONE_MSG)
                date_label.configure(text="")
                logging.error(f"Unknown timezone: {timezone} for {label_text}.")
            except Exception as e:
                time_label.configure(text=self.GENERIC_ERROR_MSG)
                date_label.configure(text="")
                logging.error(f"Error updating clock for {label_text}: {e}")
            self.root.after(self.UPDATE_INTERVAL, update_clock)

        update_clock()

    def run(self):
        """
        Runs the PyClocks application by creating the main window and adding clock widgets for specified timezones.
        """
        self.configure_window()

        # Time zones and their configurations
        time_zones = [
            {"timezone": "Asia/Tokyo", "label": "Japan 🏯", "bg_color": "#FFE5CC", "text_color": "#FF8000"},
            {"timezone": "Asia/Kolkata", "label": "India 🌴", "bg_color": "#CCFFCC", "text_color": "#008000"},
            {"timezone": "Europe/Berlin", "label": "Germany 🚘", "bg_color": "#CCCCFF", "text_color": "#0000FF"},
        ]

        for config in time_zones:
            self.add_clock_widget(
                timezone=config["timezone"],
                label_text=config["label"],
                bg_color=config["bg_color"],
                text_color=config["text_color"],
            )

        logging.info("Starting the PyClocks application.")
        self.root.mainloop()


if __name__ == "__main__":
    app = PyClocks()
    app.run()
