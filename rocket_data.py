import requests
from datetime import datetime


class Launches:
    def get_data(self):  # Get upcoming launch in json
        self.data = requests.get(
            "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
        ).json()

    def get_latest_rocket_date(
        self,
    ):  # Get launch date of previous rocket, needed for progress bar
        latest = requests.get(
            "https://ll.thespacedevs.com/2.2.0/launch/previous/"
        ).json()["results"][0]["net"]
        return latest

    def timestamp_to_seconds(
        self, timestamp_string
    ):  # Convert timestamp-string to unix-time
        return datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%SZ").timestamp()

    def get_countdown(
        self, timestamp_string
    ):  # Generate a countdown in seconds, can be converted to HMS later
        timestamp = datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.utcnow()

        countdown_seconds = (timestamp - current_time).total_seconds()

        return countdown_seconds

    def parse_data(
        self, index
    ):  # Parse only required data and calculate percentages etc.
        launch = self.data["results"][index]

        previous_launch_date = self.timestamp_to_seconds(self.get_latest_rocket_date())
        next_launch_date = self.timestamp_to_seconds(launch["net"])
        current_time = datetime.utcnow().timestamp()
        percentage = round(
            (current_time - previous_launch_date)
            / (next_launch_date - previous_launch_date),
            3,
        )

        parsed_data = {
            "rocket_name": launch["rocket"]["configuration"]["name"],
            "countdown": launch["net"],
            "mission_name": launch["mission"]["name"],
            "abbrev": launch["status"]["abbrev"],
            "agency": launch["launch_service_provider"]["name"],
            "launch_location": launch["pad"]["name"],
            "countdown": round(self.get_countdown(launch["net"])),
            "launch_percent": percentage,
        }
        return parsed_data


def wait_for_internet():
    while True:
        try:
            requests.head("http://github.com/", timeout=15)
            return
        except requests.ConnectionError:
            pass
