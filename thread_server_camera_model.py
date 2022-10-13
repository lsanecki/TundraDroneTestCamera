class ServerCameraModel:
    def __init__(self):
        self.port = 5000
        self.server_address = '10.100.255.215'
        self.camera_threshold = 300
        self.command_to_send = 'Video#A#480#480#640#640'
