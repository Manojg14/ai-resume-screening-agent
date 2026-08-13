
from services.scoring import calculate_final_score


def test_final_score_returns_valid_value():

    score = calculate_final_score(
        similarity_score=80,
        skill_score=90,
        experience_score=100,
        education_score=100
    )

    assert isinstance(score, (int, float))
    assert 0 <= score <= 100


def test_final_score_calculation():

    score = calculate_final_score(
        similarity_score=100,
        skill_score=100,
        experience_score=100,
        education_score=100
    )

    assert score == 100


def test_zero_scores():

    score = calculate_final_score(
        similarity_score=0,
        skill_score=0,
        experience_score=0,
        education_score=0
    )

    assert score == 0