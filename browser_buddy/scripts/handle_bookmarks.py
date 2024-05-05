from bookmark import BookmarkItem


edge_bookmark_path = r'C:\Users\YinChan\AppData\Local\Microsoft\Edge\User Data\Default\Bookmarks'

bookmark_item_list = BookmarkItem.parse_bookmark_data(edge_bookmark_path)
