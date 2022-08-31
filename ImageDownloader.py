from msilib.schema import Error
import requests
import shutil

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def get_avatar(url: str, id: int) -> str:
    cleaned_url = url.replace("_normal", "")
    extension = cleaned_url.split(".")[-1]
    resp = requests.get(cleaned_url, stream=True, headers=HEADERS)
    if resp.ok:
        with open(f"./images/avatars/{id}.{extension}", "wb") as f:
            shutil.copyfileobj(resp.raw, f)
    else:
        raise Exception(resp.status_code)
    return f"./images/avatars/{id}.{extension}"


def get_media(url: str, id: int) -> str:
    extension = url.split(".")[-1]
    resp = requests.get(url, stream=True, headers=HEADERS)
    if resp.ok:
        with open(f"./images/medias/{id}.{extension}", "wb") as f:
            shutil.copyfileobj(resp.raw, f)
    else:
        raise Exception(resp.status_code)
    return f"./images/medias/{id}.{extension}"


if __name__ == "__main__":
    x = get_avatar(
        "https://pbs.twimg.com/profile_images/1518474959240065024/dDS6LY6I_normal.jpg",
        0,
    )
    print(x)
