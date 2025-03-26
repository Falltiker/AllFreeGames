# AllFreeGames

## Description

AllFreeGames is a Python-based project designed to parse Epic Games, Steam, and GOG platforms for free games currently being offered. The program checks these platforms for giveaways and provides users with a list of free games they can claim.

## Features

- Parses Epic Games Store, Steam, and GOG for free games.
- Displays up-to-date free game offers in the terminal or exports them to a file.
- Regular updates of the game lists.
- Future support for additional platforms (e.g., Go).

## Installation

To get started with AllFreeGames, clone the repository and install the necessary dependencies.

1. Clone the repository:

   ```bash
   git clone https://github.com/Falltiker/AllFreeGames.git
   cd AllFreeGames
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script to check for free games:

```bash
python main.py
```

The program will fetch and display free games from the supported platforms.

### Command-line Options:

- `-p` or `--platform` — Specify which platform to check for free games. Supported platforms: `epic`, `steam`, `gog`. Example:

  ```bash
  python main.py -p epic
  ```

- `-o` or `--output` — Save the results to a file:

  ```bash
  python main.py -o report.txt
  ```

## Example Output

```
Epic Games Store:
- "The World Next Door" - Free until April 1

Steam:
- "Brawlhalla" - Free until March 30

GOG:
- "Shadow Warrior Classic" - Free until April 5
```

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Contributions are always welcome!

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please open an issue in the repository or contact me at email@example.com.
