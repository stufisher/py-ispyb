from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from ...globals import g
from .token import decode_token, set_token_data

security = HTTPBearer()


def verify_jwt(token: str):
    try:
        return decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expired. Please log in again"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def JWTBearer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials:
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme."
            )
        decoded = verify_jwt(credentials.credentials)
        if not decoded:
            raise HTTPException(
                status_code=401, detail="Invalid token or expired token."
            )

        set_token_data(decoded)

        return credentials.credentials
    else:
        raise HTTPException(status_code=401, detail="No token provided.")


def permission_required(operator, permissions):
    """Make the route only accesible to users with the specified permissions.

    Args:
        operator (str): any or all
        permissions (str[]): permissions required
    """
    operator = operator.lower()
    if operator != "any" and operator != "all":
        raise Exception("operator must be 'any' or 'all'.")

    async def res():

        user_permissions: list[str] = g.permissions
        if user_permissions is None:
            user_permissions = []

        if (
            operator == "any"
            and (
                "all" in permissions
                or any(
                    permission in list(permissions)
                    for permission in list(user_permissions)
                )
            )
        ) or (
            operator == "all"
            and (
                all(
                    permission in list(permissions)
                    for permission in list(user_permissions)
                )
            )
        ):
            return user_permissions
        else:
            msg = (
                "User %s (permissions assigned: %s) has no appropriate permission (%s: %s) "
                % (
                    g.login,
                    str(user_permissions),
                    operator,
                    str(permissions),
                )
            )
            msg += " to execute method."
            raise HTTPException(status_code=401, detail=msg)

    return res
