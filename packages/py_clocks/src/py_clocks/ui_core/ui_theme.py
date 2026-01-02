from nicegui import ui


def apply_theme(panel_width: int = 400, panel_height: int = 300) -> None:
    ui.colors(primary='#3B82F6', secondary='#10B981', accent='#F59E0B')
    ui.dark_mode().enable()

    ui.add_head_html(f'''
    <style>
      :root {{
        --retro-bg: #0a0e27; --retro-text: #ffffff;
        --retro-header-bg: #00ffff; --retro-header-text: #000000; --retro-header-border: #00cccc;
        --retro-yellow: #ffff00; --retro-green: #00ff00; --retro-cyan: #00ffff; --retro-magenta: #ff00ff;
        --retro-panel-yellow: #1a1a00; --retro-panel-green: #001a00; --retro-panel-cyan: #001a1a; --retro-panel-magenta: #1a001a;
      }}
      body {{ background: var(--retro-bg) !important; color: var(--retro-text); font-family: "Courier New", monospace; min-height: 100vh; image-rendering: pixelated; }}
      .q-page-container, .q-page {{ background: transparent !important; }}

      .app-grid {{ display: grid; grid-template-columns: {panel_width}px {panel_width}px; grid-template-rows: {panel_height}px {panel_height}px; gap: 16px; justify-content: center; align-content: center; width: 100%; height: 100%; }}
      @media (max-width: 900px) {{ .app-grid {{ grid-template-columns: {panel_width}px; grid-template-rows: {panel_height}px {panel_height}px {panel_height}px {panel_height}px; }} }}
      @media (max-width: 600px) {{ .panel {{ padding: 6px; }} .panel-title {{ margin-bottom: 6px; font-size: 0.9rem; }} }}

      .panel {{ width: {panel_width}px; height: {panel_height}px; overflow: hidden; background: var(--panel-bg); border: 4px solid var(--accent); border-radius: 0px; padding: 6px; box-shadow: 0 0 20px var(--accent); image-rendering: pixelated; box-sizing: border-box; }}
      .panel-title {{ color: var(--accent); font-weight: 700; font-size: 0.78rem; text-align: center; margin-bottom: 2px; letter-spacing: 2px; text-transform: uppercase; text-shadow: 0 0 8px var(--accent); }}
      .panel-body {{ display: flex; flex-direction: column; height: 100%; min-height: 0; width: 100%; }}
      .panel .w-full {{ width: 100% !important; }} .panel .q-card {{ width: 100%; }} .panel .q-row {{ width: 100%; }} .panel .q-col {{ width: 100%; }}

      /* header controls */
      .retro-toggle .q-toggle__track {{ background: #000000 !important; border: 2px solid #00cccc !important; border-radius: 0px; box-shadow: none; }}
      .retro-toggle.q-toggle--checked .q-toggle__track {{ background: #000000 !important; border: 2px solid #00cccc !important; }}
      .retro-toggle .q-toggle__thumb, .retro-toggle .q-toggle__thumb:before, .retro-toggle .q-toggle__thumb:after, .retro-toggle.q-toggle--checked .q-toggle__thumb, .retro-toggle.q-toggle--checked .q-toggle__thumb:before, .retro-toggle.q-toggle--checked .q-toggle__thumb:after {{ background: #000000 !important; border: 2px solid #00cccc !important; border-radius: 0px !important; box-shadow: none !important; color: #000000 !important; }}
      .retro-toggle .q-toggle__inner {{ min-height: 20px; color: #000000 !important; }}
    </style>
    <script>
      window.addEventListener('keydown', (e) => {{
        try {{
          if (e.code === 'Space') {{ const b = document.getElementById('stopwatch-start'); if (b) {{ e.preventDefault(); b.click(); return; }} }}
          if (e.key === 'l' || e.key === 'L') {{ const b = document.getElementById('stopwatch-lap'); if (b) {{ b.click(); return; }} }}
          if (e.key === 'Enter') {{ const b = document.getElementById('timer-start'); if (b) {{ b.click(); return; }} }}
        }} catch (err) {{ }}
      }});
    </script>
    ''')
