from App.apis.corp_info import corp_info
from App.apis.corp_news import corp_news


def init_view(app):
    app.register_blueprint(corp_info)
    app.register_blueprint(corp_news)
