from app.pages import (
    home_page,
)

from app.layouts import (
    base_layout,
)


ROUTES = [
    {
        'path': '/',
        'component': home_page,
        'label': 'Home',
        'layout': base_layout,
    }
]