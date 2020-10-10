from datetime import date

from movie.domain.model import User, Movie, Actor, Genre, make_genre_association, make_actor_association, \
    ModelException, make_review

import pytest


@pytest.fixture()
def movie():
    return Movie('Guardians of the Galaxy',2014)


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('Action')

@pytest.fixture()
def actor():
    return Actor('Chris Pratt')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.title == 'Guardians of the Galaxy'
    assert movie.year == 2014
    assert movie.number_of_comments == 0
    assert movie.number_of_genres == 0
    assert movie.number_of_actors == 0

    assert repr(
        movie) == '<Movie Guardians of the Galaxy, 2014>'


def test_movie_less_than_operator():
    movie_1 = Movie('Guardians of the Galaxy',2014)

    movie_2 = Movie('Prometheus',2012)

    assert movie_1 < movie_2


def test_genre_construction(genre):
    assert genre.genre_name == 'Action'

    for movie in genre.genre_movie:
        assert False

    assert not genre.is_applied_to(Movie(None,None))

def test_actor_construction(actor):
    assert actor.actor_full_name == 'Chris Pratt'

    for movie in actor.actor_movie:
        assert False

    assert not actor.is_applied_to(Movie(None,None))


def test_make_review_establishes_relationships(movie, user):
    review_text = 'COVID-19 in the USA!'
    review = make_review(review_text,user,movie,8)


    # Check that the User object knows about the Comment.
    assert review in user.reviews

    # Check that the Comment knows about the User.
    assert review.user is user

    # Check that Article knows about the Comment.
    assert review in movie.review

    # Check that the Comment knows about the Article.
    assert review.movie is movie


def test_make_tag_associations(movie, genre,actor):
    make_genre_association(movie, genre)
    make_actor_association(movie, actor)

    # Check that the Article knows about the Tag.
    assert movie.genred()
    assert movie.is_genre(genre)

    assert movie.acted()
    assert movie.is_acted_by(actor)

    # check that the Tag knows about the Article.
    assert genre.is_applied_to(movie)
    assert movie in genre.genre_movie

    assert actor.is_applied_to(movie)
    assert movie in actor.actor_movie


def test_make_genre_associations_with_movie_already_genred(movie,genre):
    make_genre_association(movie,genre)

    with pytest.raises(ModelException):
        make_genre_association(movie,genre)


def test_make_actor_associations_with_movie_already_acted(movie,actor):
    make_actor_association(movie,actor)

    with pytest.raises(ModelException):
        make_actor_association(movie,actor)
