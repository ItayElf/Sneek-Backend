"""
A file used for encrypting and decrypting text
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    """
    A class that is used to encrypt and decrypt messages
    """

    def __init__(self, key: bytes):
        self._cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, raw: bytes) -> bytes:
        """
        Encrypt the given value using the stored key

        :param raw: the value to encrypt
        :return: the encrypted value
        """
        padded = pad(raw, AES.block_size)
        return self._cipher.encrypt(padded)

    def decrypt(self, encrypted: bytes) -> bytes:
        """
        Decrypts the given encrypted bytes and returns their value

        :param encrypted: the bytes to decrypt
        :return: the decrypted value
        """
        padded = self._cipher.decrypt(encrypted)
        return unpad(padded, AES.block_size)
