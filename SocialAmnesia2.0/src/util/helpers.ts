/* eslint-disable @typescript-eslint/camelcase */
/* eslint-disable no-param-reassign */
import store from "@/store/index";
import constants from "@/store/constants";
import redditAPI from "@/redditSecrets";
import axios, { AxiosResponse } from "axios";
import qs from "qs";

const twitterGatherAndSetItems = ({
  maxId,
  apiRoute,
  itemArray,
  oldestItem
}: {
  maxId: number;
  apiRoute: string;
  itemArray: { id: number }[];
  oldestItem: number;
}) => {
  const data = {
    tweet_mode: "extended",
    user_id: store.state.twitter[constants.TWITTER_USER_ID],
    // can only do 200 per request, so we need to continually make requests until we run out of items
    count: 200
  };
  if (maxId) {
    // @ts-ignore
    data.max_id = String(maxId);
  }
  store.state.twitter[constants.TWITTER_USER_CLIENT]
    .get(apiRoute, data)
    .then((items: any) => {
      if (
        items.length === 0 ||
        (items.length === 1 && items[0].id === oldestItem)
      ) {
        if (apiRoute === constants.TWEETS_ROUTE) {
          store.dispatch(constants.UPDATE_USER_TWEETS, itemArray);
        }
        if (apiRoute === constants.FAVORITES_ROUTE) {
          store.dispatch(constants.UPDATE_USER_FAVORITES, itemArray);
        }
        return;
      }

      itemArray = itemArray.concat(items);
      oldestItem = itemArray.slice(-1)[0].id;

      twitterGatherAndSetItems({
        maxId: oldestItem,
        apiRoute,
        itemArray,
        oldestItem
      });
    });
};

const makeRedditGetRequest = async (url: string): Promise<any> => {
  try {
    const { data }: AxiosResponse = await axios.get(url, {
      headers: {
        Authorization: `bearer ${
          store.state.reddit[constants.REDDIT_ACCESS_TOKEN]
        }`
      }
    });
    return data;
  } catch (error) {
    console.error(`Error in reddit request ${url}`, error);
    return error;
  }
};

const makeRedditPostRequest = async (url: string, body: any): Promise<any> => {
  const options = {
    method: "POST",
    headers: {
      Authorization: `bearer ${
        store.state.reddit[constants.REDDIT_ACCESS_TOKEN]
      }`,
      "content-type": "application/x-www-form-urlencoded"
    },
    data: qs.stringify(body),
    url
  };

  try {
    // @ts-ignore
    const response: AxiosResponse = await axios(options);
    return response;
  } catch (error) {
    console.error(`Error in reddit request ${url}`, error);
    return error;
  }
};

const redditGatherAndSetItems = () => {
  makeRedditGetRequest(
    `https://oauth.reddit.com/user/${
      store.state.reddit[constants.REDDIT_USER_NAME]
    }/comments`
  ).then(commentsData => {
    store.dispatch(
      constants.UPDATE_REDDIT_COMMENTS,
      commentsData.data.children
    );
  });

  makeRedditGetRequest(
    `https://oauth.reddit.com/user/${
      store.state.reddit[constants.REDDIT_USER_NAME]
    }/submitted`
  ).then(submissionData => {
    store.dispatch(constants.UPDATE_REDDIT_POSTS, submissionData.data.children);
  });
};

let accessTokenTimer: any;

const stopRedditAccessTokenRefresh = () => {
  clearTimeout(accessTokenTimer);
};

const refreshRedditAccessToken = () => {
  axios
    .post(
      "https://www.reddit.com/api/v1/access_token",
      {},
      {
        params: {
          grant_type: "refresh_token",
          refresh_token: store.state.reddit[constants.REDDIT_REFRESH_TOKEN]
        },
        auth: {
          username: redditAPI.clientId,
          password: ""
        }
      }
    )
    .then(response => {
      if (response.data.access_token) {
        store.dispatch(
          constants.UPDATE_REDDIT_ACCESS_TOKEN,
          response.data.access_token
        );
      } else {
        throw new Error("No access token found!");
      }
    })
    .catch(error => {
      console.error(
        "Failed to get reddit access_token on app load with error:",
        error
      );
    });

  // refresh the items while we're at it
  redditGatherAndSetItems();

  // the reddit API requires you to get a new access token every hour
  //  we do it at 59 minutes because we real rebels here
  accessTokenTimer = setTimeout(() => {
    refreshRedditAccessToken();
  }, 3540000);
};

const helpers = {
  twitterGatherAndSetItems,
  makeRedditGetRequest,
  makeRedditPostRequest,
  redditGatherAndSetItems,
  stopRedditAccessTokenRefresh,
  refreshRedditAccessToken
};

export default helpers;
