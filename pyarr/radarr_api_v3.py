# -*- coding: utf-8 -*-
from datetime import datetime
from .request_api import RequestAPI


class RadarrAPIv3(RequestAPI):
    def __init__(
        self,
        host_url: str,
        api_key: str,
    ):
        """Constructor requires Host-URL and API-KEY

        Args:
            host_url (str): Host url to radarr.
            api_key: API key from Radarr. You can find this
        """
        super().__init__(host_url, api_key)

    # Movies
    def get_movie(self, tmdbid=None):
        """get_movie returns all movies in collection.

        Args:
            Optional - tmdbid - TMDb id of the movie to get
        Returns:
            json response

        """
        if tmdbid:
            path = f"/api/v3/movie?tmdbId={int(tmdbid)}"
            print(path)
        else:
            path = "/api/v3/movie"
        res = self.request_get(path)
        return res

    def lookup_movie(self, term):
        """Searches for movie

        Args:
            Requried - term (uses tmdb for search results)
        Returns:
            json response

        """
        term = str(term)
        term = term.replace(" ", "%20")
        path = f"/api/v3/movie/lookup?term={term}"
        res = self.request_get(path)
        return res

    def get_root(self):
        """Returns the Root Folder"""
        path = "/api/v3/rootfolder"
        res = self.request_get(path)
        return res

    # quality
    def get_quality_profiles(self):
        """Query Radarr for quality profiles"""
        path = "/api/v3/qualityProfile"
        res = self.request_get(path)
        return res

    def construct_movie_json(
        self, dbId, qualityProfileId, rootDir, monitored=True, searchForMovie=True
    ):
        """Searches for movie on tmdb and returns Movie json to add

        Args:
            Required - dbID, <imdb or tmdb id>
            Required - qualityProfileId (int)
            Required - rootDir (string)
            Optional - monitored (boolean)
            Optional - searchForMovie (boolean)

        Return:
            JsonArray

        """
        s_dict = self.lookup_movie(dbId)
        print(s_dict)

        if not s_dict:
            raise Exception("Movie Doesn't Exist")

        movie_json = {
            "title": s_dict[0]["title"],
            "path": rootDir + s_dict[0]["title"],
            "qualityProfileId": qualityProfileId,
            "year": s_dict[0]["year"],
            "tmdbId": s_dict[0]["tmdbId"],
            "images": s_dict[0]["images"],
            "titleSlug": s_dict[0]["titleSlug"],
            "monitored": monitored,
            "addOptions": {"searchForMovie": searchForMovie},
        }
        return movie_json

    # POST Movie
    def add_movie(
        self, dbId, qualityProfileId, rootDir=None, monitored=True, searchForMovie=True
    ):
        """addMovie adds a new movie to collection

        Args:
            Required - dbid tmdb id
            Required - qualityProfileId (int)
            Required - rootDir (string)
        Returns:
            json response

        """
        if not rootDir:
            rootDir = self.get_root()[0]["path"]

        term = f"tmdb:{str(dbId)}"

        movie_json = self.construct_movie_json(
            term, qualityProfileId, rootDir, monitored, searchForMovie
        )

        path = "/api/v3/movie"
        res = self.request_post(path, data=movie_json)
        return res

    # TODO: PUT Movie
    def update_movie(self, data):
        """Update an existing movie.

        Args:
            data (dictionary containing an object obtained by get_movie())
        Returns:
            json response
        """

        path = "/api/movie"
        res = self.request_put(path, data)
        return res

    # DELETE Movie
    def del_movie(self, movieId, delFiles=False, addExclusion=False):
        """Delete a single movie by database id
        Args:
            Required - movieId (int)
            Optional - delFiles (bool)
            Optional - addExclusion (bool)
        Returns:
            json response

        """
        # File deletion does not work
        data = {"deleteFiles": delFiles, "addExclusion": addExclusion}
        path = f"/api/v3/movie/{movieId}"
        res = self.request_del(path, data)
        return res

    # TODO: PUT Movie Editor
    # TODO: DELETE Movie Editor
    # TODO: POST Movie import

    # Movie Files
    # TODO: GET movieFiles
    def get_movie_file(self, movieId):
        """Returns movie files"""

        path = f"/api/v3/moviefile/{movieId}"
        res = self.request_get(path)
        return res

    # TODO: DELETE Movie Files
    def del_movie_file(self, movieId):
        """Allows for deletion of a moviefile by its database id.
        Args:
            Required - movieId (int)
        Returns:
            json response

        """
        path = f"/api/v3/movie/{movieId}"
        res = self.request_del(path)
        return res

    # history
    # TODO: GET history
    def get_history(self, page=1, pageSize=20, sortKey='date', sortDirection='descending'):
        """Return a json object list of items in your history

        Args:
            Required - page (int) - Default: 1
            Required - pageSize (int) - Default: 20
            Required - sortKey (string) - Default: date
            Required - sortDir (string) - Default: descending
        Returns:
            json response
        """
        path = f"/api/v3/history?page={page}&pageSize={pageSize}&sortDirection={sortDirection}&sortKey={sortKey}"
        res = self.request_get(path)
        return res

    # TODO: GET History Movies
    def get_history_movie(self, movieId, eventType=None):
        """Return a json object list of items in your history

        Args:
            Required - movieId (int) (Database id of movie)
            Optional - eventType (int) (History event type to retrieve)
        Returns:
            json response
        """
        if not eventType:
            path = f"/api/v3/history/movie?movieId={movieId}"
        else:
            path = f"/api/v3/history/movie?movieId={movieId}&eventType={eventType}"
        res = self.request_get(path)
        return res

    # blacklist
    # TODO: GET blacklist
    # TODO: DELETE blacklist
    # TODO: GET blacklist movie
    # TODO: DELETE Blacklist Bulk

    # queue
    # GET
    def get_queue(self, page=1, pageSize=20, sortKey='timeLeft', sortDirection='ascending',includeUnknownMovieItems='true'):
        """Return a json object list of items in the queue"""
        path = f"/api/v3/queue?page={page}&pageSize={pageSize}&sortDirection={sortDirection}&sortKey={sortKey}&includeUnknownMovieItems={includeUnknownMovieItems}"

        res = self.request_get(path)
        return res

    # indexer
    # TODO: GET indexer
    # TODO: GET Indexer by ID
    # TODO: PUT Indexer by id
    # TODO: DELETE Indexer by id

    # Download client

    # Import Lists

    # Notification

    # Tag

    # diskspace
    def get_disk_space(self):
        """Query Radarr for disk usage information

            Location: System > Status

        Args:
            None
        Returns:
            json response

        """
        path = "/api/v3/diskspace"
        res = self.request_get(path)
        return res

    # Settings

    # metadata

    # system
    def get_system_status(self):
        """Find out information such as OS, version, paths used, etc"""
        path = "/api/v3/system/status"
        res = self.request_get(path)
        return res

    # health
    def get_health(self):
        """Query radarr for health information"""
        path = "/api/v3/health"
        res = self.request_get(path)
        return res

    # command
    def post_command(self, **kwargs):
        """Performs any of the predetermined Radarr command routines.

        Kwargs:
            Required - name (string).

            Options available:
                - ApplicationUpdate - Trigger an update of Radarr
                - Backup - Trigger a backup routine
                - CheckHealth - Trigger a system health check
                - ClearBlacklist - Triggers the removal of all blacklisted movies
                - CleanUpRecycleBin - Trigger a recycle bin cleanup check
                - DeleteLogFiles - Triggers the removal of all Info/Debug/Trace log files
                - DeleteUpdateLogFiles - Triggers the removal of all Update log files
                - DownloadedMoviesScan - Triggers the scan of downloaded movies
                - MissingMoviesSearch - Triggers a search of all missing movies
                - RefreshMonitoredDownloads - Triggers the scan of monitored downloads
                - RefreshMovie - Trigger a refresh / scan of library
                    - movieIds:int[] - a list of ids (comma separated) for movies to refresh

            See https://radarr.video/docs/api/#/Command/post-command
        Returns:
        json response

        """
        path = "/api/v3/command"

        data = kwargs
        res = self.request_post(path, data)
        return res

    # update
    def get_update(self):
        """Returns a list of recent updates to Radarr

        Location: System > Updates
        """
        path = "/api/v3/update"
        res = self.request_get(path)
        return res

    # calendar
    def get_calendar(self, unmonitored='true', start_date=None, end_date=None):
        """Get a list of movies based on calendar parameters.
        If start and end are not provided, retrieves movies airing today and tomorrow.

         args:
            Required - unmonitored (bool)
            Optional -
                - start_date (datetime ISO 8601):
                - end_date (datetime ISO 8601):

         Returns:
             json response

        """

        data = {"unmonitored": unmonitored}

        if start_date and end_date:
            if isinstance(start_date, datetime):
                startDate = start_date.strftime("%Y-%m-%d")

            if isinstance(end_date, datetime):
                endDate = end_date.strftime("%Y-%m-%d")
            path = f"/api/v3/calendar?unmonitored={unmonitored}&start_date={startDate}&end_date={endDate}"
        else:
            path = "/api/v3/calendar"
        res = self.request_get(path)
        return res

    # custom filters

    # remote path mapping
