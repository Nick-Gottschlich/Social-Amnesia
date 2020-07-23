/* eslint-disable @typescript-eslint/camelcase */
/* eslint-disable no-param-reassign */
import store from "@/store/index";
import constants from "@/store/constants";
import redditAPI from "@/redditSecrets";
import axios, { AxiosResponse } from "axios";
// @ts-ignore
import qs from "qs";

const twitterGatherAndSetItems = ({
  maxId,
  apiRoute,
  itemArray,
  oldestItem
}: {
  maxId?: number;
  apiRoute: string;
  itemArray: { id: number }[];
  oldestItem?: number;
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

const makeRedditGetRequest = async (
  url: string,
  params?: any
): Promise<any> => {
  try {
    const { data }: AxiosResponse = await axios.get(url, {
      headers: {
        Authorization: `bearer ${
          store.state.reddit[constants.REDDIT_ACCESS_TOKEN]
        }`
      },
      params
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

const redditGatherAndSetItemsHelper = ({
  maxId,
  apiUrl,
  commentsOrPosts,
  itemArray
}: {
  maxId?: string;
  apiUrl: string;
  commentsOrPosts: string;
  itemArray: any;
}) => {
  const params = {
    limit: 100
  };
  if (maxId) {
    // @ts-ignore
    params.after = maxId;
  }

  makeRedditGetRequest(apiUrl, params).then(response => {
    const items = response.data.children;

    if (items.length === 0) {
      if (commentsOrPosts === "comments") {
        store.dispatch(constants.UPDATE_REDDIT_COMMENTS, itemArray);
      } else {
        store.dispatch(constants.UPDATE_REDDIT_POSTS, itemArray);
      }
      return;
    }

    itemArray = itemArray.concat(items);
    const oldestItem = itemArray.slice(-1)[0].data.name;

    redditGatherAndSetItemsHelper({
      maxId: oldestItem,
      apiUrl,
      commentsOrPosts,
      itemArray
    });
  });
};

const redditGatherAndSetItems = () => {
  redditGatherAndSetItemsHelper({
    apiUrl: `https://oauth.reddit.com/user/${
      store.state.reddit[constants.REDDIT_USER_NAME]
    }/comments`,
    commentsOrPosts: "comments",
    itemArray: []
  });

  redditGatherAndSetItemsHelper({
    apiUrl: `https://oauth.reddit.com/user/${
      store.state.reddit[constants.REDDIT_USER_NAME]
    }/submitted`,
    commentsOrPosts: "posts",
    itemArray: []
  });
};

let redditAccessTokenTimer: any;
let twitterContentTimer: any;

const stopRedditAccessTokenRefresh = () => {
  clearTimeout(redditAccessTokenTimer);
};

const stopTwitterContentRefresh = () => {
  clearTimeout(twitterContentTimer);
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
  //  we do it every 10 minutes because I don't trust reddit
  redditAccessTokenTimer = setTimeout(() => {
    refreshRedditAccessToken();
  }, 600000);
};

const refreshTwitterContent = () => {
  twitterGatherAndSetItems({
    apiRoute: "statuses/user_timeline",
    itemArray: []
  });
  twitterGatherAndSetItems({
    apiRoute: "favorites/list",
    itemArray: []
  });

  twitterContentTimer = setTimeout(() => {
    refreshTwitterContent();
  }, 600000);
};

// see https://stackoverflow.com/questions/4959975/generate-random-number-between-two-numbers-in-javascript
// and https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript
const generateRandomText = () => {
  const randomNumber = Math.floor(Math.random() * 200) + 1;

  return Array(randomNumber + 1)
    .join(`${Math.random().toString(36)}00000000000000000`.slice(2, 18))
    .slice(0, randomNumber);
};

const deleteTwitterItems = (
  items,
  itemString,
  whitelistedItems,
  skipConfirm
) => {
  const itemInSavedTimeRange = item => {
    const timeRangeObject = store.state.twitter[constants.TWITTER_TIME_RANGE];

    const hoursBackToSave =
      timeRangeObject.Hours +
      timeRangeObject.Days * 24 +
      timeRangeObject.Weeks * 168 +
      timeRangeObject.Years * 8766;
    const dateOfHoursBackToSave = new Date();
    dateOfHoursBackToSave.setHours(
      dateOfHoursBackToSave.getHours() - hoursBackToSave
    );

    return (
      new Date(item.created_at) > new Date(dateOfHoursBackToSave.toGMTString())
    );
  };

  const itemLowerThanScore = item => {
    if (
      item.favorite_count >=
      store.state.twitter[constants.TWITTER_FAVORITES_SCORE]
    ) {
      return false;
    }

    if (
      item.retweet_count >=
      store.state.twitter[constants.TWITTER_RETWEETS_SCORE]
    ) {
      return false;
    }

    return true;
  };

  if (
    window.confirm(
      `Are you sure you want to delete your ${itemString}? THIS ACTION IS PERMANENT!`
    ) ||
    skipConfirm
  ) {
    const promiseArray = [];

    const shouldDeleteItem = item => {
      const itemIsWhitelisted = whitelistedItems[`${itemString}-${item.id}`];

      const shouldDelete =
        !itemIsWhitelisted &&
        (!itemInSavedTimeRange(item) ||
          !store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED]) &&
        (itemString === "favorites" ||
          itemLowerThanScore(item) ||
          !store.state.twitter[constants.TWITTER_SCORE_ENABLED]);

      return shouldDelete;
    };

    const totalItemsLength = items.filter(item => {
      return shouldDeleteItem(item);
    }).length;

    store.dispatch(constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED);
    store.dispatch(
      constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS,
      totalItemsLength
    );

    items.forEach(item => {
      console.log("item", item);
      if (shouldDeleteItem(item)) {
        console.log("gonna delete item", item.id_str);
        promiseArray.push(
          store.state.twitter[constants.TWITTER_USER_CLIENT]
            .post(
              itemString === "twitter tweets"
                ? "statuses/destroy"
                : "favorites/destroy",
              {
                id: item.id_str
              }
            )
            .then(() => {
              store.commit(
                constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED
              );
            })
            .catch(error => {
              console.log(
                `Failed to delete item with error: ${JSON.stringify(error)}`
              );
            })
        );
      }
    });

    Promise.allSettled(promiseArray).then(() => {
      twitterGatherAndSetItems({
        apiRoute:
          itemString === "twitter tweets"
            ? constants.TWEETS_ROUTE
            : constants.FAVORITES_ROUTE,
        itemArray: []
      });

      setTimeout(() => {
        store.dispatch(constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS, 0);
      }, 2500);
    });
  }
};

const deleteRedditItems = (items, itemString, whitelistedItems) => {
  const redditItemInSavedTimeRange = item => {
    const timeRangeObject = store.state.reddit[constants.REDDIT_TIME_RANGE];

    const hoursBackToSave =
      timeRangeObject.Hours +
      timeRangeObject.Days * 24 +
      timeRangeObject.Weeks * 168 +
      timeRangeObject.Years * 8766;
    const dateOfHoursBackToSave = new Date();
    dateOfHoursBackToSave.setHours(
      dateOfHoursBackToSave.getHours() - hoursBackToSave
    );

    const convertedItemDate = new Date(
      new Date(item.data.created_utc * 1000).toGMTString()
    );
    const convertedDateRangeDate = new Date(
      dateOfHoursBackToSave.toGMTString()
    );
    return convertedItemDate > convertedDateRangeDate;
  };

  const redditItemLowerThanScore = item => {
    if (item.data.score >= store.state.reddit[constants.REDDIT_UPVOTES_SCORE]) {
      return false;
    }

    return true;
  };

  if (
    window.confirm(
      `Are you sure you want to delete your ${itemString}? THIS ACTION IS PERMANENT!`
    )
  ) {
    const promiseArray = [];

    const shouldDeleteItem = item => {
      const itemIsWhitelisted =
        whitelistedItems[`${itemString}-${item.data.name}`];

      const shouldDelete =
        !itemIsWhitelisted &&
        (!redditItemInSavedTimeRange(item) ||
          !store.state.reddit[constants.REDDIT_TIME_RANGE_ENABLED]) &&
        (redditItemLowerThanScore(item) ||
          !store.state.reddit[constants.REDDIT_SCORE_ENABLED]);

      return shouldDelete;
    };

    const totalItemsLength = items.filter(item => {
      return shouldDeleteItem(item);
    }).length;

    store.dispatch(constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED);
    store.dispatch(
      constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS,
      totalItemsLength
    );

    items.forEach(item => {
      if (shouldDeleteItem(item)) {
        promiseArray.push(
          makeRedditPostRequest("https://oauth.reddit.com/api/editusertext/", {
            thing_id: item.data.name,
            text: generateRandomText()
          })
            .then(() => {
              makeRedditPostRequest("https://oauth.reddit.com/api/del/", {
                id: item.data.name
              })
                .then(() => {
                  store.commit(
                    constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED
                  );
                })
                .catch(error => {
                  console.log(
                    `Failed to delete item with error: ${JSON.stringify(error)}`
                  );
                });
            })
            .catch(error => {
              console.log(
                `Failed to edit item with error: ${JSON.stringify(error)}`
              );
            })
        );
      }
    });

    Promise.allSettled(promiseArray).then(() => {
      redditGatherAndSetItems();

      setTimeout(() => {
        store.dispatch(constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS, 0);
      }, 2500);
    });
  }
};

const helpers = {
  twitterGatherAndSetItems,
  makeRedditGetRequest,
  makeRedditPostRequest,
  redditGatherAndSetItems,
  stopRedditAccessTokenRefresh,
  refreshRedditAccessToken,
  stopTwitterContentRefresh,
  refreshTwitterContent,
  generateRandomText,
  deleteTwitterItems,
  deleteRedditItems
};

export default helpers;
