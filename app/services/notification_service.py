def send_otp(contact: str, method: str, otp: int):
    """
    Sends OTP based on user-selected method.
    method: 'email' or 'mobile'
    """

    if method == "email":
        send_otp_email(contact, otp)

    elif method == "mobile":
        send_otp_mobile(contact, otp)

    else:
        raise ValueError("Invalid OTP method")


def send_otp_email(email: str, otp: int):
    """
    Dummy email OTP sender.
    Replace with real email service later.
    """
    print(f"[EMAIL OTP] OTP {otp} sent to email: {email}")


def send_otp_mobile(mobile: str, otp: int):
    """
    Dummy SMS OTP sender.
    Replace with real SMS service later.
    """
    print(f"[SMS OTP] OTP {otp} sent to mobile: {mobile}")
