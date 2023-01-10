
# Startr

Startr is a utility for desktop that aims to be an assistant to help improve the UX of nostr by helping to securely store private keys and connect with your favorite clients.
At the moment the project is functional, although there are many more features to be developed.

## Installation

### Compatibility: linux (tested in Debian, kali, raspbian), more coming

With this guide you can simply copy/paste this commands in terminal

1. Create an environment variable with the latest nostr_console version, take note of it [here](https://github.com/vishalxl/nostr_console/releases/) and modify it accordingly if is needed

  ```sh
  NOSTRVERSION="v0.3.4-beta"
  ```

2. Create an environment variable assigning value to it depending on your system OS architecture:

  * AMD64

  ```sh
  NOSTRARCH="amd64"
  ```

  * ARM64

   ```sh
  NOSTRARCH="arm64"
  ```

3. Open a terminal and clone this repo and put it in the project folder with

 ```sh
 git clone https://github.com/gzuuus/nostr_startr.git && cd nostr_startr
 ```

4. Download the [latest release](https://github.com/vishalxl/nostr_console/releases/) of nostr_console according to your architecture doing

 ```sh
 wget https://github.com/vishalxl/nostr_console/releases/download/$NOSTRVERSION/nostr_console_linux_$NOSTRARCH.zip
 ```

5. Extract and remove .zip file with

 ```sh
 unzip nostr_console_linux_$NOSTRARCH.zip && rm nostr_console_linux_$NOSTRARCH.zip
 ```

💡 If appears you "unzip: command not found" you will need install unzip with `sudo apt install unzip`

6. Make nostr_console file executable with

 ```sh
 chmod +x nostr_console_linux_$NOSTRARCH
 ```

7. Install requirements with

 ```sh
 pip install -r requirements.txt
 ```

## Usage

1. Run startr_app with

 ```sh
 python3 startr_app.py
 ```

2. Follow the steps, Startr will guide you to securely store or create your nostr identity

## Update only Startr

1. Go to your project folder

  ```sh
  cd nostr_startr
  ```

2. Pull the new repository changes

  ```sh
  git pull origin main
  ```

2. Type the next command to install new dependencies if necessary

  ```sh
  pip install -r requirements.txt
  ```

3. Run startr_app again with

 ```sh
 python3 startr_app.py
 ```

4. Enjoy new features

## Update only Nostr console

1. Stop start_app with option "6" until show the prompt and go to the project folder

  ```sh
  cd nostr_startr
  ```

2. Modify the environment variable with the nostr_console [new version available](https://github.com/vishalxl/nostr_console/releases) and remove the deprecated old version

  ```sh
  NOSTRVERSION="v0.x.x-beta"
  ```

  ```sh
  rm nostr_console*
  ```

3. Download the [latest release](https://github.com/vishalxl/nostr_console/releases/) of nostr_console

  ```sh
  wget https://github.com/vishalxl/nostr_console/releases/download/$NOSTRVERSION/nostr_console_linux_$NOSTRARCH.zip
  ```

4. Make nostr_console file executable with

 ```sh
 chmod +x nostr_console_linux_$NOSTRARCH
 ```

5. Run startr_app again with

  ```sh
  python3 startr_app.py
  ```

## Features

- [x] Crate new or store private key
- [x] Store keys in a safe way
- [x] Connection and launch of [nostr_console](https://github.com/vishalxl/nostr_console) in a more secure way
- [x] Multi account/key option
- [x] Shows a direct link and qr code when show/decrypt keys to easy share

### Roadmap

- [x] Improve Key Derivation scheme
- [ ] Nostr console auto install
- [ ] Multi configuration options (arguments/flags) for starting nostr_console
- [ ] RSS reader
- [ ] Make it compatible with more OS
- [ ] Bundle application into a single package
- [ ] More on the way

More docs in process