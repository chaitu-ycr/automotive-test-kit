# canmatrix_webapp

A Streamlit webapp for the [canmatrix](https://github.com/ebroecker/canmatrix) Python package.

## Features

- Upload CAN matrix files in various formats (DBC, ARXML, KCD, FIBEX, XLS, XLSX, XML)
- Explore loaded matrices, view ECUs, frames, and signals
- Export matrices to supported formats

## Usage

### Launch the Web Application

You can start the web application using the provided launcher:

```sh
python -m canmatrix_webapp.run_web_app
```

#### Optional Arguments

- `--server-address ADDRESS`
  Address to bind the Streamlit server (default: system FQDN)
- `--server-port PORT`
  Port to run the Streamlit server on (default: 8502)

Example:

```sh
python -m canmatrix_webapp.run_web_app --server-address 127.0.0.1 --server-port 8502
```

## [source manual](https://chaitu-ycr.github.io/automotive-test-kit/packages/canmatrix_webapp/#source-manual)
