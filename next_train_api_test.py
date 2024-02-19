import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HkMTRService:

    def __init__(self):
        try:
            s = requests.Session()
            retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
            s.mount('http://', HTTPAdapter(max_retries=retries))
            response = s.get("http://localhost:3000/api/mtr")
            self.mtr_lines = response.json().get('line', {})
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except ValueError:
            print("Response is not valid JSON.")

    def get_schedule_by_line(self, line):
        if not line in self.mtr_lines.keys():
            print(f"No data found for the line: {line}")
            return

        stations = self.mtr_lines[line].keys()
        for station in stations:
            response = requests.get(f"https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={line}&sta={station}&lang=en")
            data = response.json()
            print(data)

work = HkMTRService()
work.get_schedule_by_line('AEL')
