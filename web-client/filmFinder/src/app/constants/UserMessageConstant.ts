export class UserMessageConstant {
  public static get SUBSCRIBED_USER(): string { return 'Subscribed to user'; }
  public static get SUBSCRIBED_USER_UNSUCCESSFUL(): string {
    return 'Could not subscribed to user, either already subscribed or try again!';
  }
  public static get UNSUBSCRIBED_USER(): string { return 'Unsubscribed to user'; }
  public static get UNSUBSCRIBED_USER_UNSUCCESSFUL(): string { return 'Could not unsubscribed to user, either already unsubscribed or try again!'; }
  public static get WISHLIST_ADDED(): string { return 'Added to wishlist'; }
  public static get BLOCKED_USER_SUCCESSFUL(): string { return 'User has been blocked'; }
  public static get BLOCKED_USER_UNSUCCESSFUL(): string { return 'User block was not successful, try again!'; }
  public static get WISHLIST_REMOVED(): string { return 'Removed from wishlist'; }
  public static get WATCH_LIST_ADDED(): string { return 'Added to watchlist'; }
  public static get WATCH_LIST_ADD_UNSUCCESSFUL(): string { return 'Add to watchlist was not successful, already added or try again!'; }
  public static get WATCHLIST_REMOVED(): string { return 'Removed from watchlist'; }
  public static get WATCHLIST_REMOVED_UNSUCCESSFUL(): string { return 'Removed from watchlist unsuccessful, not present in watchlist or try again!'; }
  public static get REVIEW_ADDED(): string { return 'Added review'; }
  public static get REVIEW_ADD_UNSUCCESSFUL(): string { return 'Could not add review, review is already present or try again!'; }
  public static get WISHLIST_ADD_UNSUCCESSFUL(): string { return 'Could not add to wishlist, movie is already present or try again!'; }
  public static get WISHLIST_REMOVE_UNSUCCESSFUL(): string { return 'Could not remove from wishlist, movie is not present or try again!'; }
  public static get WISHLIST_IMPORT_SUCCESSFUL(): string { return 'Wishlist import successful.'; }
  public static get WISHLIST_IMPORT_UNSUCCESSFUL(): string { return 'Wishlist import unsuccessful, already imported or try again!'; }
  public static get WATCHLIST_REMOVE_UNSUCCESSFUL(): string {
    return 'Could not remove from watchlist, movie is not present or try again!';
  }
  public static get DISMISS(): string { return 'Dismiss'; }

}
