from pydantic import BaseModel


class PredictHistory(BaseModel):
    """
    Class PredictHistory
    ------------------
    Properties:
        name: str
        Name of the image 
        predictions: str
        Predictions for the image
        blur, missing, overexposed, sharp: float
        Probability for each class
    """
    name: str
    predictions: str
    blur: float
    missing: float
    overexposed: float
    sharp: float