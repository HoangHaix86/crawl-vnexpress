python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd vnexpress
scrapy crawl vnexpress -o dataset.json