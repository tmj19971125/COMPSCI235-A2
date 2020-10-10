from datetime import date, datetime
from typing import List, Iterable



class User:
    def __init__(self, username, password):
        self.__user_name = username.strip()
        self.__password = password
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0



    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies



    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @property
    def user_name(self):
        return self.__user_name

    def __repr__(self):
        return '<User ' + str(self.__user_name) +' '+str(self.__password)+'>'

    def __eq__(self, other):
        if not isinstance(other,User):
            return False
        return self.__user_name == other.user_name

    def __lt__(self, other):
        return self.__user_name < other.user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self,value):
        self.__watched_movies.append(value)
        self.__time_spent_watching_movies_minutes += value.runtime_minutes


    def add_review(self, value):
        self.__reviews.append(value)
    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self.__reviews)

    def add_comment(self, comment: 'Review'):
        self.__reviews.append(comment)


class Review:
    def __init__(self, user, movie, text, rating):
        self.__movie = movie
        self.__review_text = text.strip()
        if (rating <= 0) or (rating > 10):
            self.__rating = None
        else:
            self.__rating = rating

        self.__timestamp = datetime.today()
        self.__user = user

    @property
    def movie(self):
        return self.__movie

    @property
    def user(self) -> User:
        return self.__user

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return '<Movie ' + self.__movie.title + ', ' + str(self.__timestamp) + '>'

    def __eq__(self, other):
        if not isinstance(other,Review):
            return False
        return (self.__movie == other.movie) and (self.__review_text == other.review_text) and (self.__rating \
                                                                                                == other.rating) and (
                           self.__timestamp == other.timestamp)


class Movie:
    def __init__(self, name, year1,rank):


        if type(name) == str and name != '':
            self.__title = name.strip()
        else:
            self.__title = None

        if type(year1) == int and year1 >= 1900:
            self.__year = year1
        else:
            self.__year = None
        self.__rank = rank
        self.__description = None
        self.__director = []
        self.__reviews = []
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None


    def __repr__(self):
        return '<Movie ' + self.__title + ', ' + str(self.__year) + '>'

    def __eq__(self, other):
        if not isinstance(other,Movie):
            return False
        return (self.__class__ == other.__class__ and self.__title == other.__title and self.__year == other.__year)


    def __lt__(self, other):
        if self.__title == other.title:
            return self.__year < other.__year
        else:
            return self.__title < other.__title

    def __hash__(self):
        return hash((self.__title , self.__year))

    @property
    def rank(self):
        return self.__rank

    @property
    def title(self):
        return self.__title

    @property
    def year(self):
        return self.__year

    @property
    def description(self):
        return self.__description

    @property
    def director(self) -> Iterable['Director']:
        return iter(self.__director)
    @property
    def actors(self) -> Iterable['Actor']:
        return iter(self.__actors)


    @property
    def number_of_actors(self) -> int:
        return len(self.__actors)

    def is_acted_by(self, actor: 'Actor'):
        return actor in self.__actors

    def acted(self) -> bool:
        return len(self.__actors) > 0

    @property
    def genres(self) -> Iterable['Genre']:
        return iter(self.__genres)

    @property
    def first_genre(self):
        return self.__genres[0]

    @property
    def number_of_genres(self) -> int:
        return len(self.__genres)


    def is_genre(self,genre: 'Genre'):
        return genre in self.__genres

    def genred(self) -> bool:
        return len(self.__genres) > 0

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self.__reviews)

    @property
    def number_of_comments(self) -> int:
        return len(self.__reviews)

    @description.setter
    def description(self, value):
        if type(value) == str and value != '':
            self.__description = value.strip()

    @runtime_minutes.setter
    def runtime_minutes(self, value):
        if type(value) == int and value >= 0:
            self.__runtime_minutes = value
        else:
            raise ValueError

    def add_actor(self, actor):
        self.__actors.append(actor)

    def add_director(self, director):
        self.__director.append(director)

    def remove_actor(self, actor):
        for i in range(len(self.__actors)):
            if self.__actors[i] == actor:
                self.__actors.pop(i)

    def add_genre(self, genre):
        self.__genres.append(genre)

    def remove_genres(self, genre):
        for i in range(len(self.__genres)):
            if self.__genres[i] == genre:
                self.__genres.pop(i)

    def add_review(self, value):
        self.__reviews.append(value)







