# coding: utf-8
"""
:mod:`boardgamegeek.objects.games` - Classes for storing game data
==================================================================

.. module:: boardgamegeek.objects.games
   :platform: Unix, Windows
   :synopsis: classes for storing games data

.. moduleauthor:: Cosmin Luță <q4break@gmail.com>

"""
from __future__ import unicode_literals

import datetime
from copy import copy

from .things import Thing
from ..exceptions import BGGError
from ..utils import fix_url, DictObject, fix_unsigned_negative


class BoardGameRank(Thing):
    """
    Object containing information about the rank of a board game
    """
    @property
    def type(self):
        """
        :return: type of the rank (e.g. "subtype", "family", etc.)
        :rtype: str
        """
        return self._data.get("type")

    @property
    def friendly_name(self):
        """
        :return: friendly name of the rank
        :rtype: str
        """
        return self._data.get("friendlyname")

    @property
    def value(self):
        """
        :return: value of the rank
        :rtype: int
        """
        return self._data.get("value")

    @property
    def rating_bayes_average(self):
        """
        :return: bayes average
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("bayesaverage")

    def __repr__(self):
        return "BoardGameRank(id: {}, name: {}, value: {})".format(self.id, self.friendly_name, self.value)


class PollResultLanguageDependence(DictObject):
    """
    Stores poll results for the game's language dependence
    """
    def __init__(self, data):
        super(PollResultLanguageDependence, self).__init__(data)

    @property
    def level(self):
        """
        """
        return self._level

    @property
    def description(self):
        """

        :return: text description for this language dependence level
        """
        return self._description

    @property
    def votes(self):
        """
        :return: the number of votes in the "Best" category, for this number of players
        :rtype: int
        """
        return self._votes

    def _format(self, log):
        log.info("> {} (level {}): votes: {}".format(self._description,
                                                     self._level,
                                                     self._votes))


class PollResultPlayerNumber(DictObject):
    """
    Stores poll results for the number of players
    """
    def __init__(self, data):
        super(PollResultPlayerNumber, self).__init__(data)

    @property
    def player_number(self):
        """
        """
        return self._count

    @property
    def votes_for_best(self):
        """
        :return: the number of votes in the "Best" category, for this number of players
        :rtype: int
        """
        return self._best

    @property
    def votes_for_recommended(self):
        """
        :return: the number of votes in the "Recommended" category, for this number of players
        :rtype: int
        """
        return self._recommended

    @property
    def votes_for_not_recommended(self):
        """
        :return: the number of votes in the "Not Recommended" category, for this number of players
        """
        return self._not_recommended

    def _format(self, log):
        log.info("> {} players: votes: {} for best, {} for recommended, {} for not recommended".format(self._count,
                                                                                                       self._best,
                                                                                                       self._recommended,
                                                                                                       self._not_recommended))


class PollResultPlayerAge(DictObject):
    """
    Stores poll results for player age
    """
    def __init__(self, data):
        super(PollResultPlayerAge, self).__init__(data)

    @property
    def player_age(self):
        """
        """
        return self._age

    @property
    def votes(self):
        """
        :return: the number of votes for this age
        :rtype: int
        """
        return self._votes

    def _format(self, log):
        log.info("> {} years: votes: {}".format(self._age, self._votes))


class BoardGameStats(DictObject):
    """
    Statistics about a board game
    """
    def __init__(self, data):
        self._ranks = []

        for rank in data.get("ranks", []):
            if rank.get("name") == "boardgame":
                try:
                    self._bgg_rank = int(rank["value"])
                except (KeyError, TypeError):
                    self._bgg_rank = None
            self._ranks.append(BoardGameRank(rank))

        super(BoardGameStats, self).__init__(data)

    @property
    def bgg_rank(self):
        """
        :return: BGG rank
        :rtype: int
        """
        return self._bgg_rank

    @property
    def ranks(self):
        """
        :return: list of ranks for this game
        :rtype: list of :py:class:`boardgamegeek.objects.games.BoardGameRank`
        """
        return self._ranks

    @property
    def users_rated(self):
        """
        :return: how many users rated the game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("usersrated")

    @property
    def rating_average(self):
        """
        :return: average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("average")

    @property
    def rating_bayes_average(self):
        """
        :return: bayes average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("bayesaverage")

    @property
    def rating_stddev(self):
        """
        :return: standard deviation
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("stddev")

    @property
    def rating_median(self):
        """
        :return: median value of all ratings
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("median")

    @property
    def users_owned(self):
        """
        :return: number of users owning this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("owned")

    @property
    def users_trading(self):
        """
        :return: number of users trading this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("trading")

    @property
    def users_wanting(self):
        """
        :return: number of users wanting this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("wanting")

    @property
    def users_wishing(self):
        """
        :return: number of users wishing for this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("wishing")

    @property
    def users_commented(self):
        """
        :return: number of user comments
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("numcomments")

    @property
    def rating_num_weights(self):
        """
        :return:
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("numweights")

    @property
    def rating_average_weight(self):
        """
        :return: average weight
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("averageweight")


class BoardGameComment(DictObject):
    """
    Object containing a comment on BGG
    """
    @property
    def commenter(self):
        """
        :return: name of the user making the comment
        :rtype: str
        """
        return self._data["username"]

    @property
    def comment(self):
        """
        :return: the comment
        :rtype: str
        """
        return self._data["comment"]

    @property
    def rating(self):
        """
        :return: user's rating
        :rtype: str
        :return: "n/a" if user didn't rate the game with this comment
        """
        return self._data["rating"]

    def _format(self, log):
        log.info(u"comment by {} (rating: {}): {}".format(self.commenter, self.rating, self.comment))

    def __repr__(self):
        return "BoardGameComment(user: {}): {}".format(self.commenter, self.comment)


class BoardGameVideo(Thing):
    """
    Object containing information about a board game video
    """
    def __init__(self, data):
        kw = copy(data)

        if "post_date" in kw:
            date = kw["post_date"]
            if type(date) != datetime.datetime:
                try:
                    kw["post_date"] = datetime.datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S")
                except:
                    kw["post_date"] = None

        kw["uploader_id"] = int(kw["uploader_id"])

        super(BoardGameVideo, self).__init__(kw)

    def __repr__(self):
        return "BoardGameVideo (link: {})".format(self.link)

    def _format(self, log):
        log.info("video id          : {}".format(self.id))
        log.info("video title       : {}".format(self.name))
        log.info("video category    : {}".format(self.category))
        log.info("video link        : {}".format(self.link))
        log.info("video language    : {}".format(self.language))
        log.info("video uploader    : {}".format(self.uploader))
        log.info("video uploader id : {}".format(self.uploader_id))
        log.info("video posted at   : {}".format(self.post_date))

    @property
    def category(self):
        """
        :return: the category of this video
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("category")

    @property
    def link(self):
        """
        :return: the link to this video
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("link")

    @property
    def language(self):
        """
        :return: the language of this video
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("language")

    @property
    def uploader(self):
        """
        :return: the name of the user which uploaded this video
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("uploader")

    @property
    def uploader_id(self):
        """
        :return: id of the uploader
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("uploader_id")

    @property
    def post_date(self):
        """
        :return: date when this video was uploaded
        :rtype: datetime.datetime
        :return: ``None`` if n/a
        """
        return self._data.get("post_date")


