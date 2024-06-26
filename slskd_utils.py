from typing import Dict, Any, List, Tuple

import slskd_api

from secrets import SLSKD_USERNAME, SLSKD_PASSWORD

host = 'http://localhost:5030'
api_key = 'e45f17a4c8e2b302da89f3e8f906e5cd'


class Slskd:

    def __init__(self):
        self.api = slskd_api.SlskdClient(host, username=SLSKD_USERNAME, password=SLSKD_PASSWORD)
        print(self.api)

    def search(self, query: str) -> str:
        results = self.api.searches.search_text(query)
        return results.get('id')

    def search_state(self, search_id: str) -> Dict[str, Any]:
        return self.api.searches.state(search_id)

    def is_search_complete(self, search_id: str) -> bool:
        return self.search_state(search_id).get('isComplete', False)

    @staticmethod
    def sort_and_flatten_results(results):
        def get_file_priority(file):
            extensions_priority = {"aiff": 1, "wav": 2, "flac": 3, "mp3": 4}
            bitrate_or_samplerate = file.get("bitRate", file.get("sampleRate", 0))
            return (
                -result.get("hasFreeUploadSlot", False),
                -result["uploadSpeed"],
                extensions_priority.get(file["filename"].split(".")[-1], 5),
                -bitrate_or_samplerate,
            )

        flattened_results = []
        for result in results:
            if result["fileCount"] > 0 and result.get("hasFreeUploadSlot", False):
                if result["fileCount"] == 1:
                    flattened_results.append(result)
                else:
                    # Flatten the 'files' list and create a new result for each file
                    for file in result["files"]:
                        new_result = result.copy()
                        new_result["fileCount"] = 1
                        new_result["files"] = [file]
                        flattened_results.append(new_result)

        # Sort the flattened results based on the defined criteria
        sorted_results = sorted(flattened_results, key=lambda r: get_file_priority(r["files"][0]))

        return sorted_results

    @staticmethod
    def prepare_results_for_download(ordered_results: List[Any]):
        result_list = []

        for result in ordered_results:
            username = result.get("username", None)
            files = result.get("files", [])
            if username and files:
                result_list.append((username, files))

        return result_list

    def get_results(self, search_id: str) -> List[Any]:
        results = (self.api.searches.search_responses(search_id))
        sorted_results = self.sort_and_flatten_results(results)
        prepared_results = self.prepare_results_for_download(sorted_results)
        return prepared_results

    def pop_best_result(self, results: List[Any]) -> Tuple[str, Dict[str, Any]]:
        return results[0] if results else None

    def start_download(self, track: Tuple[str, Dict[str, Any]]) -> bool:
        return self.api.transfers.enqueue(*track)

    def get_all_downloads(self, including_removed: bool = False):
        return self.api.transfers.get_all_downloads(includeRemoved=including_removed)

    def get_all_failed_downloads(self, including_removed: bool = False):
        all_downloads = self.get_all_downloads(including_removed=including_removed)

        result = []
        for user in all_downloads:
            username = user['username']
            files = []
            for directory in user['directories']:
                for file in directory['files']:
                    if 'queued' in file['state'].lower() or 'errored' in file['state'].lower():
                        files.append(file)
            if files:
                result.append((username, files))
        return result
