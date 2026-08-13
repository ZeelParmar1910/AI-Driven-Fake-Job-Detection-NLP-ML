import os
import urllib.request

def download_data():
    url = "https://raw.githubusercontent.com/abbylmm/fake_job_posting/main/data/fake_job_postings.csv"
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    file_path = os.path.join(data_dir, "fake_job_postings.csv")
    print(f"Downloading dataset from {url}...")
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"Dataset successfully downloaded and saved to: {file_path}")
        print(f"Size: {os.path.getsize(file_path)} bytes")
    except Exception as e:
        print(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    download_data()
