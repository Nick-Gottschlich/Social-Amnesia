# Socal-Scrubber
Cleans out the old gunk from your social media profiles!

This is in very early versions, but the eventual goal is to create a user-friendly app that will allow one click and scheduled cleaning of social media accounts. What does "cleaning" mean? On a site like twitter, this could be removing old tweets, retweets, and likes. On a site like reddit, this could be deleting submissions and comments. This readme will contain a list of what sites are usable and what features are available on each one.

### How to build and run
Build the executable by running `python3 setup.py build`. This will create a folder called `build`, inside you can a folder with some crazy name, and in that you should see a 'main' executable. Run that executable to start the program.

## Reddit
* Can delete comments and submissions.
* Can keep a time range of comments and submissions (in hours)
* Can keep comments or submissions that are above a certain amount of upvotes.
