import jwt
import config

print(config.SECRETKEY)
res = jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImlhdCI6MTYyMzE4MDkxOC43MDkyNjZ9.eyJzdWIiOjEzLCJuYW1lIjoicmVuYXRvIiwiaWF0IjoxNjIzMTgwOTE4LjcwOTI2Nn0.11EAGeOx3b7hk9pBIWV0HFUIk89DvrjQ0nu525slDyg", config.SECRETKEY, algorithms=['HS256'])
res = jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImlhdCI6MTYyMzA5NDQ4MS41MzgxMDR9.eyJzdWIiOjEzLCJuYW1lIjoicmVuYXRvIiwiaWF0IjoxNjIzMDk0NDgxLjUzODEwNH0.RJN65RMPfw_2R5kFpN6g3C67qj2CM95W8QgZ3K4lgXQ", config.SECRETKEY, algorithms=['HS256'])
print(config.SECRETKEY, res)