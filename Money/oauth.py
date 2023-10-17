from google.oauth2 import service_account

# Ruta al archivo JSON de las credenciales del cliente OAuth 2.0
CREDENTIALS_FILE = 'C:\\Users\\Asdrual Lezama\\Downloads\\Educacionl_website\\Educacionl_website\\hotel_website\\client_secret_711545168062-uvq9opsk6jol216rhsikbnt3r6rg86jf.apps.googleusercontent.com.json'


def get_authenticated_service():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
    )
    return build('youtube', 'v3', credentials=credentials)
