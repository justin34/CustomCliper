import subprocess
import os
import signal

class ObsProcessController:
    def __init__(self, obs_path: str, config_path: str = None):
        """
        :param obs_path: Path to the OBS executable (e.g., "C:/Program Files/obs-studio/bin/64bit/obs64.exe").
        :param config_path: Optional path to a custom OBS configuration directory.
        """
        self.obs_path = obs_path
        self.config_path = config_path
        self.process = None

    def start_obs(self):
        """Start OBS as a subprocess."""
        try:
            obs_home_dir = os.path.dirname(self.obs_path)  # Get the directory of the OBS executable
            args = [self.obs_path]
            if self.config_path:
                args.extend(["--portable", "--config", self.config_path])  # Use portable mode with a custom config
            self.process = subprocess.Popen(args, cwd=obs_home_dir, 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE,
                                             creationflags=subprocess.CREATE_NO_WINDOW)
            print("OBS started successfully.")
        except Exception as e:
            print(f"Failed to start OBS: {e}")

    def stop_obs(self):
        """Stop the OBS subprocess."""
        if self.process:
            try:
                self.process.terminate()  # Gracefully terminate the process
                self.process.wait(timeout=5)  # Wait for the process to exit
                print("OBS terminated successfully.")
            except subprocess.TimeoutExpired:
                print("OBS did not terminate in time. Forcing shutdown...")
                self.process.kill()  # Forcefully kill the process
            except Exception as e:
                print(f"Failed to stop OBS: {e}")
            finally:
                self.process = None

    def is_running(self):
        """Check if the OBS subprocess is still running."""
        return self.process and self.process.poll() is None

