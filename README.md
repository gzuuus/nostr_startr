
![image](https://i.ibb.co/hsvGcMJ/startr-splash2.png)

# Startr

Startr is a utility for desktop that aims to be an assistant to help improve the UX of nostr by helping to securely store private keys and connect with your favorite clients.

At the moment the project is functional, although there are many more features to be developed.

## Installation

### Compatibility: linux (tested in Debian, kali, raspbian), more coming
  💡At the moment nostr_console has a bug that makes it unusable, so it cannot be used with Startr. **The rest of the features of Startr are working fine.**
  
With this guide you can simply copy/paste this commands in terminal

  

1. Open a terminal, clone this repo and put it in the project folder with

  

```sh

git clone  https://github.com/gzuuus/nostr_startr.git && cd  nostr_startr

```

  

2. Install requirements with

  

```sh

pip install  -r  requirements.txt

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

  

1. Run startr_app with

  

```sh

python3 startr_app.py

```

  

2. In the menu select option `6. Install/update nostr_console`

  

Alternatively, you can:

  

1. Download the [latest release](https://github.com/vishalxl/nostr_console/releases/) of nostr_console

  

2. Make nostr_console file executable with

  

```sh

chmod +x  nostr_console_binary_file

```

3. Run startr_app again with

  

```sh

python3 startr_app.py

```
  

## Features
- [x] Crate new or store private key
- [x] Store keys in a safe way
- [x] Connection and launch of [nostr_console](https://github.com/vishalxl/nostr_console) in a more secure way (nostr_console is currently not working due to a bug not related to Startr)
- [x] Multi account/key option
- [x] Shows a direct link and qr code when show/decrypt keys to easy share

### Roadmap

- [x] Improve Key Derivation scheme
- [x] Nostr console auto install
- [ ] Request your metadata from a specific relay list to store it offline
- [ ] Rebroadcast your metadata from your offline backup to a list of specific relays
- [ ] Nuke events from key in list of relays
- [ ] RSS reader
- [ ] Make it compatible with more OS
- [ ] Bundle application into a single package
- [ ] More on the way

More docs in process
