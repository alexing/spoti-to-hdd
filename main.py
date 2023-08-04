from time import sleep
from typing import List, Set

from slskd_utils import Slskd

slskd = Slskd()


def get_queries_from_songs(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()

        # Remove leading and trailing whitespaces (including '\n' newline character) for each line
        lines = [line.strip() for line in lines if line.strip()]
    return lines


def get_done_songs(done_file: str) -> Set[str]:
    with open(done_file, 'r') as file:
        lines = file.readlines()

        # Remove leading and trailing whitespaces (including '\n' newline character) for each line
        lines = [line.strip() for line in lines if line.strip()]
    return set(lines)


def start_downloads(queries: List[str], done_file: str):
    len_queries = len(queries)
    done_songs = get_done_songs(done_file)
    print(f"{len_queries} queries found. Starting...")
    for i, query in enumerate(queries):
        print(f"{i + 1}/{len_queries}: {query}")
        if query in done_songs:
            print(f"{query} already downloaded!")
            continue
        results_id = slskd.search(query)
        while not slskd.is_search_complete(results_id):
            sleep(3)

        results = slskd.get_results(results_id)
        best_result = slskd.pop_best_result(results)
        if not best_result:
            print(f"{query} not found :/")
            continue
        print(f"Best results for {query}: {best_result}\nStarting to download {query}...")
        download_start_success = slskd.start_download(best_result)
        if download_start_success:
            with open(done_file, 'a') as file:
                # Adding a newline character '\n' to the end of the string before writing
                file.write(query + '\n')
            print(f"{query} persisted to {done_file}.")
        else:
            print(f"WARNING: {query} didn't succeed!")


if __name__ == "__main__":
    queries = get_queries_from_songs("afterglow.songs")
    start_downloads(queries, 'done.songs')
