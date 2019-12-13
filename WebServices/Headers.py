
# when you click the back button in the browser it will load requests from cache
# unless you set no cahce headers on that specefic endpoint
# important mostly for GET method endpoints

NO_CACHE_HEADERS = {}

NO_CACHE_HEADERS["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
NO_CACHE_HEADERS["Expires"] = 0
NO_CACHE_HEADERS["Pragma"] = "no-cache"