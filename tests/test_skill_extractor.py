from services.skill_extractor import extract_skills


def test_skill_extraction():

    text = """
    I have experience with Python, Machine Learning,
    Deep Learning, NLP, TensorFlow and AWS.
    """

    skills = extract_skills(text)

    assert isinstance(skills, (list, set))


def test_python_is_detected():

    text = """
    Python developer with experience in machine learning.
    """

    skills = extract_skills(text)

    skills = [skill.lower() for skill in skills]

    assert "python" in skills 