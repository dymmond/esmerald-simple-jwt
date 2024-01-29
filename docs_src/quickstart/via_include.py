from esmerald import Esmerald, Include

app = Esmerald(
    routes=[
        Include(path="/auth", namespace="esmerald_simple_jwt.urls"),
    ]
)
