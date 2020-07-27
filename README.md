![Social Amnesia Logo](/assets/FullLogo.png)
![Quick Delete Demo](/assets/QuickDeleteDemo.gif)


# Social Amnesia
Social Amnesia aims to make your social media (twitter/reddit) only exist within a time period that you choose. For many people, there is no reason they want to have years old tweets or reddit comments publicly accessible. With Social Amnesia, set the time period you want to keep, whitelist posts and items you want to preserve indefinitely, and let Social Amnesia wipe the rest out of existence.

## Sponsor the development of Social Amnesia

You can [sponsor me on GitHub](https://github.com/sponsors/Nick-Gottschlich) to fund the continued development of Social Amnesia!
You can also make a one-time donation directly via:

- [Venmo](https://venmo.com/code?user_id=1345298144165889018)
- [Paypal](https://www.paypal.me/nickpgott)
- Send Bitcoin to 36Bq7F2JZdYEWLyB8jPWB1XuLCBCCkLvHn

![DonateQR](/assets/DonateQR.png)

And please [follow me on Twitter](https://twitter.com/NickGottschlich) to receive updates on the development of Social Amnesia!

## How to build/run Social Amnesia

### Executables

This is the simplest option. Bundled and easily usable files for Mac, Windows and Linux are available on the [releases](https://github.com/Nick-Gottschlich/Social-Amnesia/releases) page.

### How to run Social Amnesia from the command line
First, clone this repo.

In order to run Social Amnesia, you will need to set up Reddit and Twitter APIs.

For Reddit, you will want to create an installed app using https://www.reddit.com/prefs/apps. Set your redirect url to be `https://google.com`. Then you will need to create a `redditSecrets.ts` file in the `src/` directory:

```javascript
const redditAPI = {
  userAgent: "Social-Amnesia-2.0",
  clientId: "YOUR_CLIENT_ID"
};

export default redditAPI;
```

For Twitter, create an app using https://developer.twitter.com/en/apps, enable `Sign in with Twitter`, set the Callback URL to be `https://google.com`, and then create a `twitterSecrets.ts` file in the `src/` directory:

```javascript
const twitterAPI = {
  consumer_key: "YOUR_CONSUMER_KEY",
  consumer_secret: "YOUR_CONSUMER_SECRET",
  access_token: "YOUR_ACCESS_TOKEN",
  access_token_secret: "YOUR_ACCESS_TOKEN_SECRET"
};

export default twitterAPI;
```

Then you can run `yarn run electron:serve` and start developing!

### How to build the executables for Social Amnesia

Simply run `yarn run electron:serve` once you have completed the steps above. Output is sent to the `dist_electron` folder.

## Sites and Features

### Reddit
* Delete comments and posts, individually or en masse.
* Edits your posts before deleting them. According to [the reddit admins](https://www.reddit.com/r/blog/comments/1dhw2j/reddits_privacy_policy_has_been_rewritten_from/c9qgbbb/) this is an effective way to remove content from reddit.
* Keep a time range of comments and submissions.
* Keep comments or submissions that reach a certain amount of upvotes.
* Whitelist specific posts and comments you want to save.
* Schedule deletions daily.

### Twitter
* Delete tweets, retweets, replies and remove "favorites" (aka ❤️'s), individually or en masse.
* Keep a time range of tweets, retweets, replies and favorites.
  * In the case of favorites, this is done by the time the favorited item was created, NOT the time it was favorited at.
* Keep tweets that have reached a certain amount of retweets or favorites.
  * This option ignores retweets, these will be removed no matter what if they are out of the time range.
* Whitelist specific tweets and favorites you want to save.
* Schedule deletions daily.

## Contributing

Contributions are not only welcomed but greatly appreciated. If you have any idea for a new feature, or find a bug, you can open up a [new issue](https://github.com/Nick-Gottschlich/Social-Amnesia/issues/new) and report it. Better yet, fork this project, write up some code, and [submit a new pull request](https://github.com/Nick-Gottschlich/Social-Amnesia/compare).

Don't feel comfortable coding? That's okay! There are plenty of other ways to contribute to this project: 
- The easiest is to just share it. Post it (ironically?) on your social media. Tell your friends and family. Launch t-shirts at bewildered pedestrians. Drop pamphlets out of air planes. Get creative!
- UX people are needed to help make mockups to improve the design of the application.
- Do you have a social media account with lots of posts you would like to donate to the cause? Accounts like these can be used to help us bug hunt. Open an issue or tweet [@NickGottschlich](https://twitter.com/NickGottschlich).
- Be a user tester! Just record your experience using this the first time using screen recording software and upload it as [an issue](https://github.com/Nick-Gottschlich/Social-Amnesia/issues/new). Better yet if you can record yourself talking through your thoughts as you try out the software for the first time!

## Limitations

- Reddit
  - reddit API currently only indexes ~1k most recent items back (confirmed for comments, not submissions)
- Twitter
  - twitter API currently only indexes ~3200 tweets and favorites back

## Tech talks / Blog Posts

*Note: These talks and posts may be using the user interface from Social Media 1.0, which looks significantly different from the new version!*

[@NickGottschlich](https://twitter.com/NickGottschlich) spoke about Social Amnesia at the Austin Python Monthly Meetup on April 10th, 2019.

Youtube link: https://www.youtube.com/watch?v=wPv_pLofedU

Link to slides: https://nickpgott.com/files/AbusingSocialMediaAPIs.pdf 

Medium Article about Social Amnesia: https://medium.com/@nickpgott/ab-using-social-media-apis-using-python-for-privacys-sake-7091b3f76666

## Links

- [Official Website](https://socialamnesia.com) - currently redirects to this github repo.
- [Official Twitter Account](https://twitter.com/social_amnesia)
- [Official Subreddit](http://reddit.com/r/socialamnesia)

## Related software

- [Shreddit](https://github.com/x89/Shreddit) - a python program to delete reddit posts/submissions.
- [Reddit Overwrite](https://greasyfork.org/en/scripts/10380-reddit-overwrite) - a greasey fork program to overwrite reddit comments.
- [Reddit Secure Delete](https://userscripts-mirror.org/scripts/show/166415) - a userscript program to delete reddit comments.
- [Nuke Reddit History](https://www.reddit.com/r/NukeRedditHistory/) - a web extension to erase reddit history.
- [Twitter Archive Eraser](https://github.com/martani/Twitter-Archive-Eraser) - tweet deletion tool
