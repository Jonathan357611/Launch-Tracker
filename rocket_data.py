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

    def truncate_string(self, string, overflow, new_end="..."):
        if len(string) >= overflow:
            return string[:overflow] + "..."
        return string

    def parse_data(
        self, index
    ):  # Parse only required data and calculate percentages etc.
        current_time = datetime.utcnow().timestamp()

        skip = 0
        for i in range(
            len(self.data["results"])
        ):  # Get next upcoming launch, by checking launch dates
            iter_launch_date = self.timestamp_to_seconds(self.data["results"][i]["net"])

            if current_time > iter_launch_date:
                skip += 1
            else:
                continue

        launch = self.data["results"][skip + index]

        previous_launch_date = self.timestamp_to_seconds(self.get_latest_rocket_date())
        next_launch_date = self.timestamp_to_seconds(launch["net"])

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
            "agency": self.truncate_string(
                launch["launch_service_provider"]["name"], 15
            ),
            "launch_location": launch["pad"]["name"],
            "countdown": round(self.get_countdown(launch["net"])),
            "launch_percent": percentage,
        }
        return parsed_data


def check_internet_connection():
    try:
        output = subprocess.check_output("ping -W 3 -c 1 8.8.8.8", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


def wait_for_internet():
    connected = False
    while not connected:
        connected = check_internet_connection()
    return
