def calculate_rating(reviews):
    """Calculate the average rating from a list of reviews."""
    if not reviews:
        return 0
    total_rating = sum(review.rating for review in reviews)
    return total_rating / len(reviews)
