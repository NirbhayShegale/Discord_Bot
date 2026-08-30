# Discord_Bot

The bot exposes a health endpoint on Render's `PORT` and sends a keepalive request every 10 minutes while it is running.

For Render, `RENDER_EXTERNAL_URL` is used automatically. On another host, set `KEEPALIVE_URL` to the service's public base URL. You can override the interval in seconds with `KEEPALIVE_INTERVAL`.
