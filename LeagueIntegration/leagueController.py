import datetime
import time
import requests

from LeagueIntegration.event_listener import EventListener

class LeagueController:
    def __init__(self, onKillCallback, gameEndCallback):
        self.current_summoner_name = None
        self.game_start_time = None
        self.game_end_time = None
        self.onKillCallback = onKillCallback
        self.gameEndCallback = gameEndCallback

    def process_event(self, events):
        for event in events:
            event_name = event.get("EventName")
            if event_name == "GameStart":
                self.handle_game_start()
            elif event_name in ["ChampionKill", "Multikill"]:
                self.handle_kill_event(event)
            elif event_name == "GameEnd":
                self.handle_game_end()

    def handle_game_start(self):
        # Store the current timestamp
        self.game_start_time = datetime.datetime.now()

        # Fetch the current summoner name
        try:
            response = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False)
            response.raise_for_status()
            data = response.json()
            self.current_summoner_name = data.get("riotIdGameName")
            print(f"\033[92mGame started at: {self.game_start_time}, Summoner: {self.current_summoner_name}\033[0m")
        except requests.RequestException as e:
            print(f"\033[91mError fetching active player data: {e}\033[0m")

    def handle_kill_event(self, event):
        killer_name = event.get("KillerName")
        if killer_name == self.current_summoner_name:
            # Trigger the callback function
            self.onKillCallback()

    def handle_game_end(self):
        # Store the current timestamp as a tuple with the last GameStart timestamp
        self.game_end_time = datetime.datetime.now()
        print(f"\033[92mGame started at: {self.game_start_time}, ended at: {self.game_end_time}\033[0m")
        # Reset summoner name and timestamps)
        self.gameEndCallback(self.game_start_time, self.game_end_time)
        self.game_start_time = None
        self.game_end_time = None

