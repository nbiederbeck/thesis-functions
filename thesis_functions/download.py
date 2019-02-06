"""Loop over all files in given *days*"""
import requests
import bs4
from tqdm import tqdm
from os import path, makedirs


class MAGICDownloader:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def download_files(self, urls: list, output_directory: str = ".", chunk_size=1024):
        makedirs(output_directory, exist_ok=True)
        for url in urls:
            page = requests.get(url, auth=(self.user, self.password))
            if not page.ok:
                day = url.split("/")[-2]
                print(f"No data found for {day}")
                continue
            soup = bs4.BeautifulSoup(page.text, "lxml")
            download_links = soup.find_all("a", download=True)

            for link in download_links:
                filename = link.attrs["download"]
                if "superstar" in filename:
                    print(f"{filename} not a Data file, not downloading.")
                    continue
                local_filename = f"{output_directory}/{filename}"
                if path.exists(local_filename):
                    print(f"{local_filename} exists, not downloading.")
                    continue
                download_url = url + filename
                print(f"Getting {download_url}")
                stream = requests.get(
                    download_url, stream=True, auth=(self.user, self.password)
                )
                file_size = stream.headers["content-length"]
                with open(local_filename, "wb") as f:
                    for chunk in tqdm(
                        stream.iter_content(chunk_size=chunk_size),
                        total=int(int(file_size) / chunk_size),
                    ):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
