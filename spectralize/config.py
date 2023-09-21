import os


def generate_secret_key():
    # Attempt to read the secret from the secret file
    # This will fail if the secret has not been written
    try:
        with open(".secret_key", "rb") as secret:
            key = secret.read()
    except (OSError, IOError):
        key = None

    if not key:
        key = os.urandom(64)
        # Attempt to write the secret file
        # This will fail if the filesystem is read-only
        try:
            with open(".secret_key", "wb") as secret:
                secret.write(key)
                secret.flush()
        except (OSError, IOError):
            pass

    return key


class Config:
    SECRET_KEY: str = os.environ.get("SAECRET_KEY") or generate_secret_key()
