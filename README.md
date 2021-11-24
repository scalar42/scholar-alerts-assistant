# Scholar Alerts Assistant

Save your flooded mailbox from Google Scholar Alerts.  [Scholar Alerts Assistant](https://github.com/scalar42/scholar-alerts-assistant) can automatically merge all the papers for you just in one digest.



## Prerequisites

Set a filter to automatically label the scholar alerts mails in your Gmail, following [these steps](https://support.google.com/a/users/answer/9308833).

Create and turn on [Gmail API](https://developers.google.com/gmail/api/quickstart/python) and download the `credentials.json` into the `./data/`folder.

```shell
.
├── data
    └── credentials.json
```



## Clone & Configure

Download or clone the repository into your local directory.

```git
git clone https://github.com/scalar42/scholar-alerts-assistant.git
```

Then configure `SCHOLAR_LABEL` and `DIGEST_ADDRESS` in the `main.py`

```python
# Note: Remember to change the "Your-alert-label"
SCHOLAR_LABEL = ["UNREAD", "Your-alert-label"]
# Note: Remember to change the "your-gmail-address@gmail.com"
DIGEST_ADDRESS = "your-gmail-address@gmail.com" 
```



## Run the scripts

```python
python main.py
```

Wait and see, it should take less than 1 minute depending on the number of mails.

Note you can use `cron` or other tools to schedule the job.

For the first time, you may need to open the browser to authorize the API.

## Check the results

Open your Gmail client, and you may now see your digest mail. All previous unread scholar alerts mails are now marked read.

## Special Credits

- [Scholar Alters](https://github.com/elikbelik/scholar_alters)

- [Google Scholar alert digest](https://github.com/bzz/scholar-alert-digest)
