from enum import Enum, IntFlag, auto, unique



class PaymentType(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    PAYPAL = "PAYPAL"

class Provider(IntFlag):
    GOOGLE = auto()
    SC = auto()

@unique
class AuthMethod(Enum):
    SC = "SC"
    GOOGLE = "GOOGLE"


class Hardcode(Enum):
    EMAIL_SUBJECT='SC Side Project Email Validation'
    EMAIL_Content="""
    <html>
    <body>
    <h1>Hi {user}, Welcome to SC Side Project</h1>
    <p>This is a validating email.</p>
    <p>Please click the below link within 5 min to complete your registration.</p>
    <a href='{validate_registration_url}'>{validate_registration_url}</a>
    </body>
    </html>
    """
@unique
class RedisKeys(Enum):
    EMAIL_TOKEN = 'EMAIL_TOKEN'
    USER_CART = 'cart:{user_email}'
    PRODUCT_ID_SET = 'PRODUCT_ID_SET'
    PRODUCT_CACHE = 'PRODUCT_CACHE'

@unique
class RedisFields(Enum):
    PRODUCT_NAME = 'PRODUCT_NAME'
    PRODUST_AVAIL = 'PRODUST_AVAIL'

@unique
class ErrorCode(Enum):
    SC001='SC001'
    SC002='SC002'
    SC003='SC003'
    SC004='SC004'
    SC005='SC005'
    SC006='SC006'
    SC007='SC007'
    SC008='SC008'
    SC009='SC009'
    SC010='SC010'
    SC011='SC011'
    SC012='SC012'
    SC013='SC013'
    SC014='SC014'