class BoardGameVersion(Thing):
    """
    Object containing information about a board game version
    """
    def __init__(self, data):
        kw = copy(data)

        for to_fix in ["thumbnail", "image"]:
            if to_fix in kw:
                kw[to_fix] = fix_url(kw[to_fix])

        super(BoardGameVersion, self).__init__(kw)

    def __repr__(self):
        return "BoardGameVersion (id: {})".format(self.id)

    def _format(self, log):
        log.info("version id           : {}".format(self.id))
        log.info("version name         : {}".format(self.name))
        log.info("version language     : {}".format(self.language))
        log.info("version publisher    : {}".format(self.publisher))
        log.info("version artist       : {}".format(self.artist))
        log.info("version product code : {}".format(self.product_code))
        log.info("W x L x D            : {} x {} x {}".format(self.width, self.length, self.depth))
        log.info("weight               : {}".format(self.weight))
        log.info("year                 : {}".format(self.year))

    @property
    def artist(self):
        """
        :return: artist of this version
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("artist")

    @property
    def depth(self):
        """
        :return: depth of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("depth")

    @property
    def length(self):
        """
        :return: length of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("length")

    @property
    def language(self):
        """
        :return: language of this version
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("language")

    @property
    def name(self):
        """
        :return: name of this version
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("name")

    @property
    def product_code(self):
        """

        :return: product code of this version
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("product_code")

    @property
    def publisher(self):
        """

        :return: publisher of this version
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._data.get("publisher")

    @property
    def weight(self):
        """
        :return: weight of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("weight")

    @property
    def width(self):
        """
        :return: width of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("width")

    @property
    def year(self):
        """
        :return: publishing year
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("yearpublished")


