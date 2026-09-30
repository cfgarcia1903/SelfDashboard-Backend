from flask import Blueprint, request
from flask.views import MethodView

from backend.utils.utils_auth import Authorization    
from backend.utils.utils_etoro import get_etoro_credentials 
from backend.services.etoro_service import EtoroService

etoro_api = Blueprint("etoro_api", __name__)


def _not_implemented():
    return {"message": "Endpoint not implemented"}, 501


class EtoroSummaryView(MethodView):
    def get(self):
        try:
            authorization = Authorization(request.headers.get("user_ID"), 
                                        request.headers.get("user_PIN"), 
                                        request.headers.get("X-APIKEY"))
        except Exception as e:
            return {"message": "Invalid authorization"}, 401

        if authorization.validate():
            credentials = get_etoro_credentials(authorization.__dict__)
            account_summary = EtoroService.get_account_summary(credentials["public"], credentials["private"])
            return {"account_summary": account_summary.__dict__}, 200
        
        if not authorization.validate():
            return {"message": "Invalid authorization"}, 401


class EtoroDepositsRetrieveView(MethodView):
    def get(self):
        try:
            authorization = Authorization(request.headers.get("user_ID"), 
                                        request.headers.get("user_PIN"), 
                                        request.headers.get("X-APIKEY"))
        except Exception as e:
            return {"message": "Invalid authorization"}, 401

        if authorization.validate():
            
            deposits = EtoroService.get_deposits()
            if deposits is None:
                return {"message": "No deposits found"}, 404
            return {"deposits": deposits}, 200
        
        if not authorization.validate():
            return {"message": "Invalid authorization"}, 401


class EtoroDepositsEditView(MethodView):
    def put(self):
        try:
            authorization = Authorization(request.headers.get("user_ID"), 
                                        request.headers.get("user_PIN"), 
                                        request.headers.get("X-APIKEY"))
        except Exception as e:
            return {"message": "Invalid authorization"}, 401

        if authorization.validate():
            deposits = EtoroService.update_deposits(request.json.get("deposits", []))
            if deposits is None:
                return {"message": "No deposits found"}, 404
            return {"deposits": deposits}, 200
        
        if not authorization.validate():
            return {"message": "Invalid authorization"}, 401


class EtoroDepositsDeleteView(MethodView):
    def post(self):
        try:
            authorization = Authorization(request.headers.get("user_ID"), 
                                        request.headers.get("user_PIN"), 
                                        request.headers.get("X-APIKEY"))
        except Exception as e:
            return {"message": "Invalid authorization"}, 401

        if authorization.validate():
            deposits = EtoroService.delete_deposits(request.json.get("deposit_ids", []))
            if deposits is None:
                return {"message": "No deposits found"}, 404
            return {"deposits": deposits}, 200
        
        if not authorization.validate():
            return {"message": "Invalid authorization"}, 401


etoro_api.add_url_rule("/etoro/summary", view_func=EtoroSummaryView.as_view("etoro_summary"))
etoro_api.add_url_rule("/etoro/deposits", view_func=EtoroDepositsRetrieveView.as_view("etoro_deposits_retrieve"))
etoro_api.add_url_rule("/etoro/deposits/edit", view_func=EtoroDepositsEditView.as_view("etoro_deposits_edit"))
etoro_api.add_url_rule("/etoro/deposits/delete", view_func=EtoroDepositsDeleteView.as_view("etoro_deposits_delete"))