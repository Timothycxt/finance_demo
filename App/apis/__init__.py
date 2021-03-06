from App.apis.corp_info import corp_info
from App.apis.corp_news import corp_news
from App.apis.corp_neo4j import corp_neo4j
from App.apis.economic_news import economic_new
from App.apis.indu_news import indu_news
from App.apis.corp_score import corp_score
from App.apis.authen import authen


def init_view(app):
    app.register_blueprint(corp_info)
    app.register_blueprint(corp_news)
    app.register_blueprint(corp_neo4j)
    app.register_blueprint(economic_new)
    app.register_blueprint(indu_news)
    app.register_blueprint(corp_score)
    app.register_blueprint(authen)
