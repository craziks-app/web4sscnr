# 
## Deploying your own

#### The Easiest Way [Heroku ONLY 👾]

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

- Make sure to read below what the configuration variables do.


#### The Legacy Way

- if you want to run this bot in your GNU/Linux System,
- `cd code_directory`
- Enter `python3 setup.py`
- Enter the 'mandatory' environment variables as prompted
- Once setup is done, enter `python3 -m bot`
- To enter optional variables, copy the key from sample_config.env and paste in config.env.

## ENVironment VARiables

#### Mandatory Environment Variables

- `TG_BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.

- `APP_ID`,
- `API_HASH`: Get these two values from [my.telegram.org/apps](https://my.telegram.org/apps).

- `AUTH_CHANNEL`:
  Go to [@Rose](https://telegram.dog/MissRose_bot), send /id in the chat to get this value.

- `MONGO_URL`: You can get this value by creating a cluster on [MongoDB](https://mongodb.com) and getting the connection url.

* **Note** You MUST enter 0.0.0.0/0 in the allowed ip addresses range in your cluster.

#### Optional Environment Variables

- `TG_BOT_WORKERS`: Number of workers to use. 4 is the recommended (and default) amount, but your experience may vary.
  **Note** that going crazy with more workers won't necessarily speed up your bot, given the amount of sql data accesses, and the way python asynchronous calls work.

- `COMMM_AND_PRE_FIX`: The command prefix. Telegram, by default, recommeds the use of `/`, which is the default prefix. ~~Please don't change this unless you know what you're doing.~~

- `START_COMMAND`: The command to check if the bot is alive, or for users to start the robot.

- `START_OTHER_USERS_TEXT`: The message that your bot users would see on sending /start message.

- `ONLINE_CHECK_START_TEXT`: The message that the bot administrators can use to check if bot is online.

- `HELP_MEHH`: The message that bot users would see on sending /help message.

- `TZ`: Timezone to make sure time related functions work as required.

- `LOG_FILE_ZZGEVC`: The path to store log files.

- `REQUEST_INTERVAL`: Time interval between each check.

## License

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [LICENSE](./LICENSE) for more details.
