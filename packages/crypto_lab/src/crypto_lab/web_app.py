import streamlit as st
from Crypto.Hash import SHA256, HMAC
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2, scrypt, HKDF
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA, ECC
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Cipher import PKCS1_OAEP
import ast
from typing import Any

class WebApp:
    """Streamlit-based cryptographic algorithms and protocols playground."""

    def __init__(self) -> None:
        # UI constants
        self.KDF_METHODS = ["PBKDF2", "scrypt", "HKDF"]
        self.ECC_CURVE = "P-256"
        self.AES_KEY_LENGTHS = (16, 24, 32)
        self.RANDOM_BYTES_MIN = 1
        self.RANDOM_BYTES_MAX = 64
        self.RANDOM_BYTES_DEFAULT = 16
        self.KDF_DKLEN_MIN = 16
        self.KDF_DKLEN_MAX = 64
        self.KDF_DKLEN_DEFAULT = 32
        self.SHAMIR_N_MIN = 2
        self.SHAMIR_N_MAX = 10
        self.SHAMIR_N_DEFAULT = 5
        self.SHAMIR_K_MIN = 2
        self.SHAMIR_K_DEFAULT = 3

        st.title("🔐 Cryptographic Algorithms and Protocols Lab")

    def sha256_hash_section(self) -> None:
        """SHA-256 hashing demo."""
        st.header("1. SHA-256 Hashing")
        data = st.text_input("Enter data to hash:", key="sha256_data")
        if st.button("Generate SHA-256 Hash", key="sha256_btn"):
            if not data:
                st.error("Input data is required.")
            else:
                try:
                    h = SHA256.new(data.encode())
                    st.code(h.hexdigest())
                except Exception as e:
                    st.error(f"Error: {e}")

    def random_bytes_section(self) -> None:
        """Random bytes generation demo."""
        st.header("2. Random Number Generation")
        length = st.slider(
            "Select number of random bytes",
            self.RANDOM_BYTES_MIN,
            self.RANDOM_BYTES_MAX,
            self.RANDOM_BYTES_DEFAULT,
            key="rand_bytes_len"
        )
        if st.button("Generate Random Bytes", key="rand_bytes_btn"):
            try:
                st.code(get_random_bytes(length).hex())
            except Exception as e:
                st.error(f"Error: {e}")

    def hmac_section(self) -> None:
        """HMAC (SHA-256) demo."""
        st.header("3. HMAC (SHA-256)")
        hmac_key = st.text_input("Enter HMAC key:", key="hmac_key")
        hmac_data = st.text_input("Enter data to authenticate:", key="hmac_data")
        if st.button("Generate HMAC", key="hmac_btn"):
            if not hmac_key or not hmac_data:
                st.error("HMAC key and data are required.")
            else:
                try:
                    h = HMAC.new(hmac_key.encode(), digestmod=SHA256)
                    h.update(hmac_data.encode())
                    st.code(h.hexdigest())
                except Exception as e:
                    st.error(f"Error: {e}")

    def kdf_section(self) -> None:
        """Key derivation functions demo."""
        st.header("4. Key Derivation Functions")
        password = st.text_input("Password:", key="kdf_password")
        salt = st.text_input("Salt (as text):", key="kdf_salt")
        dk_len = st.slider(
            "Derived key length",
            self.KDF_DKLEN_MIN,
            self.KDF_DKLEN_MAX,
            self.KDF_DKLEN_DEFAULT,
            key="kdf_len"
        )
        kdf_method = st.selectbox("Select KDF", self.KDF_METHODS, key="kdf_method")
        if st.button("Derive Key", key="kdf_btn"):
            if not password or not salt:
                st.error("Password and salt are required.")
            else:
                try:
                    salt_bytes = salt.encode()
                    if kdf_method == "PBKDF2":
                        key = PBKDF2(password, salt_bytes, dkLen=dk_len)
                    elif kdf_method == "scrypt":
                        # Provide required N, r, p parameters
                        key = scrypt(password, salt_bytes, key_len=dk_len, N=2**14, r=8, p=1)
                    elif kdf_method == "HKDF":
                        key = HKDF(password.encode(), dk_len, salt_bytes, SHA256)
                    else:
                        raise ValueError("Unknown KDF method.")
                    st.code(key.hex())
                except Exception as e:
                    st.error(f"Error: {e}")

    def aes_section(self) -> None:
        """AES encryption (CBC mode) demo."""
        st.header("5. AES Encryption (CBC Mode)")
        aes_key = st.text_input("AES key (16/24/32 bytes):", key="aes_key")
        aes_data = st.text_input("Data to encrypt:", key="aes_data")
        if st.button("Encrypt with AES", key="aes_btn"):
            key_bytes = aes_key.encode()
            if not aes_key:
                st.error("AES key is required.")
            elif len(key_bytes) not in self.AES_KEY_LENGTHS:
                st.error("AES key must be 16, 24, or 32 bytes.")
            elif not aes_data:
                st.error("Data to encrypt is required.")
            else:
                try:
                    cipher = AES.new(key_bytes, AES.MODE_CBC)
                    ct = cipher.encrypt(pad(aes_data.encode(), AES.block_size))
                    st.code(f"IV: {cipher.iv.hex()}")
                    st.code(f"Ciphertext: {ct.hex()}")
                except Exception as e:
                    st.error(f"Error: {e}")

    def rsa_section(self) -> None:
        """RSA encryption demo."""
        st.header("6. RSA Encryption")
        rsa_data = st.text_input("Data to encrypt with RSA:", key="rsa_data")
        if st.button("Generate RSA Keys", key="rsa_gen_btn"):
            try:
                rsa_key = RSA.generate(2048)
                st.session_state['rsa_private'] = rsa_key.export_key()
                st.session_state['rsa_public'] = rsa_key.publickey().export_key()
                st.code(st.session_state['rsa_public'].decode())
            except Exception as e:
                st.error(f"Error generating RSA keys: {e}")

        if st.button("Encrypt with RSA", key="rsa_enc_btn"):
            if 'rsa_public' in st.session_state:
                try:
                    pub_key = RSA.import_key(st.session_state['rsa_public'])
                    cipher = PKCS1_OAEP.new(pub_key)
                    ct = cipher.encrypt(rsa_data.encode())
                    st.code(ct.hex())
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Generate RSA keys first.")

    def ecc_section(self) -> None:
        """ECC key generation demo."""
        st.header("7. ECC Key Exchange")
        if st.button("Generate ECC Keys", key="ecc_btn"):
            try:
                ecc_key = ECC.generate(curve=self.ECC_CURVE)
                st.session_state['ecc_private'] = ecc_key.export_key(format='PEM')
                st.session_state['ecc_public'] = ecc_key.public_key().export_key(format='PEM')
                st.code(st.session_state['ecc_public'])
            except Exception as e:
                st.error(f"Error: {e}")

    def rsa_transport_section(self) -> None:
        """RSA key transport demo."""
        st.header("8. RSA Key Transport")
        transport_key = st.text_input("Key to transport:", key="rsa_transport_key")
        if st.button("Transport Key with RSA", key="rsa_transport_btn"):
            if 'rsa_public' in st.session_state:
                try:
                    pub_key = RSA.import_key(st.session_state['rsa_public'])
                    cipher = PKCS1_OAEP.new(pub_key)
                    ct = cipher.encrypt(transport_key.encode())
                    st.code(ct.hex())
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Generate RSA keys first.")

    def signature_section(self) -> None:
        """Digital signature (RSA) demo."""
        st.header("9. Digital Signature (RSA)")
        sign_data = st.text_input("Data to sign:", key="sign_data")
        if st.button("Sign with RSA", key="sign_btn"):
            if 'rsa_private' in st.session_state:
                try:
                    priv_key = RSA.import_key(st.session_state['rsa_private'])
                    h = SHA256.new(sign_data.encode())
                    signature = pkcs1_15.new(priv_key).sign(h)
                    st.session_state['signature'] = signature
                    st.code(signature.hex())
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Generate RSA keys first.")

        if st.button("Verify RSA Signature", key="verify_btn"):
            if 'rsa_public' in st.session_state and 'signature' in st.session_state:
                try:
                    pub_key = RSA.import_key(st.session_state['rsa_public'])
                    h = SHA256.new(sign_data.encode())
                    pkcs1_15.new(pub_key).verify(h, st.session_state['signature'])
                    st.success("Signature is valid.")
                except (ValueError, TypeError):
                    st.error("Signature is invalid.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Missing signature or public key.")

    def shamir_section(self) -> None:
        """Shamir's Secret Sharing demo."""
        st.header("10. Shamir's Secret Sharing")
        secret = st.text_input("Secret to split:", key="shamir_secret")
        n = st.slider(
            "Total shares",
            self.SHAMIR_N_MIN,
            self.SHAMIR_N_MAX,
            self.SHAMIR_N_DEFAULT,
            key="shamir_n"
        )
        k = st.slider(
            "Threshold to reconstruct",
            self.SHAMIR_K_MIN,
            n,
            self.SHAMIR_K_DEFAULT,
            key="shamir_k"
        )
        if st.button("Split Secret", key="shamir_split_btn"):
            if not secret:
                st.error("Secret is required.")
            else:
                try:
                    # Ensure secret is exactly 16 bytes
                    secret_bytes = secret.encode()
                    if len(secret_bytes) < 16:
                        secret_bytes = secret_bytes.ljust(16, b'\0')
                    elif len(secret_bytes) > 16:
                        from Crypto.Hash import SHA256
                        secret_bytes = SHA256.new(secret_bytes).digest()[:16]
                    shares = Shamir.split(k, n, secret_bytes)
                    st.session_state['shares'] = [(i, s.hex()) for i, s in shares]
                    st.write(st.session_state['shares'])
                except Exception as e:
                    st.error(f"Error: {e}")

        combine_input = st.text_area(
            "Enter shares to combine (e.g., [(1, 'abc...'), (2, 'def...')])",
            key="shamir_combine_input"
        )
        if st.button("Combine Shares", key="shamir_combine_btn"):
            if not combine_input.strip():
                st.error("Please enter shares to combine.")
            else:
                try:
                    parsed = ast.literal_eval(combine_input)
                    if not (isinstance(parsed, list) and all(isinstance(t, tuple) and len(t) == 2 for t in parsed)):
                        raise ValueError("Input must be a list of (index, hexstring) tuples.")
                    shares = [(i, bytes.fromhex(s)) for i, s in parsed]
                    recovered = Shamir.combine(shares)
                    # Remove padding zeros if present
                    recovered_str = recovered.rstrip(b'\0').decode(errors='replace')
                    st.success(f"Recovered Secret: {recovered_str}")
                except Exception as e:
                    st.error(f"Error: {e}")

    def run(self) -> None:
        """Run all Streamlit UI sections."""
        self.sha256_hash_section()
        self.random_bytes_section()
        self.hmac_section()
        self.kdf_section()
        self.aes_section()
        self.rsa_section()
        self.ecc_section()
        self.rsa_transport_section()
        self.signature_section()
        self.shamir_section()

if __name__ == "__main__":
    app = WebApp()
    app.run()
