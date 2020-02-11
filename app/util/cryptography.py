"""
Encrypt and decrypt configuration files.

The cipher is AES.
The key is randomized and stored in the keyring.
The key is changed after each decryption.
The data will be sent to keyring.
"""

from keyring import get_password, set_password, delete_password
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt(data):
    """
    Encrypt the configuration file with a random key.

    'Data' should be bytes-like
    """
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    set_password("ScoreChecker Crypto", "scc_key", key.hex())
    set_password("ScoreChecker Crypto", "scc_nonce", nonce.hex())
    set_password("ScoreChecker Crypto", "scc_tag", tag.hex())
    set_password("ScoreChecker Crypto", "scc_data", ciphertext.hex())


def decrypt():
    """
    Decrypt and verify the data with the key stored in keyring.

    The configuration file will be encrypted with a different key after
    decryption.
    """
    key = bytes.fromhex(get_password("ScoreChecker Crypto", "scc_key"))
    nonce = bytes.fromhex(get_password("ScoreChecker Crypto", "scc_nonce"))
    tag = bytes.fromhex(get_password("ScoreChecker Crypto", "scc_tag"))
    ciphertext = bytes.fromhex(get_password("ScoreChecker Crypto", "scc_data"))
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    cipher.verify(tag)
    encrypt(plaintext)
    return plaintext


def reset():
    """
    Reset all keys and data from keyring.

    This function will be invoked when encrypt or decrypt does wrong.
    When this function is invoked, all configuration you've saved will be lost.
    """
    print('Resetting all keys and data from keyring ...')
    set_password("ScoreChecker Crypto", "scc_key", "")
    set_password("ScoreChecker Crypto", "scc_nonce", "")
    set_password("ScoreChecker Crypto", "scc_tag", "")
    set_password("ScoreChecker Crypto", "scc_data", "")
