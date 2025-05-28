# Bless Network BOT
Bless Network BOT

- Register Here : [Bless Network](https://bless.network/dashboard?ref=BPSZ9G)
- Use Code `BPSZ9G`

## Features

  - Auto Get Account Information
  - Auto Run With [Monosans](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt) Proxy - `Choose 1`
  - Auto Run With Private Proxy - `Choose 2`
  - Auto Run Without Proxy - `Choose 3`
  - Auto Rotate Invalid Proxies - `y` or `n`
  - Auto Send Ping Every 10 Minutes
  - Auto Update Node Uptime Every 30 Minutes
  - Multi Accounts & Multi Nodes With Threads

## Requiremnets

- Make sure you have Python3.9 or higher installed and pip.

## Instalation

1. **Clone The Repositories:**
   ```bash
   git clone https://github.com/vonssy/Bless-BOT.git
   ```
   ```bash
   cd Bless-BOT
   ```

2. **Install Requirements:**
   ```bash
   pip install -r requirements.txt # or pip3 install -r requirements.txt
   ```

## Configuration

- **accounts.json:** You will find the file `accounts.json` inside the project directory. Make sure `accounts.json` contains data that matches the format expected by the script. Here are examples of file formats:
  ```json
    [
      {
          "B7S_AUTH_TOKEN": "your_b7s_auth_token_account_1",
          "Nodes": [
              {
                  "PubKey": "your_pubkey_1_account_1",
                  "HardwareId": "your_hardware_id_1_account_1"
              },
              {
                  "PubKey": "your_pubkey_2_account_1",
                  "HardwareId": "your_hardware_id_1_account_1"
              },
              {
                  "PubKey": "your_pubkey_3_account_1",
                  "HardwareId": "your_hardware_id_1_account_1"
              },
              {
                  "PubKey": "your_pubkey_4_account_1",
                  "HardwareId": "your_hardware_id_1_account_1"
              },
              {
                  "PubKey": "your_pubkey_5_account_1",
                  "HardwareId": "your_hardware_id_1_account_1"
              }
          ]
      },
      {
          "B7S_AUTH_TOKEN": "your_b7s_auth_token_account_2",
          "Nodes": [
              {
                  "PubKey": "your_pubkey_1_account_2",
                  "HardwareId": "your_hardware_id_1_account_2"
              },
              {
                  "PubKey": "your_pubkey_2_account_2",
                  "HardwareId": "your_hardware_id_1_account_2"
              },
              {
                  "PubKey": "your_pubkey_3_account_2",
                  "HardwareId": "your_hardware_id_1_account_2"
              },
              {
                  "PubKey": "your_pubkey_4_account_2",
                  "HardwareId": "your_hardware_id_1_account_2"
              },
              {
                  "PubKey": "your_pubkey_5_account_2",
                  "HardwareId": "your_hardware_id_1_account_2"
              }
          ]
      }
    ]
  ```

- **proxy.txt:** You will find the file `proxy.txt` inside the project directory. Make sure `proxy.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    ip:port # Default Protcol HTTP.
    protocol://ip:port
    protocol://user:pass@ip:port
  ```

## Run

```bash
python bot.py # or python3 bot.py
```

## Read
- **Note:** For hardware id, u can use `gen_hardware_id.py` or use your own. The generated hardware id will be saved to `hardware_ids.txt`.
```bash
python gen_hardware_id.py # or python3 gen_hardware_id.py
```

## Buy Me a Coffee

- **EVM:** 0xe3c9ef9a39e9eb0582e5b147026cae524338521a
- **TON:** UQBEFv58DC4FUrGqinBB5PAQS7TzXSm5c1Fn6nkiet8kmehB
- **SOL:** E1xkaJYmAFEj28NPHKhjbf7GcvfdjKdvXju8d8AeSunf
- **SUI:** 0xa03726ecbbe00b31df6a61d7a59d02a7eedc39fe269532ceab97852a04cf3347

Thank you for visiting this repository, don't forget to contribute in the form of follows and stars.
If you have questions, find an issue, or have suggestions for improvement, feel free to contact me or open an *issue* in this GitHub repository.

**vonssy**