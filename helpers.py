# helpers for backend

import os

from flask import redirect, session
from sqlalchemy import inspect
from functools import wraps


def login_required(f):
    """Decorates routes to require login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def get_dict_array(obj):
    res = []
    for o in obj:
        res.append(get_dict(o))
    return res
