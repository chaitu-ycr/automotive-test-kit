# crypto_lab

A Python Streamlit-based web application for experimenting with cryptographic algorithms and protocols using [PyCryptodome](https://www.pycryptodome.org/).

## Features

- Interactive web UI for cryptographic demos, including:
  - SHA-256 hashing
  - Random number generation
  - HMAC (SHA-256)
  - Key derivation functions (PBKDF2, scrypt, HKDF)
  - AES encryption (CBC mode)
  - RSA encryption and key transport
  - ECC key generation
  - Digital signatures (RSA)
  - Shamir's Secret Sharing

## Getting Started

### Running the Web Application

- Launch the Streamlit web app using the main entry point:
  ```
  python -m crypto_lab.run_web_app [--server-address ADDRESS] [--server-port PORT]
  ```
  - `--server-address`: Address to bind the Streamlit server (default: system FQDN)
  - `--server-port`: Port to run the Streamlit server on (default: 8503)

## [source manual](https://chaitu-ycr.github.io/automotive-test-kit/packages/crypto_lab/#source-manual)
