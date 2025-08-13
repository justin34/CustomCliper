import threading
import time
from obswebsocket import obsws
from ObsIntegration.RequestsObject import requestObject
from screeninfo import get_monitors


class ObsController:
    def __init__(self, file_store_location: str):
        self._file_store_location = file_store_location

        self._host = "localhost"
        self._port = 4455
        self._password = "BZyN8dU4qDEoYxDI"
        self._lock = threading.Lock() # Lock for thread safety
        self._sceneName = "CustomClip"
        self._sceneUUID = None
        self._screenCaptureInputName = "MainMonitor"
        self._screenCaptureUUID = None

        self._originalFileStoreLocation = None

    def callBack(self, callback):
        #print(f"Callback called with: {callback}")
        pass
    
    def _safe_call(self, request):
        with self._lock: # Acquire the lock before making the call
            return self._ws.call(request) 

    def connect(self):
        self._ws = obsws(self._host, self._port, password=self._password)
        try:
            connected = False
            for _ in range(30):
                try:
                    print("Attempting to connect to OBS WebSocket...")
                    self._ws.connect()
                    time.sleep(5)
                    connected = True
                    break
                except Exception as e:
                    print(f"Connection attempt failed: {e}")
                    time.sleep(10)
            if not connected:
                raise Exception("Unable to connect to OBS WebSocket after multiple attempts")
            print("Connected to OBS WebSocket")
            print(self._ws.register(self.callBack))
            #print(self._safe_call(requestObject.GetVersion()).getObsVersion())
            self._sceneUUID = self._safe_call(requestObject.CreateScene(sceneName=self._sceneName)).getSceneUuid()
            print(f"Created Scene with UUID: {self._sceneUUID}")
            self.monitors = get_monitors()
            screen_names = [f"{m}" for i, m in enumerate(self.monitors)]
            self._screenCaptureUUID = self._safe_call(requestObject.CreateInput(sceneName=self._sceneName, sceneUuid=self._sceneUUID,
                                                        inputName=self._screenCaptureInputName, inputKind="monitor_capture")).getInputUuid()
            print(f"Created Screen Capture Input with UUID: {self._screenCaptureUUID}")
            input_settings = {
            "capture_cursor": True,
            "force_sdr": False,
            "method": 0,
            "monitor_id": "\\\\?\\DISPLAY#AOC2702#5&1ca1a46e&0&UID28931#{e6f07b5f-ee97-4a90-b076-33f57bf4eaa7}",
            "monitor_wgc": 0
            }
            self._safe_call(requestObject.SetInputSettings(inputName=self._screenCaptureInputName, inputUuid=self._screenCaptureUUID, inputSettings=input_settings))
            self._safe_call(requestObject.SetCurrentProgramScene(sceneName=self._sceneName, sceneUuid=self._sceneUUID))
        except Exception as e:
            print(f"Failed to connect to OBS WebSocket: {e}")
        
        
    
    def disconnect(self):
        if self._sceneUUID:
            try:
                self._safe_call(requestObject.RemoveScene(sceneName=self._sceneName, sceneUuid=self._sceneUUID))
                print(f"Removed Scene with UUID: {self._sceneUUID}")
            except Exception as e:
                print(f"Failed to remove scene: {e}")
            self._sceneUUID = None

        self._ws.disconnect()
        print("Disconnected from OBS WebSocket")

    def getFileStoreLocation(self) -> str:
        return self._file_store_location

    def start_recording(self):
        # Implement OBS start recording logic here
        print("Starting OBS recording...")
        print(requestObject.StartRecord())
        #self._safe_call()

    def stop_recording(self):
        # Implement OBS stop recording logic here
        print("Stopping OBS recording...")
        self._safe_call(requestObject.StopRecord())
    
    def stopReplayBuffer(self):
        # Implement OBS stop replay buffer logic here
        print("Stopping OBS replay buffer...")
        self._safe_call(requestObject.StopReplayBuffer())
        if self._originalFileStoreLocation:
            self._safe_call(requestObject.SetRecordDirectory(recordDirectory=self._originalFileStoreLocation))
            print(f"Restored original Replay Buffer Directory: {self._safe_call(requestObject.GetRecordDirectory())}")
            self._originalFileStoreLocation = None

    def startReplayBuffer(self):
        # Implement OBS start replay buffer logic here
        print("Starting OBS replay buffer...")
        self._originalFileStoreLocation = self._safe_call(requestObject.GetRecordDirectory()).getRecordDirectory()
        print(f"Original Record Directory: {self._originalFileStoreLocation}")
        self._safe_call(requestObject.SetRecordDirectory(recordDirectory=self._file_store_location))
        print(f"Changed Record directory to: {self._safe_call(requestObject.GetRecordDirectory())}")
        
        print(self._safe_call(requestObject.StartReplayBuffer()))

    def save_replay_buffer(self):
        # Implement OBS save replay buffer logic here
        print("Saving OBS replay buffer...")
        print(self._safe_call(requestObject.SaveReplayBuffer()))

