# SocialScrubber
Cleans out the old gunk from your social media profiles!

This is in very early versions, but the eventual goal is to create a user-friendly app that will allow one click and scheduled cleaning of social media accounts. What does "cleaning" mean? On a site like twitter, this could be removing old tweets, retweets, and likes. On a site like reddit, this could be deleting submissions and comments. This readme will contain a list of what sites are usable and what features are available on each one.

## How to run the App

### Executables

Available in the zip files on the [releases](https://github.com/Nick-Gottschlich/Social-Amnesia/releases) page.

### How to run SocialScrubber from the command line
If you have python3 you can run SocialScrubber directly by cloning this repo and running `python3 SocialScrubber.py` on a command line. You will have to install several packages with a package manager like "pip" or "pip3".

`pip3 install praw`
`pip3 install arrow`

Note: On windows you may have to copy `tcl86t.dll` and `tk86t.dll` from your `Python3X/DLLs` into the folder with the executable to get this to run.

### How to build the executable for SocialScrubber

Build the executable by first installing cx_freeze by running `pip3 install cx_Freeze`. Then you can build the executable running `python3 setup.py `. This will create a folder called `build`, inside you can a folder with some crazy name, and in that you should see a 'SocialScrubber' executable. Run that executable to start the program.


## Sites and Features

### Reddit
* Can delete comments and submissions.
* Edits your posts before deleting them. According to [the reddit admins](https://www.reddit.com/r/blog/comments/1dhw2j/reddits_privacy_policy_has_been_rewritten_from/c9qgbbb/) this is an effective way to remove content from reddit.
* Can keep a time range of comments and submissions (in hours)
* Can keep comments or submissions that are above a certain amount of upvotes.
* Trial run - do a run showing what would be deleted, without actually doing it.

#### How to set up your reddit account

Reddit requires accounts to create a "script" in order for SocialScrubber to run. Don't worry, this is actually quite simple to do. You can see reddit's docs on how to do this [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps). Doing this provides you with the reddit "Client ID" and "Client Secret" you will need to log in within the SocialScrubber app.

## Related software

[Shreddit](https://github.com/x89/Shreddit) - a python program to delete reddit posts/submissions.