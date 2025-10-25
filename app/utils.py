from app.schemas.posts import BasePost


def deduplicate_posts(posts_list: list[BasePost]) -> list[BasePost]:
    """Deduplicate posts based on their UID."""
    seen_uids = set()
    unique_posts = []
    
    for post in posts_list:
        if post.uid not in seen_uids:
            seen_uids.add(post.uid)
            unique_posts.append(post)
    
    return unique_posts