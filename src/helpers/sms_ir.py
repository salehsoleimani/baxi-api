from sms_ir import SmsIr
from ..config.config import settings

sms_helper = SmsIr(
    settings.SMS_KEY,
    settings.SMS_LINE,
)
