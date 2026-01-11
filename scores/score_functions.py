def calc_max_score(diff, SCORE_FILES):
    """
    Calculates the highest score for a given difficulty

    Args:
        diff (str): The current difficulty
        SCORE_FILES (dict): A dictionary mapping difficulty to file name

    Returns:
        max_score (int): The highest score for that difficulty
    """
    max_score = 0
    with open(SCORE_FILES[diff], 'r') as file:
        for line in file:
            max_score = max(max_score, int(line.strip()))
    return max_score