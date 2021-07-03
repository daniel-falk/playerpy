from simple_websocket_server import WebSocketServer, WebSocket
import threading
import time

IMAGES = [
        "https://pngimg.com/uploads/number0/number0_PNG19165.png",
        "https://upload.wikimedia.org/wikipedia/commons/8/81/Linea_1.png",
        "https://upload.wikimedia.org/wikipedia/commons/9/9f/Icon_2_%28set_basic%29.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/26/MRT_Singapore_Destination_3.png"
]


class SimpleImageSource(WebSocket):
    def __init__(self, *args, **kwargs):
        self.idx = 0
        super().__init__(*args, **kwargs)

    def send_image_path(self):
        img_path = IMAGES[self.idx % len(IMAGES)]
        self.send_message("img:" + img_path)

    def handle(self):
        # Receive an event from the front-end and act on it
        print("Event: %s" % self.data)
        if self.data == "ARROW_LEFT":
            self.idx -= 1
        elif self.data == "ARROW_RIGHT":
            self.idx += 1
        else:
            print("Unknown event: %s" % str(self.data))
            return
        self.send_image_path()

    def connected(self):
        print(self.address, 'connected')
        self.send_image_path()

    def handle_close(self):
        print(self.address, 'closed')


def advance_loop(server):
    """Advance every image source one frame per 3 seconds
    """
    while True:
        for _, image_source in server.connections.items():
            image_source.idx += 1
            image_source.send_image_path()
        time.sleep(10)

server = WebSocketServer('', 8000, SimpleImageSource)
th = threading.Thread(target=advance_loop, args=(server,), daemon=True)
th.start()
server.serve_forever()
