from fastapi import FastAPI

app = FastAPI()

class ApiEndpoints:
    def __init__(self):
        try:
            if os.environ['AWS_ENDPOINT_URL']:
                self.aws_endpoint = os.environ['AWS_ENDPOINT_URL']
        except KeyError as e:
            self.aws_endpoint = 'http://localhost:4566'
        print(f"AWS_ENDPOINT_URL [ {self.aws_endpoint} ]")
        
    @app.get("/train")
    async def train(self):
        print(f"TRAIN!")

    @app.predict("/predict")
    def predict(self):
        print(f"PREDICT!")        