class BaseGame(Thing):

    def __init__(self, data):

        self._thumbnail = fix_url(data["thumbnail"]) if "thumbnail" in data else None
        self._image = fix_url(data["image"]) if "image" in data else None
        if "stats" not in data:
            raise BGGError("invalid data")

        self._stats = BoardGameStats(data["stats"])

        self._versions = []
        self._versions_set = set()

        try:
            self._year_published = fix_unsigned_negative(data["yearpublished"])
        except KeyError:
            self._year_published = None

        for version in data.get("versions", []):
            try:
                if version["id"] not in self._versions_set:
                    self._versions.append(BoardGameVersion(version))
                    self._versions_set.add(version["id"])
            except KeyError:
                raise BGGError("invalid version data")

        super(BaseGame, self).__init__(data)

    @property
    def thumbnail(self):
        """
        :return: thumbnail URL
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._thumbnail

    @property
    def image(self):
        """
        :return: image URL
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._image

    @property
    def year(self):
        """
        :return: publishing year
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._year_published

    @property
    def min_players(self):
        """
        :return: minimum number of players
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("minplayers")

    @property
    def max_players(self):
        """
        :return: maximum number of players
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("maxplayers")

    @property
    def min_playing_time(self):
        """
        :return: minimum playing time
        :return: ``None`` if n/a
        :rtype: int
        """
        return self._data.get("minplaytime")

    @property
    def max_playing_time(self):
        """
        :return: maximum playing time
        :return: ``None`` if n/a
        :rtype: int
        """
        return self._data.get("maxplaytime")

    @property
    def playing_time(self):
        """
        :return: playing time
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("playingtime")

    @property
    def users_rated(self):
        """
        :return: how many users rated the game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._stats.users_rated

    @property
    def rating_average(self):
        """
        :return: average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_average

    @property
    def rating_bayes_average(self):
        """
        :return: bayes average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_bayes_average

    @property
    def rating_stddev(self):
        """
        :return: standard deviation
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_stddev

    @property
    def rating_median(self):
        """
        :return:
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_median

    @property
    def ranks(self):
        """
        :return: rankings of this game
        :rtype: list of :py:class:`boardgamegeek.objects.games.BoardGameRank`
        :return: ``None`` if n/a
        """
        return self._stats.ranks

    @property
    def bgg_rank(self):
        """
        :return: The board game geek rank of this game
        """
        # TODO: document this
        return self._stats.bgg_rank


class CollectionBoardGame(BaseGame):
    """
    A boardgame retrieved from the collection information, which has less information than the one retrieved
    via the /thing api and which also contains some user-specific information.
    """

    def __init__(self, data):
        super(CollectionBoardGame, self).__init__(data)

    def __repr__(self):
        return "CollectionBoardGame (id: {})".format(self.id)

    def _format(self, log):
        log.info("boardgame id      : {}".format(self.id))
        log.info("boardgame name    : {}".format(self.name))
        log.info("number of plays   : {}".format(self.numplays))
        log.info("last modified     : {}".format(self.lastmodified))
        log.info("rating            : {}".format(self.rating))
        log.info("own               : {}".format(self.owned))
        log.info("preordered        : {}".format(self.preordered))
        log.info("previously owned  : {}".format(self.prev_owned))
        log.info("want              : {}".format(self.want))
        log.info("want to buy       : {}".format(self.want_to_buy))
        log.info("want to play      : {}".format(self.want_to_play))
        log.info("wishlist          : {}".format(self.wishlist))
        log.info("wishlist priority : {}".format(self.wishlist_priority))
        log.info("for trade         : {}".format(self.for_trade))
        for v in self._versions:
            v._format(log)

    @property
    def lastmodified(self):
        # TODO: deprecate this
        return self._data.get("lastmodified")

    @property
    def last_modified(self):
        """
        :return: last modified date
        :rtype: str
        """
        return self._data.get("lastmodified")

    @property
    def version(self):
        if len(self._versions):
            return self._versions[0]
        else:
            return None

    @property
    def numplays(self):
        """
        :return: number of plays
        :rtype: int
        """
        return self._data.get("numplays", 0)

    @property
    def rating(self):
        """
        :return: user's rating of the game
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("rating")

    @property
    def owned(self):
        """
        :return: game owned
        :rtype: bool
        """
        return bool(int(self._data.get("own", 0)))

    @property
    def preordered(self):
        """
        :return: game preordered
        :rtype: bool
        """
        return bool(int(self._data.get("preordered", 0)))

    @property
    def prev_owned(self):
        """
        :return: game previously owned
        :rtype: bool
        """
        return bool(int(self._data.get("prevowned", 0)))

    @property
    def want(self):
        """
        :return: game wanted
        :rtype: bool
        """
        return bool(int(self._data.get("want", 0)))

    @property
    def want_to_buy(self):
        """
        :return: want to buy
        :rtype: bool
        """
        return bool(int(self._data.get("wanttobuy", 0)))

    @property
    def want_to_play(self):
        """
        :return: want to play
        :rtype: bool
        """
        return bool(int(self._data.get("wanttoplay", 0)))

    @property
    def for_trade(self):
        """
        :return: game for trading
        :rtype: bool
        """
        return bool(int(self._data.get("fortrade", 0)))

    @property
    def wishlist(self):
        """
        :return: game on wishlist
        :rtype: bool
        """
        return bool(int(self._data.get("wishlist", 0)))

    @property
    def wishlist_priority(self):
        """
        :return: the priority in the whishlist for this game
        :rtype: int or None
        """
        try:
            return int(self._data.get("wishlistpriority"))
        except TypeError:
            # This occurs when the priority is not set
            return None


