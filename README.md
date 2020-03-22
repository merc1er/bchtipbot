<div align="center">
  <img src="tippie.png" width="100">
</div>

<div align="center">
  <h3>Bitcoin Cash Telegram tipping bot</h3>
</div>

<div align="center">
  <img src="https://travis-ci.com/merc1er/bchtipbot.svg?token=ikFpFZzenHdDVbwQsxJX&branch=master" alt="Build">
</div>

## Usage

Simply open https://t.me/BCHtipbot and talk to the bot.

### List of commands

```
/start - Starts the bot
/deposit - Displays your Bitcoin Cash address for top up
/balance - Shows your balance in Bitcoin Cash
/withdraw - Withdraw your funds. Usage: /withdraw amount|all address
/help - Lists all commands
/tip - Sends a tip. Usage: /tip amount [@username]
/price - Displays the current price of Bitcoin Cash. Usage: /price [currency_code]
```

## Run development server

Run the following commands:

```shell
pip install -r requirements.txt
python tipbot/app.py
```

Credentials and API keys are stored in `settings.py`

#### Customize the bot

In `settings.py`, edit:

```shell
FEE_ADDRESS  # the Bitcoin Cash address where you want to collect the fees
FEE_PERCENTAGE  # how much fee you want to charge per tip (over $1)
TOKEN  # is the Telegram API token for the development bot (not for prod)
ADMIN_LIST  # you may add your Telegram username to the list to use the admin commands
```

## Deployment

Deploys are automatic on `master`.

## To do

- Reply with stickers
- Queues with Celery/rq
- Implement more tests
- Allow users without a username to use the bot
