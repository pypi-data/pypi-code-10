import urllib

from generic_client import PredataGenericClient


class PredataAnalysisClient(PredataGenericClient):

    """
    Client for requesting Predata analysis information.
    """

    def list_country_drivers(self, iso3, date=None, n=None):
        """
        List top signal drivers for country overview signal.
        """
        endpoint = "analysis/drivers/countries/%s/" % iso3
        query_dict = {
            "n": n,
            "date": date.isoformat() if date else None,
        }
        params = urllib.urlencode({k: query_dict[k] for k in query_dict.keys() if query_dict[k]})
        endpoint += "?" + params
        return {
            "iso3": iso3,
            "date": date.isoformat() if date else None,
            "n": n if n else 3,
            "result": self.make_request(endpoint)
        }

    def list_topic_drivers(self, topic_id, date=None, n=None):
        """
        List top signal drivers for topic overview signal.
        """
        endpoint = "analysis/drivers/topics/%s/" % topic_id
        query_dict = {
            "n": n,
            "date": date.isoformat() if date else None,
        }
        params = urllib.urlencode({k: query_dict[k] for k in query_dict.keys() if query_dict[k]})
        endpoint += "?" + params
        return {
            "topic_id": topic_id,
            "date": date.isoformat() if date else None,
            "n": n if n else 3,
            "result": self.make_request(endpoint)
        }

    def list_country_predictions(self, iso3=None, date=None, maximum=False, prediction_type=None,
                                 prediction_window=None):
        """
        List country predictions.
        """
        endpoint = "analysis/predictions/countries/"
        query_dict = {
            "iso3": iso3,
            "date": date.isoformat() if date else None,
            "max": maximum,
            "heatmap_type": prediction_type,
            "prediction_window": prediction_window
        }
        params = urllib.urlencode({k: query_dict[k] for k in query_dict.keys() if query_dict[k]})
        endpoint += "?" + params
        return {
            "iso3": iso3,
            "date": date.isoformat() if date else None,
            "max": maximum,
            "prediction_type": prediction_type,
            "prediction_window": prediction_window,
            "result": self.make_request(endpoint)
        }

    def list_topic_predictions(self, topic_id=None, date=None, maximum=False, prediction_type=None,
                               prediction_window=None):
        """
        List country predictions.
        """
        endpoint = "analysis/predictions/topics/"
        query_dict = {
            "topic_id": topic_id,
            "max": maximum,
            "date": date.isoformat() if date else None,
            "heatmap_type": prediction_type,
            "prediction_window": prediction_window
        }
        params = urllib.urlencode({k: query_dict[k] for k in query_dict.keys() if query_dict[k]})
        endpoint += "?" + params
        return {
            "topic_id": topic_id,
            "date": date.isoformat() if date else None,
            "max": maximum,
            "prediction_type": prediction_type,
            "prediction_window": prediction_window,
            "result": self.make_request(endpoint)
        }
