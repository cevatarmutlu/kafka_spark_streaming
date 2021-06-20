import src.category_viewed as category_viewed, src.category_bought as category_bought, src.conversion_rates as conversion_rates
from pathlib import Path
import src.utils.config as config

if __name__ == "__main__":
    Path(config.get('category_management')['output_path']).mkdir(parents=True, exist_ok=True)

    category_viewed.main()
    category_bought.main()
    conversion_rates.main()