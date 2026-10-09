from src.logger import setup_logger
from src.data_loader import load_all_data
from src.validation import validate_all_tables
from src.data_cleaner import clean_data, save_cleaned_data

def run_pipeline():
    logger = setup_logger()
    logger.info("Starting Motor Insurance Data Pipeline...")
    
    try:
        # 1. Load Data
        logger.info("Loading raw data from data/raw/...")
        raw_data = load_all_data("data/raw")
        logger.info("Data loaded successfully.")
        
        # 2. Validate Data
        logger.info("Validating raw data tables and relationships...")
        validate_all_tables(raw_data)
        logger.info("Data validation passed successfully.")
        
        # 3. Clean and Transform Data
        logger.info("Cleaning data and creating derived columns...")
        cleaned_data = clean_data(raw_data)
        logger.info("Data cleaning completed successfully.")
        
        # 4. Save Cleaned Data
        logger.info("Saving cleaned datasets to data/cleaned/...")
        save_cleaned_data(cleaned_data, "data/cleaned")
        logger.info("Cleaned datasets saved successfully.")
        
        logger.info("Motor Insurance Data Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        raise e

if __name__ == "__main__":
    run_pipeline()
