<template>
  <div class="aboutContainer">
    <div class="aboutIntro">
      <img class="logo" src="./About/SaLogoWhiteTransparent.png" />
      <h1 class="sectionTopPadding">Social Amnesia</h1>
      <h4>
        Forget the past. Social Amnesia makes sure your social media accounts
        only show your posts from recent history, not from "that phase" 5 years
        ago.
      </h4>
      <h5>
        Click on the Social Media links above to log in and get started.
      </h5>
    </div>
    <div class="sectionTopPadding">
      <h3>🚨 API Limit Warning 🚨</h3>
      <h5>
        <div>
          Due to limitations set by twitter and reddit, Social Amnesia is only
          able to index:
        </div>
        <div>
          <img class="aboutSMLogo" src="./About/TwitterLogo.png" />
          3200 tweets and 3200 favorites
        </div>
        <div>
          <img class="aboutSMLogo" src="./About/RedditLogo.png" />
          1000 comments and 1000 posts
        </div>
      </h5>
    </div>
    <div class="authorInfoContainer">
      <h3>
        Created by Nick Gottschlich
      </h3>
      <h5>
        <img class="aboutSMLogo" src="./About/TwitterLogo.png" />
        Follow me on twitter
        <a
          href="https://twitter.com/NickGottschlich"
          target="_blank"
          @click.prevent="
            openExternalBrowser('https://twitter.com/NickGottschlich')
          "
          >@NickGottschlich</a
        >
        to get updates on future Social Amnesia development.
      </h5>
      <h5>
        <img class="aboutSMLogo" src="./About/GitHubLogo.png" />
        View the source code for Social Amnesia on the
        <a
          href="https://github.com/Nick-Gottschlich/Social-Amnesia"
          target="_blank"
          @click.prevent="
            openExternalBrowser(
              'https://github.com/Nick-Gottschlich/Social-Amnesia'
            )
          "
          >official GitHub repo</a
        >
      </h5>
      <h5>
        Want to support the continued development of Social Amnesia? Any amount
        helps! Thank you!! 😁
      </h5>
      <div class="aboutPaymentLinks">
        <div class="aboutPaymentIndvLink">
          <h5>
            <div>Send bitcoin to</div>
            <div>36Bq7F2JZdYEWLyB8jPWB1XuLCBCCkLvHn</div>
          </h5>
          <img src="./About/btcQR.png" class="QR" />
        </div>
        <div class="aboutPaymentIndvLink">
          <h5>
            Venmo me
            <a
              href="https://venmo.com/code?user_id=1345298144165889018"
              target="_blank"
              @click.prevent="
                openExternalBrowser(
                  'https://venmo.com/code?user_id=1345298144165889018'
                )
              "
              >@Nicholas-Gottschlich</a
            >
          </h5>
          <img src="./About/VenmoQR.png" class="QR" />
        </div>
        <div class="aboutPaymentIndvLink">
          <h5>
            PayPal me
            <a
              href="https://www.paypal.me/nickpgott"
              target="_blank"
              @click.prevent="
                openExternalBrowser('https://www.paypal.me/nickpgott')
              "
              >@nickpgott</a
            >
          </h5>
          <img src="./About/PaypalQR.jpeg" class="QR" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import remote from "electron";

@Component
export default class About extends Vue {
  openExternalBrowser(link) {
    remote.shell.openExternal(link);
  }
}
</script>

<style lang="scss">
.aboutContainer {
  padding-bottom: 20px;
}

.aboutIntro {
  padding-left: 200px;
  padding-right: 200px;
}

.aboutSMLogo {
  height: 28px;
}

.logo {
  border: 1px solid #606060;
  background-color: #606060;
  height: 100px;
}

.aboutPaymentLinks {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  padding-left: 30px;
  padding-right: 30px;
}

.aboutPaymentIndvLink {
  padding-right: 50px;
}

.QR {
  height: 200px;
}

.authorInfoContainer {
  padding-top: 20px;
}

.sectionTopPadding {
  padding-top: 20px;
}
</style>
