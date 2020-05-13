/* eslint-disable @typescript-eslint/camelcase */
/* eslint-disable no-param-reassign */
import store from "@/store/index";
import constants from "@/store/constants";

const gatherAndSetItems = ({
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
    user_id: store.state[constants.TWITTER_USER_ID],
    // can only do 200 per request, so we need to continually make requests until we run out of items
    count: 200
  };
  if (maxId) {
    data.max_id = String(maxId);
  }
  store.state[constants.TWITTER_USER_CLIENT].get(apiRoute, data).then(items => {
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

    gatherAndSetItems({ maxId: oldestItem, apiRoute, itemArray, oldestItem });
  });
};

const helpers = {
  gatherAndSetItems
};

export default helpers;
