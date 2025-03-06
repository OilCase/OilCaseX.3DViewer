import os
from app.api.oilcase_x import OilCaseXApi
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('OILCASEX_URL')
# url = 'https://x.oil-case.online'

api = OilCaseXApi(url)
token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6ImRiZTkyYzU1LWUwNjYtNGZlOS04NTQ1LTA0NzE0ODEyYzhjMiIsInJvbGUiOiJDQVBUQUlOIiwiVGVhbUlkIjoiOCIsIm5iZiI6MTc0MTA4MDQxNiwiZXhwIjoxNzcyNjE2NDE2LCJpYXQiOjE3NDEwODA0MTZ9.bgQdjxJh0u95kAWE7Rc4JuRtpobNP0YA8YyZ45cxJyjoJgf6Gxqx_wqeY87rqG0-EH6eWRqDlSWbHxSPh6x03Q'

r = api.upload_files(token, 'Api/V1/Info/HDM/UploadVtpVtu', [('vtp', '825984.vtp'), ('vtu', '825984.vtu')])
print(r)