from services.similarity import calculate_similarity


def test_similarity_returns_percentage():
    jd = """
    Python developer with experience in machine learning,
    NLP, pandas and scikit-learn.
    """

    resume = """
    Python developer with experience in machine learning,
    NLP, pandas and scikit-learn.
    """

    score = calculate_similarity(jd, resume)

    assert isinstance(score, (int, float))
    assert 0 <= score <= 100


def test_similar_text_has_higher_score():
    jd = """
    Python machine learning developer with NLP experience.
    """

    matching_resume = """
    Python machine learning developer with NLP experience.
    """

    unrelated_resume = """
    Graphic designer with experience in Photoshop,
    Illustrator and visual design.
    """

    matching_score = calculate_similarity(jd, matching_resume)
    unrelated_score = calculate_similarity(jd, unrelated_resume)

    assert matching_score > unrelated_score 