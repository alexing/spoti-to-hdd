from time import sleep

from slskd_utils import Slskd

slskd = Slskd()
failed_downloads = slskd.get_all_failed_downloads()
while failed_downloads:
    len_failed_downloads = len(failed_downloads)
    print(f"{len_failed_downloads} failed downloads found. Starting...")

    for i, failed_download in enumerate(failed_downloads):
        print(f"{i + 1}/{len_failed_downloads}: {failed_download}")
        download_start_success = slskd.start_download(failed_download)
        print(f"Starting to download {failed_download}...")
        sleep(15)
    failed_downloads = slskd.get_all_failed_downloads()