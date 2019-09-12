# Bitcoin Tipping Bot

## Usage

Simply open https://t.me/BitcoinTippingBot and talk to the bot.

### List of commands

```
start - Starts the bot
deposit - Displays your Bitcoin Cash address for top up
balance - Shows your balance in Bitcoin Cash
withdraw - Withdraw your funds. Usage: /withdraw [amount] [address]
help - Lists all commands
tip - Sends a tip. Usage: /tip [amount] [@username]
```

## Run development server

Run the following commands:

```shell
pip install -r requirements.txt
python app.py
```

Credentials and API keys are stored in `settings.py`

## To do

- top ups and withdrawals
- migration to PostgreSQL
- logging
- prepare for deployment
