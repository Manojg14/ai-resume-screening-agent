from services.scoring import calculate_final_score


def test_final_score_returns_valid_result():

    jd_text = """
    We are looking for a Python AI Engineer with 2 years
    of experience in Python, Machine Learning, NLP,
    TensorFlow and AWS.

    Bachelor's degree in Engineering.
    """

    resume_text = """
    Python AI Engineer with 3 years of experience.

    Skills:
    Python
    Machine Learning
    NLP
    TensorFlow
    AWS

    Education:
    Bachelor's degree in Engineering.
    """

    result = calculate_final_score(
        jd_text,
        resume_text
    )

    assert isinstance(result, dict)

    assert "final_score" in result
    assert "similarity_score" in result
    assert "skill_score" in result
    assert "experience_score" in result
    assert "education_score" in result
    assert "matched_skills" in result
    assert "missing_skills" in result
    assert "recommendation" in result


def test_final_score_is_valid_percentage():

    jd_text = """
    Python developer with machine learning experience.
    """

    resume_text = """
    Python developer with machine learning experience.
    """

    result = calculate_final_score(
        jd_text,
        resume_text
    )

    assert 0 <= result["final_score"] <= 100
    assert 0 <= result["similarity_score"] <= 100
    assert 0 <= result["skill_score"] <= 100
    assert 0 <= result["experience_score"] <= 100
    assert 0 <= result["education_score"] <= 100


def test_matching_resume_has_skills():

    jd_text = """
    We need a Python developer with Machine Learning,
    NLP and TensorFlow skills.
    """

    resume_text = """
    I am a Python developer with experience in
    Machine Learning, NLP and TensorFlow.
    """

    result = calculate_final_score(
        jd_text,
        resume_text
    )

    assert len(result["matched_skills"]) > 0


def test_final_score_calculation():

    jd_text = """
    Python developer with Machine Learning experience.
    """

    resume_text = """
    Python developer with Machine Learning experience.
    """

    result = calculate_final_score(
        jd_text,
        resume_text
    )

    expected_score = round(
        result["similarity_score"] * 0.50
        + result["skill_score"] * 0.30
        + result["experience_score"] * 0.10
        + result["education_score"] * 0.10,
        2
    )

    assert result["final_score"] == expected_score