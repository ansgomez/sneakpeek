# SneakPeek2023

This repo holds the code for the SneakPeek day 2023 (TODO: one sentence on the event,
e.g. host institute at TU Braunschweig and audience).

Small, self-contained demos with Espruino devices (Puck.js / Bangle.js) and a
Raspberry Pi:

- `accel_stream.html` - web page that connects to a Bangle.js/Puck.js over Web Bluetooth (via `puck.js`) and streams accelerometer data.
- `espruino-examples/` - Espruino snippets to upload to a Puck.js:
  - `Accel_Read.js` - print accelerometer values periodically
  - `IR_Read.js` - record IR remote pulse timings
  - `IR_Send.js` - replay recorded IR "on"/"off" codes
- `lamp-demo/` - Raspberry Pi demo: `ir_decode.py` decodes IR remote codes on a GPIO pin; `lamp.html`/`style.css` is a light bulb on/off web page.

TODO: how `lamp.html` and `ir_decode.py` are wired together and how to start the demo.
