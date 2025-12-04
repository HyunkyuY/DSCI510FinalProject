import requests
import os

def download_file_from_gdrive(gdrive_url: str, local_filename: str) -> str:
    """
    Downloads a file from Google Drive to a local filename.
    File must be shared with: 'Anyone with the link'.
    """
    file_id = gdrive_url.split("/")[-2]
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Skip download if file already exists
    if os.path.exists(local_filename):
        print(f"Found existing file: {local_filename}")
        return local_filename

    print(f"Downloading {local_filename} from Google Drive...")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"Downloaded: {local_filename}")
    return local_filename
