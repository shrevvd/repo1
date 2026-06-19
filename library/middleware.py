class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.status_2xx = 0
        self.status_4xx = 0
        self.status_5xx = 0
        self.request_count_since_last_log = 0
        self.error_rate = 0.0

    def __call__(self, request):

        path = request.path
        
        if (
            path.startswith('/static/') or 
            path.startswith('/media/') or 
            path.endswith('.css') or 
            path.endswith('.js') or 
            'favicon.ico' in path or
            'jsi18n' in path or
            'img' in path
        ):
            return self.get_response(request)

        response = self.get_response(request)
        
        self.total_requests += 1
        self.request_count_since_last_log += 1
        
        status_code = response.status_code
        if 200 <= status_code < 300:
            self.status_2xx += 1
        elif 400 <= status_code < 500:
            self.status_4xx += 1
        elif 500 <= status_code < 600:
            self.status_5xx += 1
            
        if self.request_count_since_last_log >= 10:
            self._log_metrics()
            self.request_count_since_last_log = 0
            
        return response

    def _log_metrics(self):
        total_errors = self.status_4xx + self.status_5xx
        
        if self.total_requests > 0:
            self.error_rate = (total_errors / self.total_requests) * 100
        else:
            self.error_rate = 0.0

        print("- METRICS -")
        print(f"Total requests: {self.total_requests}")
        print(f"2xx: {self.status_2xx}, 4xx: {self.status_4xx}, 5xx: {self.status_5xx}")
        print(f"error_rate: {self.error_rate:.2f}%")
        print("------------")
