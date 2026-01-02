from nicegui import ui


def play_beep(frequency: int = 880, duration_s: float = 0.25, wave: str = 'square') -> None:
    ui.run_javascript(
        "const c=new (window.AudioContext||window.webkitAudioContext)();"
        "const o=c.createOscillator();"
        f"o.type='{wave}';"
        f"o.frequency.setValueAtTime({frequency},c.currentTime);"
        "o.connect(c.destination);o.start();"
        f"o.stop(c.currentTime+{duration_s});"
    )
