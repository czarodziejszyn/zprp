class DataRecord:
    def __init__(self, circle):
        self.features = get_features(circle)
        self.label = get_label()
