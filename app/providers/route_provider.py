from routes.api import api_router, yggdrasil_router


def boot(app):
    # 注册api路由[routes/api.py]
    app.include_router(api_router)
    app.include_router(yggdrasil_router)
    # 打印路由
    if app.debug:
        for route in app.routes:
            print({'path': route.path, 'name': route.name, 'methods': route.methods})
