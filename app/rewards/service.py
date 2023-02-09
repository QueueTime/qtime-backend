import random

from app.firebase import firestore_db, REFERRAL_CODES_COLLECTION


def create_unique_referral_code() -> str:
    """
    Create a unique 6 character referral code.

    :return: A unique 6 character referral code.
    """
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = _generate_unique_code(CHARS, 6)
    while _referral_code_exists(code):
        code = _generate_unique_code(CHARS, 6)
    return code


def save_referral_code(code: str):
    """
    Add a new referral code to the referral codes collection

    :param code: The referral code to add
    """
    firestore_db.collection(REFERRAL_CODES_COLLECTION).document(code).set({})
    # TODO: add property to each referral code so that they can be traced back to original user


def delete_referral_code(code: str):
    """
    Deletes a referral code from the referral codes collection

    :param code: The referral code to delete
    """
    firestore_db.collection(REFERRAL_CODES_COLLECTION).document(code).delete()


def _generate_unique_code(CHARS: str, length: int) -> str:
    """
    Generate a unique code from a set of characters.

    :param CHARS: String with the characters to generate the code from.
    :param length: The length of the code to generate.
    :return: A unique code of given length.
    """
    return "".join(random.choices(CHARS, k=length))


def _referral_code_exists(code: str) -> bool:
    """
    Check if a referral code exists in the database.

    :param code: The referral code to check.
    :return: True if the referral code exists, False otherwise.
    """

    return (
        firestore_db.collection(REFERRAL_CODES_COLLECTION).document(code).get().exists
    )
