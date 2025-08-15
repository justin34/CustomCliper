import requests
import time
import threading

class EventListener:
    def __init__(self, callback):
        """
        Initialize the EventListener.

        :param callback: A function to call when a relevant event is detected.
        """
        self.callback = callback
        self.endpoint = "https://127.0.0.1:2999/liveclientdata/eventdata"
        self.running = True
        self.thread = threading.Thread(target=self.listen_to_events)
        self.thread.daemon = True
        self.thread.start()
        self.last_event_id = -1  # Track the last processed EventID

    def listen_to_events(self):
        """
        Continuously poll the endpoint for events every 30 seconds.
        """
        while self.running:
            try:
                response = requests.get(self.endpoint, verify=False)
                print("Polling for events...")
                if response.status_code == 200:
                    data = response.json()
                    self.process_events(data.get("Events", []))
            except requests.RequestException as e:
                print(f"Error fetching events: {e}")
                if(self.last_event_id != -1):
                    self.last_event_id = -1  # Reset last_event_id on error after first successful fetch
                    self.callback([{"EventName": "GameEnd"}])

            time.sleep(15)  # Wait for 30 seconds before polling again
            

    def process_events(self, events):
        """
        Process the list of events and call the callback for new events.

        :param events: List of event dictionaries.
        """
        new_events = []
        for event in events:
            event_id = event.get("EventID", -1)
            if event_id > self.last_event_id:
                new_events.append(event)

        if new_events:
            self.last_event_id = max(event["EventID"] for event in new_events)
            print(f'Latest events received: {new_events}')
            self.callback(new_events)

    def stop(self):
        """
        Stop the event listener.
        """
        self.running = False
        self.thread.join()


