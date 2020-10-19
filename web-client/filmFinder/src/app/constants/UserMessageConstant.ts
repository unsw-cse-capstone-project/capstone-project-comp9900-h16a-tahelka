export class UserMessageConstant {
  public static get WISHLIST_ADDED(): string { return 'Added to wishlist'; }
  public static get WISHLIST_REMOVED(): string { return 'Removed from wishlist'; }
  public static get WATCH_LIST_ADDED(): string { return 'Added to watchlist'; }
  public static get WATCHLIST_REMOVED(): string { return 'Removed from watchlist'; }
  public static get REVIEW_ADDED(): string { return 'Added review'; }
  public static get REVIEW_ADD_UNSUCCESSFUL(): string { return 'Could not add review, review is already present or try again!'; }
  public static get WISHLIST_ADD_UNSUCCESSFUL(): string { return 'Could not add to wishlist, movie is already present or try again!'; }
  public static get WISHLIST_REMOVE_UNSUCCESSFUL(): string { return 'Could not remove from wishlist, movie is not present or try again!'; }
  public static get WATCHLIST_REMOVE_UNSUCCESSFUL(): string {
    return 'Could not remove from watchlist, movie is not present or try again!';
  }
  public static get DISMISS(): string { return 'Dismiss'; }

}