class Director:
    def __init__(self, value):
        if value == '' or type(value) != str:
            self.__director_full_name = None
        else:
            self.__director_full_name = value.strip()
        self.__movie_list: List[Movie] = []

    def add_movie(self, movie:Movie):
        self.__movie_list.append(movie)

    @property
    def director_full_name(self):
        return self.__director_full_name
    @property
    def directed_movie(self) -> Iterable[Movie]:
        return iter(self.__movie_list)
    @property
    def number_of_actor_movie(self) -> int:
        return len(self.__movie_list)
    def is_applied_to(self, movie:Movie) -> bool:
        return movie in self.__movie_list

    def __repr__(self):
        return '<Director ' + str(self.__director_full_name) + '>'

    def __eq__(self, other):
        if not isinstance(other,Director):
            return False
        if self.__director_full_name == other.__director_full_name:
            return self.__director_full_name == other.__director_full_name
        else:
            return False

    def __lt__(self, other):
        return self.__director_full_name < other.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:
    def __init__(self, value):
        if value == '' or type(value) != str:
            self.__genre_name = None
        else:
            self.__genre_name = value.strip()
        self.__movie_list:List[Movie] = []

    def __repr__(self):
        return '<Genre ' + str(self.__genre_name) + '>'

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @property
    def genre_movie(self) -> Iterable[Movie]:
        return iter(self.__movie_list)

    @property
    def number_of_genre_movie(self) -> int:
        return len(self.__movie_list)

    def is_applied_to(self, movie:Movie) -> bool:
        return movie in self.__movie_list
    def add_movie(self, movie:Movie):
        self.__movie_list.append(movie)

    def __eq__(self, other):
        if not isinstance(other,Genre):
            return False
        if self.__genre_name == other.__genre_name:
            return self.__genre_name == other.__genre_name
        else:
            return False

    def __lt__(self, other):
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        return hash(self.__genre_name)


class Actor:

    def __init__(self, value):
        self.__colleague = []
        if value == '' or type(value) != str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = value.strip()
        self.__movie_list: List[Movie] = []

    def add_movie(self, movie:Movie):
        self.__movie_list.append(movie)

    def __repr__(self):
        return '<Actor ' + str(self.__actor_full_name) + '>'

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def actor_movie(self) -> Iterable[Movie]:
        return iter(self.__movie_list)

    @property
    def number_of_actor_movie(self) -> int:
        return len(self.__movie_list)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self.__movie_list

    def __eq__(self, other):
        if not isinstance(other,Actor):
            return False
        if self.__actor_full_name == other.actor_full_name:
            return self.__actor_full_name == other.__actor_full_name
        else:
            return False

    def __lt__(self, other):
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, other):
        if isinstance(other, Actor):
            self.__colleague.append(other)
            other.__colleague.append(self)

    def check_if_this_actor_worked_with(self, other):
        if isinstance(other, Actor):
            for x in self.__colleague:
                if x == other:
                    return x == other

            return False






class WatchList:
    pass
class ModelException(Exception):
    pass

def make_review(review_text: str, user: User, movie: Movie,review_num: int):
    review = Review(user, movie, review_text,review_num)
    user.add_review(review)
    movie.add_review(review)
    return review


def make_genre_association(movie:Movie, genre:Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Tag {movie.title} already applied to Movie "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)


def make_actor_association(movie:Movie,actor:Actor):
    if actor.is_applied_to(movie):
        raise ModelException(f'Tag {movie.title} already applied to Movie "{movie.title}"')

    movie.add_actor(actor)
    actor.add_movie(movie)


def make_director_association(movie:Movie,director:Director):
    if director.is_applied_to(movie):
        raise ModelException(f'Tag {movie.title} already applied to Movie "{movie.title}"')

    movie.add_director(director)
    director.add_movie(movie)

