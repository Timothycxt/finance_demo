from App.apis.corp_info import corp_info
from App.apis.corp_news import corp_news
from App.apis.economic_news import economic_new
from App.apis.indu_news import indu_news


def init_view(app):
    app.register_blueprint(corp_info)
    app.register_blueprint(corp_news)
    app.register_blueprint(economic_new)
    app.register_blueprint(indu_news)