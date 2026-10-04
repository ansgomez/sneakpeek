# SneakPeek2023

This repo holds the code for the demos shown at the SneakPeek day 2023.

Small, self-contained demos with Espruino devices (Puck.js / Bangle.js) and a
Raspberry Pi:

- `accel_stream.html` - web page that connects to a Bangle.js/Puck.js over Web Bluetooth (via `puck.js`) and streams accelerometer data.
- `espruino-examples/` - Espruino snippets to upload to a Puck.js:
  - `Accel_Read.js` - print accelerometer values periodically
  - `IR_Read.js` - record IR remote pulse timings
  - `IR_Send.js` - replay recorded IR "on"/"off" codes
- `lamp-demo/` - Raspberry Pi demo: `ir_decode.py` decodes IR remote codes on a GPIO pin; `lamp.html`/`style.css` is a light bulb on/off web page.

## License

MIT License, Copyright (c) 2023 Andres Gomez. See [LICENSE](LICENSE).