class BoardGame(BaseGame):
    """
    Object containing information about a board game
    """
    def __init__(self, data):

        self._expansions = []                      # list of Thing for the expansions
        self._expansions_set = set()               # set for making sure things are unique
        for exp in data.get("expansions", []):
            try:
                if exp["id"] not in self._expansions_set:
                    self._expansions_set.add(exp["id"])
                    self._expansions.append(Thing(exp))
            except KeyError:
                raise BGGError("invalid expansion data")

        self._expands = []                         # list of Thing which this item expands
        self._expands_set = set()                  # set for keeping things unique
        for exp in data.get("expands", []):        # for all the items this game expands, create a Thing
            try:
                if exp["id"] not in self._expands_set:
                    self._expands_set.add(exp["id"])
                    self._expands.append(Thing(exp))
            except KeyError:
                raise BGGError("invalid expanded game data")

        self._videos = []
        self._videos_ids = set()
        for video in data.get("videos", []):
            try:
                if video["id"] not in self._videos_ids:
                    self._videos.append(BoardGameVideo(video))
                    self._videos_ids.add(video["id"])
            except KeyError:
                raise BGGError("invalid video data")

        self._comments = []
        for comment in data.get("comments", []):
            self.add_comment(comment)

        self._poll_results_numplayers = []
        if "suggested_numplayers" in data:
            for count, result in data["suggested_numplayers"]["results"].items():
                suggestion_data = {
                    "_count": count,
                    "_best": result["best"],
                    "_recommended": result["recommended"],
                    "_not_recommended": result["not_recommended"],
                }
                self._poll_results_numplayers.append(PollResultPlayerNumber(suggestion_data))

        self._poll_results_playerage = []
        if "suggested_playerage" in data:
            for age, num_votes in data["suggested_playerage"]["results"].items():
                self._poll_results_playerage.append(PollResultPlayerAge({"_age": age,
                                                                         "_votes": num_votes}))

        self._poll_results_langdeps = []
        if "language_dependence" in data:
            for level, d in data["language_dependence"]["results"].items():
                self._poll_results_langdeps.append(PollResultLanguageDependence({"_level": level,
                                                                                 "_description": d["description"],
                                                                                 "_votes": d["num_votes"]}))

        super(BoardGame, self).__init__(data)

    def __repr__(self):
        return "BoardGame (id: {})".format(self.id)

    def add_comment(self, data):
        self._comments.append(BoardGameComment(data))

    def add_expanded_game(self, data):
        """
        Add a game expanded by this one

        :param dict data: expanded game's data
        :raises: :py:exc:`boardgamegeek.exceptions.BoardGameGeekError` if data is invalid
        """
        try:
            if data["id"] not in self._expands_set:
                self._data["expands"].append(data)
                self._expands_set.add(data["id"])
                self._expands.append(Thing(data))
        except KeyError:
            raise BGGError("invalid expanded game data")

    def add_expansion(self, data):
        """
        Add an expansion of this game

        :param dict data: expansion data
        :raises: :py:exc:`boardgamegeek.exceptions.BoardGameGeekError` if data is invalid
        """
        try:
            if data["id"] not in self._expansions_set:
                self._data["expansions"].append(data)
                self._expansions_set.add(data["id"])
                self._expansions.append(Thing(data))
        except KeyError:
            raise BGGError("invalid expansion data")

    def _format(self, log):
        log.info("boardgame id      : {}".format(self.id))
        log.info("boardgame name    : {}".format(self.name))
        log.info("boardgame rank    : {}".format(self.bgg_rank))
        if self.alternative_names:
            for i in self.alternative_names:
                log.info("alternative name  : {}".format(i))
        log.info("year published    : {}".format(self.year))
        log.info("minimum players   : {}".format(self.min_players))
        log.info("maximum players   : {}".format(self.max_players))
        log.info("playing time      : {}".format(self.playing_time))
        log.info("minimum age       : {}".format(self.min_age))
        log.info("thumbnail         : {}".format(self.thumbnail))
        log.info("image             : {}".format(self.image))
        log.info("is expansion      : {}".format(self.expansion))

        if self.expansions:
            log.info("expansions")
            for i in self.expansions:
                log.info("- {}".format(i.name))

        if self.expands:
            log.info("expands")
            for i in self.expands:
                log.info("- {}".format(i.name))

        if self.categories:
            log.info("categories")
            for i in self.categories:
                log.info("- {}".format(i))

        if self.families:
            log.info("families")
            for i in self.families:
                log.info("- {}".format(i))

        if self.mechanics:
            log.info("mechanics")
            for i in self.mechanics:
                log.info("- {}".format(i))

        if self.implementations:
            log.info("implementations")
            for i in self.implementations:
                log.info("- {}".format(i))

        if self.designers:
            log.info("designers")
            for i in self.designers:
                log.info("- {}".format(i))

        if self.artists:
            log.info("artistis")
            for i in self.artists:
                log.info("- {}".format(i))

        if self.publishers:
            log.info("publishers")
            for i in self.publishers:
                log.info("- {}".format(i))

        if self.videos:
            log.info("videos")
            for v in self.videos:
                v._format(log)
                log.info("--------")

        if self.versions:
            log.info("versions")
            for v in self.versions:
                v._format(log)
                log.info("--------")

        if self.player_number_votes:
            log.info("poll: player number results")
            for v in self.player_number_votes:
                v._format(log)
            log.info("--------")

        if self.player_age_votes:
            log.info("poll: player age results")
            for v in self.player_age_votes:
                v._format(log)
            log.info("--------")

        if self.language_dependence_votes:
            log.info("poll: language dependence results")
            for v in self.language_dependence_votes:
                v._format(log)
            log.info("--------")

        log.info("users rated game  : {}".format(self.users_rated))
        log.info("users avg rating  : {}".format(self.rating_average))
        log.info("users b-avg rating: {}".format(self.rating_bayes_average))
        log.info("users commented   : {}".format(self.users_commented))
        log.info("users owned       : {}".format(self.users_owned))
        log.info("users wanting     : {}".format(self.users_wanting))
        log.info("users wishing     : {}".format(self.users_wishing))
        log.info("users trading     : {}".format(self.users_trading))
        log.info("ranks             : {}".format(self.ranks))
        log.info("description       : {}".format(self.description))
        if self.comments:
            for c in self.comments:
                c._format(log)

    @property
    def alternative_names(self):
        """
        :return: alternative names
        :rtype: list of str
        """
        return self._data.get("alternative_names", [])

    @property
    def description(self):
        """
        :return: description
        :rtype: str
        """
        return self._data.get("description", "")

    @property
    def families(self):
        """
        :return: families
        :rtype: list of str
        """
        return self._data.get("families", [])

    @property
    def categories(self):
        """
        :return: categories
        :rtype: list of str
        """
        return self._data.get("categories", [])

    @property
    def comments(self):
        """
        :return: comments for this game
        :rtype: list of :py:class:`boardgamegeek.objects.games.BoardGameComment`
        """
        return self._comments

    @property
    def mechanics(self):
        """
        :return: mechanics
        :rtype: list of str
        """
        return self._data.get("mechanics", [])

    @property
    def expansions(self):
        """
        :return: expansions
        :rtype: list of :py:class:`boardgamegeek.objects.things.Thing`
        """
        return self._expansions

    @property
    def expands(self):
        """
        :return: games this item expands
        :rtype: list of :py:class:`boardgamegeek.objects.things.Thing`
        """
        return self._expands

    @property
    def implementations(self):
        """
        :return: implementations
        :rtype: list of str
        """
        return self._data.get("implementations", [])

    @property
    def designers(self):
        """
        :return: designers
        :rtype: list of str
        """
        return self._data.get("designers", [])

    @property
    def artists(self):
        """
        :return: artists
        :rtype: list of str
        """
        return self._data.get("artists", [])

    @property
    def publishers(self):
        """
        :return: publishers
        :rtype: list of str
        """
        return self._data.get("publishers", [])

    @property
    def expansion(self):
        """
        :return: True if this item is an expansion
        :rtype: bool
        """
        return self._data.get("expansion", False)

    @property
    def min_age(self):
        """
        :return: minimum recommended age
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("minage")

    @property
    def users_owned(self):
        """
        :return: number of users owning this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._stats.users_owned

    @property
    def users_trading(self):
        """
        :return: number of users trading this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._stats.users_trading

    @property
    def users_wanting(self):
        """
        :return: number of users wanting this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("wanting")

    @property
    def users_wishing(self):
        """
        :return: number of users wishing for this game
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("wishing")

    @property
    def users_commented(self):
        """
        :return: number of user comments
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._data.get("numcomments")

    @property
    def rating_num_weights(self):
        """
        :return:
        :rtype: int
        :return: ``None`` if n/a
        """
        return self._stats.rating_num_weights

    @property
    def rating_average_weight(self):
        """
        :return: average weight
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_average_weight

    @property
    def videos(self):
        """
        :return: videos of this game
        :rtype: list of :py:class:`boardgamegeek.objects.games.BoardGameVideo`
        """
        return self._videos

    @property
    def versions(self):
        """
        :return: versions of this game
        :rtype: list of :py:class:`boardgamegeek.objects.games.BoardGameVersion`
        """
        return self._versions

    @property
    def player_number_votes(self):
        """
        :return list of player number votes
        :rtype: list of :py:class:`boardgamegeek.games.PollResultPlayerNumber`
        """
        return self._poll_results_numplayers

    @property
    def player_age_votes(self):
        """
        :return list of player age suggestions, with votes
        :rtype: list of :py:class:`boardgamegeek.games.PollResultPlayerAge`
        """
        return self._poll_results_playerage

    @property
    def language_dependence_votes(self):
        """
        :return list of language dependence votes
        :rtype: list of :py:class:`boardgamegeek.games.PollResultPlayerAge`
        """
        return self._poll_results_langdeps
