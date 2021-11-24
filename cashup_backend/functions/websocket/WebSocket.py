from websocket import WebSocketApp


class BitMEXWebSocket:
    def __init__(self, api_key, api_secret_key, conn):
        self.BASE_URL = 'bitmex'
        self.socket = None
        self.conn = conn

    def _on_connect(self):
        self.socket = WebSocketApp(self.BASE_URL, on_open=self._on_open, on_message=self._on_message,
                                   on_error=self._on_error, on_close=self._on_close)

    def _on_message(self, message):
        pass

    def _on_error(self, ws):
        pass

    def _on_close(self, ws):
        pass

    def _on_open(self, ws):
        pass
        # ws.send('{"op": "subscribe", "args": ["trade:XBTUSD"]}')
        # ws.send('{"op": "subscribe", "args": ["trade:XBTZ21"]}')
        # ws.send('{"op": "subscribe", "args": ["orderBook10:XBTUSD"]}')
        # ws.send('{"op": "subscribe", "args": ["orderBook10:XBTZ21"]}')
