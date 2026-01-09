from dataset import Dataset

creator = Dataset(700, "../data/processed/geocoded_otodom_warszawa.json")
creator.save_to_csv("warsaw_house_data_700.csv")
