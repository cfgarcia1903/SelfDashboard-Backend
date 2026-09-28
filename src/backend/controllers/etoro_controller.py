from flask import Blueprint, request
from flask.views import MethodView

from backend.utils.utils_auth import Authorization    
from backend.utils.utils_etoro import get_etoro_credentials 
from backend.services.etoro_service import EtoroService

etoro_api = Blueprint("etoro_api", __name__)


def _not_implemented():
    return {"error": "Endpoint not implemented"}, 501


class EtoroSummaryView(MethodView):
    def get(self):
        authorization = Authorization(request.headers.get("user_ID"), 
                                      request.headers.get("user_PIN"), 
                                      request.headers.get("X-APIKEY"))
        if authorization.validate():
            credentials = get_etoro_credentials(authorization.__dict__)
            account_summary = EtoroService.get_account_summary(credentials["public"], credentials["private"])
            return {"account_summary": account_summary.__dict__}, 200
        
        if not authorization.validate():
            return {"error": "Invalid authorization"}, 401

        return _not_implemented()




etoro_api.add_url_rule(
    "/account_summary",
    view_func=EtoroSummaryView.as_view("account_summary"),
)

