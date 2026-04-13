# ──────────────────────────────────────────────
# SECTION 1: Grade Calculator
# ──────────────────────────────────────────────

def calculate_letter_grade(score: float) -> str:
    """
    Convert a numeric score (0–100) to a letter grade.

    Boundaries (mutation targets):
        >= 90  → 'A'
        >= 80  → 'B'
        >= 70  → 'C'
        >= 60  → 'D'
        else   → 'F'
    """
    if score < 0 or score > 100:
        raise ValueError(f"Score must be between 0 and 100, got {score}")

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def calculate_gpa(score: float) -> float:
    """
    Convert a numeric score to a GPA value on a 4.0 scale.

    Boundaries (mutation targets):
        >= 90  → 4.0
        >= 80  → 3.0
        >= 70  → 2.0
        >= 60  → 1.0
        else   → 0.0
    """
    if score < 0 or score > 100:
        raise ValueError(f"Score must be between 0 and 100, got {score}")

    if score >= 90:
        return 4.0
    elif score >= 80:
        return 3.0
    elif score >= 70:
        return 2.0
    elif score >= 60:
        return 1.0
    else:
        return 0.0


def calculate_weighted_average(scores: list, weights: list) -> float:
    """
    Calculate a weighted average of scores.

    Args:
        scores:  List of numeric scores.
        weights: List of weights (must sum to 1.0).

    Raises:
        ValueError: If inputs are mismatched or weights don't sum to 1.
    """
    if not scores or not weights:
        raise ValueError("Scores and weights cannot be empty")
    if len(scores) != len(weights):
        raise ValueError("Scores and weights must have the same length")
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
    if any(s < 0 or s > 100 for s in scores):
        raise ValueError("All scores must be between 0 and 100")
    if any(w < 0 for w in weights):
        raise ValueError("All weights must be non-negative")

    return sum(s * w for s, w in zip(scores, weights))


def is_passing(score: float, passing_threshold: float = 60.0) -> bool:
    """
    Determine whether a score meets the passing threshold.

    Mutation target: the >= operator (vs >) and the default threshold value.
    """
    if score < 0 or score > 100:
        raise ValueError(f"Score must be between 0 and 100, got {score}")
    return score >= passing_threshold


def calculate_grade_points(letter_grade: str, credit_hours: int) -> float:
    """
    Calculate grade points earned for a single course.

    Args:
        letter_grade: One of 'A', 'B', 'C', 'D', 'F'.
        credit_hours: Positive integer number of credit hours.

    Mutation targets: grade-point mapping values, credit_hours validation.
    """
    grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

    if letter_grade not in grade_points:
        raise ValueError(f"Invalid letter grade: '{letter_grade}'")
    if credit_hours <= 0:
        raise ValueError("Credit hours must be a positive integer")

    return grade_points[letter_grade] * credit_hours


def calculate_cumulative_gpa(courses: list) -> float:
    """
    Calculate cumulative GPA from a list of (letter_grade, credit_hours) tuples.

    Returns 0.0 when the course list is empty.
    """
    if not courses:
        return 0.0

    total_points = 0.0
    total_hours = 0

    for letter_grade, credit_hours in courses:
        total_points += calculate_grade_points(letter_grade, credit_hours)
        total_hours += credit_hours

    return total_points / total_hours