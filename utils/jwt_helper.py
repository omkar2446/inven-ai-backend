from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


def generate_token(user):
    payload = user.to_dict()
    return create_access_token(identity=payload)


# decorator in routes can use @jwt_required()
