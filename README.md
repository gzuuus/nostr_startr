
# Startr

Startr is a utility for desktop that aims to be an assistant to help improve the UX of nostr by helping to securely store private keys and connect with your favorite clients.
At the moment the project is functional, although there are many more features to be developed.

## Installation:
#### Compatibility: linux, more coming
1. Create a folder for the project, open a terminal and git clone this repo `'git clone https://github.com/gzuuus/nostr_startr'`
2. Download the latest release of nostr_console: [nostr_console release page](https://github.com/vishalxl/nostr_console/releases/) and put it in the project folder (remember make nostr_console file executable)
3. Open a terminal `'cd <path/to/project_folder>'` and do `'pip install -r requirements.txt'`
4. when finish, run startr_app with `'python startr_app.py'` in the terminal
5. Follow the steps, Startr will guide you to securely store or create your nostr identity

## Usage:

1. Open terminal and `'cd <path/to/project_folder>'` then `'python3 startr_app.py'` (remember make nostr_console file executable)
2. Follow the steps

## Features:
 - [x] Crate new or store private key
 - [x] Store keys in a safe way
 - [x] Connection and launch to nostr_console (linux only)
### Roadmap:
 - [ ] Multi account/key option
 - [ ] Multi configuration option for starting nostr_console
 - [x] Improve Key Derivation scheme 
 - [ ] Make it compatible with more OS
 - [ ] Bundle application into a single package
 - [ ] More on the way

More docs in process
