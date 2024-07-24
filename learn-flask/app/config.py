import secrets

class Config:
  SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db/flask'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = secrets.token_hex(32)
  JWT_ACCESS_TOKEN_EXPIRES = 15  # Access token expires in 15 minutes
  JWT_REFRESH_TOKEN_EXPIRES = 30  # Refresh token expires in 30 days