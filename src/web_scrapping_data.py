import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Define the URL of the FAQ page
url = "https://www.getirarac.com/tr/sikca-sorulan-sorular#genel-bilgiler-kullanim-ve-kosullar"

# Fetch the HTML content from the URL
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
else:
    print(f"Failed to fetch the URL. Status code: {response.status_code}")
    exit()

# Step 1: Extract categories
categories = {}
category_elements = soup.select('div.left ul li a.sssCats')
for category in category_elements:
    data_cat = category['data-cat']  # Get category ID
    category_name = category.get_text(strip=True)  # Get category name
    categories[data_cat] = category_name

# Step 2: Extract questions and answers
faqs = []
faq_items = soup.select('div.sssContent ul li')  # Find all FAQ items
for item in faq_items:
    # Extract the category from the class attribute
    category_class = item.get('class', [])
    category_id = next((cls.split('-')[1] for cls in category_class if cls.startswith('cat-')), None)
    category_name = categories.get(category_id, "Unknown")  # Default to "Unknown" if no category is found

    # Extract the question
    question_element = item.select_one('div.questionTitle span')
    question_text = question_element.get_text(strip=True) if question_element else "No question"

    # Extract the answer
    answer_element = item.select_one('div.answerBox')
    answer_text = answer_element.get_text(strip=True) if answer_element else "No answer"

    # Add the extracted data to the FAQs list
    faqs.append({
        'category': category_name,
        'question': question_text,
        'answer': answer_text
    })

# Step 3: Save data to CSV and JSON
# Save to CSV
df = pd.DataFrame(faqs)
df.to_csv('faq_data.csv', index=False, encoding='utf-8')

# Save to JSON
with open('faq_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(faqs, json_file, ensure_ascii=False, indent=4)

# Display a preview of the extracted data
print(f"Extracted {len(faqs)} FAQs:")
print(df.head())
