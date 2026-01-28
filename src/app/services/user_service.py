class DuplicateEmailError(Exception):
    pass

def normalize_email(email: str) -> str:
    return email.strip().lower()

def ensure_email_unique(email: str, repo) -> str:
    email_n = normalize_email(email)
    if repo.exists_by_email(email_n):
        raise DuplicateEmailError(email_n)
    return email_n
