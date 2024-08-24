from app.router import ROUTES
import solara



def get_all_routes():
    routes = []
    for route in ROUTES:
        routes.append(solara.Route(**route))
    return routes

routes = get_all_routes()