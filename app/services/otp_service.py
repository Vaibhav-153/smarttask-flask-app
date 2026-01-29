import random
import time
from flask import session


# -------------------------
# GENERATE OTP
# -------------------------
def generate_otp() -> int:
    """
    Generates a 6-digit OTP.
    """
    return random.randint(100000, 999999)


# -------------------------
# STORE OTP
# -------------------------
def store_otp(otp: int, expiry_seconds: int = 300):
    """
    Stores OTP in session with expiry.
    """
    session["otp"] = otp
    session["otp_expiry"] = time.time() + expiry_seconds


# -------------------------
# VERIFY OTP
# -------------------------
def verify_otp(user_otp: int) -> bool:
    """
    Verifies OTP and checks expiry.
    """
    stored_otp = session.get("otp")
    expiry_time = session.get("otp_expiry")

    if not stored_otp or not expiry_time:
        return False

    if time.time() > expiry_time:
        clear_otp()
        return False

    if int(user_otp) != int(stored_otp):
        return False

    clear_otp()
    return True


# -------------------------
# CLEAR OTP
# -------------------------
def clear_otp():
    """
    Clears OTP from session.
    """
    session.pop("otp", None)
    session.pop("otp_expiry", None)
