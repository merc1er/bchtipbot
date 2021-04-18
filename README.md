<div align="center">
  <img src="tippie.png" width="100">
</div>

<div align="center">
  <h3>Bitcoin Cash Telegram tipping bot</h3>
</div>

<div align="center">
  <img src="https://github.com/merc1er/bchtipbot/workflows/Run%20tests/badge.svg" alt="tests">
  <a href="https://www.codefactor.io/repository/github/merc1er/bchtipbot"><img src="https://www.codefactor.io/repository/github/merc1er/bchtipbot/badge" alt="CodeFactor"></a>
  <a href="https://codecov.io/gh/merc1er/bchtipbot"><img src="https://codecov.io/gh/merc1er/bchtipbot/branch/master/graph/badge.svg?token=CIQBH8S6HA"></a>
</div>

---

### 📱 Usage

**Simply open https://t.me/BCHtipbot and talk to the bot.**

#### List of commands

##### Tipping

```
/start - Starts the bot
/deposit - Displays your Bitcoin Cash address for top up
/balance - Shows your balance in Bitcoin Cash
/withdraw - Withdraw your funds. Usage: /withdraw amount|all address
/help - Lists all commands
/tip - Sends a tip. Usage: /tip amount [@username]
```

Note that you can also tip satoshis with, for example: `/tip 2000 satoshi @merc1er`.

##### Price

```
/price - Displays the current price of Bitcoin Cash. Usage: /price [currency_code]
```

For example: `/price` (defaults to USD), `/price eur`, `price BTC` and so on.

### ⚙️ Run development server

Run the following commands:

```shell
pip install -r requirements.txt
python3 tipbot/app.py
```

Credentials and API keys are stored in environment variables (recommended) or in `settings.py` (not recommended for production).


##### Run tests

Simply do:

```shell
python run_tests.py
```

Or, if you want to check coverage, do:

```shell
pip install coverage  # if you don't have it already
coverage run -m unittest
coverage html
```

then open the `htmlcov/index.html` page in a browser.

##### Customize the bot

⚠️ Add the following environment variables:

```shell
FEE_ADDRESS  # the Bitcoin Cash address where you want to collect the fees
FEE_PERCENTAGE  # how much fee you want to charge per tip (over $1)
TOKEN  # is the Telegram API token for the development bot (not for prod)
ADMIN_LIST  # you may add your Telegram username to the list to use the admin commands
```

---

### 🚀 Deployment

Deployments are automatic on `master` if tests pass.

To deploy your own bot, add the environment variables found in the section above (⚠️) and read **[this page](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot)**.

---

### To do

- Reply with stickers
- Queues with Celery/rq
- Implement more tests
- Allow users without a username to use the bot
- Sometimes the bot doesn't get triggered with the `/tip` command while not admin

---

### Support me

Bitcoin Cash: `bitcoincash:qrzd59chq6052tj9fdsllnc55wk5jwpjxqg4crtfwr`
