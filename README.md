# Add song to Spotify Playlist

script to add song to spotify playlist

can set your own playlist id to add it to

can create an automator script that runs this, and assign the script to a shortcut in keyboard shortcut settings e.g.

```
cd ~/Documents/My\ Projects/Spotify\ Playlist\ Automation
source myenv/bin/activate
python3 main.py
```

for this to notify you, need to create automator application named `AddedToPlaylist`
and make it run applescript:

```
set notificationText to (do shell script "echo $NOTIFICATION_TEXT")
set notificationTitle to (do shell script "echo $NOTIFICATION_TITLE")

display notification notificationText with title notificationTitle
```

can then drag a custom png in finder to set as the application icon in finder e.g. playlist cover/like icon so notification looks nice

## Setup

- install python
- pip install requests/other files needed
  - if brew installed python, need to create virtual space for pip installs, and activate before running code
  - `source myenv/bin/activate`

source myenv/bin/activate

### Potential Improvements:

- more easily switch playlist without having to edit code with playlist id
  - e.g. Config UI page fetches and displays your playlists, select which you want to add to
- handle reauth better: currently have to run `sudo python3 main.py`
  - issue -> need sudo permission to edit folder localData - permissions issue?
- Add this application as part of larger productivity application
