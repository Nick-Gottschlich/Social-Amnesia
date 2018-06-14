# Social Amnesia
Social Amnesia aims to make your social media only exist within a time period that you choose. For many people, there is no reason they want to have years old facebook statuses or reddit comments existing and making it easier for online marketers and jilted ex-lovers to profile you. With Social Amnesia, set the time period you want to keep, whitelist posts and items you want to preserve indefinitely, and let Social Amnesia wipe the rest out of existence.

This is in very early versions, this readme will contain a list of what sites are usable and what features are available on each one.

## How to run the App

### Executables

Available in the zip files on the [releases](https://github.com/Nick-Gottschlich/Social-Amnesia/releases) page.

### How to run Social Amnesia from the command line
If you have python3 you can run Social Amnesia directly by cloning this repo and running `python3 SocialAmnesia.py` on a command line. You will have to install several packages with a package manager like "pip" or "pip3".

`pip3 install praw`
`pip3 install arrow`

Note: On windows you may have to copy `tcl86t.dll` and `tk86t.dll` from your `Python3X/DLLs` into the folder with the executable to get this to run.

### How to build the executable for Social Amnesia

Build the executable by first installing cx_freeze by running `pip3 install cx_Freeze`. Then you can build the executable running `python3 setup.py `. This will create a folder called `build`, inside you can a folder with some crazy name, and in that you should see a 'Social Amnesia' executable. Run that executable to start the program.

You can build a mac DMG using `python3 setup.py bdist_dmg` and you can build a windows installer using `python3 setup.py bdist_msi`. These will let you install and use Social Amnesia as an actual application.


## Sites and Features

### Reddit
* Can delete comments and submissions.
* Edits your posts before deleting them. According to [the reddit admins](https://www.reddit.com/r/blog/comments/1dhw2j/reddits_privacy_policy_has_been_rewritten_from/c9qgbbb/) this is an effective way to remove content from reddit.
* Can keep a time range of comments and submissions (in hours)
* Can keep comments or submissions that are above a certain amount of upvotes.
* Can skip gilded comments/submissions.
* Trial run - do a run showing what would be deleted, without actually doing it.

#### How to set up your reddit account

Reddit requires accounts to create a "script" in order for Social Amnesia to run. Don't worry, this is actually quite simple to do. You can see reddit's docs on how to do this [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps). Doing this provides you with the reddit "Client ID" and "Client Secret" you will need to log in within the Social Amnesia app.

## Related software

[Shreddit](https://github.com/x89/Shreddit) - a python program to delete reddit posts/submissions.
[Reddit Overwrite](https://greasyfork.org/en/scripts/10380-reddit-overwrite) - a greasey fork program to overwrite reddit comments.
[Reddit Secure Delete](https://userscripts-mirror.org/scripts/show/166415) - a userscript program to delete reddit comments.
[Nuke Reddit History](https://www.reddit.com/r/NukeRedditHistory/) - a web extension to erase reddit history.
