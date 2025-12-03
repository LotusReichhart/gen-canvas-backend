from typing import Dict

from src.core.domain.service.mail_service import MailService

from ..external_service.mail_transporter import MailTransporter


class MailServiceImpl(MailService):
    def __init__(self, transporter: MailTransporter):
        self._transporter = transporter

    async def send_mail(self, to: str, subject: str, html: str) -> bool:
        return await self._transporter.send(to=to, subject=subject, html=html)

    def build_otp_template(self, otp: str, lang: str = "en") -> Dict[str, str]:
        if lang == "vi":
            content = {
                "subject": "Mã xác thực OTP của bạn",
                "title": "Mã xác thực OTP của bạn",
                "greeting": "Người dùng thân mến,",
                "intro": "Dưới đây là mã OTP của bạn. Vui lòng không chia sẻ mã này với bất kỳ ai:",
                "validity": "Mã OTP này chỉ có hiệu lực trong 5 phút.",
                "note": "Đây là email tự động, vui lòng không trả lời.",
                "closing": "Trân trọng,",
                "team": "Gen Canvas"
            }
        else:
            content = {
                "subject": "Your OTP Verification Code",
                "title": "Your OTP Verification Code",
                "greeting": "Dear user,",
                "intro": "Below is your OTP code. Please do not share this code with anyone:",
                "validity": "This OTP code is valid for 5 minutes.",
                "note": "This is an automated email, please do not reply.",
                "closing": "Regards,",
                "team": "Gen Canvas Team"
            }

        html = f"""
                   <div style="width:90%; background-color:#f0f2f3; padding:20px; border-radius:15px; font-family:Arial,sans-serif; color:#252f3d;">
                       <div style="max-width:400px; margin:0 auto; background-color:#ffffff; border-radius:10px; padding:25px; box-shadow:0 4px 8px rgba(0,0,0,0.05);">
                           <h2 style="font-size:18px; color:#333; margin-bottom:20px;">{content['title']}</h2>

                           <p style="margin-bottom:15px; font-size:14px;">{content['greeting']}</p>
                           <p style="margin-bottom:15px; font-size:14px;">{content['intro']}</p>

                           <div style="color:#1d4ed8; font-size:20px; font-weight:bold; letter-spacing:2px; margin-bottom:20px; text-align:center;">
                               {otp}
                           </div>

                           <p style="font-size:13px; color:#555; margin-bottom:10px;">
                               {content['validity']}
                           </p>
                           <p style="font-size:13px; color:#555; margin-bottom:10px;">
                               {content['note']}
                           </p>

                           <p style="font-size:12px; color:#555; margin-top:20px;">
                               {content['closing']}<br>
                               <strong>{content['team']}</strong>
                           </p>
                       </div>
                   </div>
                   """

        return {"subject": content['subject'], "html": html}
