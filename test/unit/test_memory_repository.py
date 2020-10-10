from datetime import date, datetime
from typing import List

import pytest

from movie.domain.model import User, Movie, Actor,Genre, Review, make_review
from movie.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_article_count(in_memory_repo):
    number_of_articles = in_memory_repo.get_number_of_movies()

    # Check that the query returned 5 Articles.
    assert number_of_articles == 5


def test_repository_can_add_article(in_memory_repo):
    movie = Movie(name='The Great Wall',year1=2016,rank=6)
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(6) is movie


def test_repository_can_retrieve_article(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Article has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Article is commented as expected.
    review_one = [review for review in movie.reviews if review.review_text == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    review_two = [review for review in movie.reviews if review.review_text == 'Yeah Freddie, bad news'][0]

    assert review_one.user.user_name == 'fmercury'
    assert review_two.user.user_name == "thorke"

    # Check that the Article is tagged as expected.
    assert movie.is_genre(Genre('Action'))
    assert movie.is_genre(Genre('Adventure'))
    assert movie.is_genre(Genre('Sci-Fi'))
    assert movie.is_acted_by(Actor('Chris Pratt'))
    assert movie.is_acted_by(Actor('Vin Diesel'))
    assert movie.is_acted_by(Actor('Bradley Cooper'))
    assert movie.is_acted_by(Actor('Zoe Saldana'))




def test_repository_does_not_retrieve_a_non_existent_article(in_memory_repo):
    movie = in_memory_repo.get_movie(101)
    assert movie is None


# def test_repository_can_retrieve_articles_by_date(in_memory_repo):
#     articles = in_memory_repo.get_articles_by_date(date(2020, 3, 1))
#
#     # Check that the query returned 3 Articles.
#     assert len(articles) == 3
#
#
# def test_repository_does_not_retrieve_an_article_when_there_are_no_articles_for_a_given_date(in_memory_repo):
#     articles = in_memory_repo.get_articles_by_date(date(2020, 3, 8))
#     assert len(articles) == 0
#
#
def test_repository_can_retrieve_tags(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 10

    genre_one = [genre for genre in genres if genre.genre_name == 'Action'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'Adventure'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'Sci-Fi'][0]


    assert genre_one.number_of_genre_movie == 2
    assert genre_two.number_of_genre_movie == 3
    assert genre_three.number_of_genre_movie == 2


#
# def test_repository_can_get_first_article(in_memory_repo):
#     article = in_memory_repo.get_first_article()
#     assert article.title == 'Coronavirus: First case of virus in New Zealand'
#
#
# def test_repository_can_get_last_article(in_memory_repo):
#     article = in_memory_repo.get_last_article()
#     assert article.title == 'Coronavirus: Death confirmed as six more test positive in NSW'
#
#
def test_repository_can_get_articles_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([2, 5])

    assert len(movies) == 2
    assert movies[0].title == 'Prometheus'
    assert movies[1].title == "Suicide Squad"



def test_repository_does_not_retrieve_article_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([2, 9])

    assert len(movies) == 1
    assert movies[0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([0, 9])

    assert len(movies) == 0


def test_repository_returns_article_ids_for_existing_tag(in_memory_repo):
    movie_ranks = in_memory_repo.get_movie_ranks_for_genre('Action')

    assert movie_ranks == [1,5]


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    movie_ranks = in_memory_repo.get_movie_ranks_for_genre('Loving')

    assert len(movie_ranks) == 0

#
# def test_repository_returns_date_of_previous_article(in_memory_repo):
#     article = in_memory_repo.get_article(6)
#     previous_date = in_memory_repo.get_date_of_previous_article(article)
#
#     assert previous_date.isoformat() == '2020-03-01'
#
#
# def test_repository_returns_none_when_there_are_no_previous_articles(in_memory_repo):
#     article = in_memory_repo.get_article(1)
#     previous_date = in_memory_repo.get_date_of_previous_article(article)
#
#     assert previous_date is None
#
#
# def test_repository_returns_date_of_next_article(in_memory_repo):
#     article = in_memory_repo.get_article(3)
#     next_date = in_memory_repo.get_date_of_next_article(article)
#
#     assert next_date.isoformat() == '2020-03-05'
#
#
# def test_repository_returns_none_when_there_are_no_subsequent_articles(in_memory_repo):
#     article = in_memory_repo.get_article(6)
#     next_date = in_memory_repo.get_date_of_next_article(article)
#
#     assert next_date is None
#
#
def test_repository_can_add_a_tag(in_memory_repo):
    genre = Genre('Loving')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = make_review("Trump's onto it!", user, movie,4)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "Trump's onto it!", 5)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = Review(user,movie,"Trump's onto it!",5)

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 2



