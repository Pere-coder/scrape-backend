import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium.common.exceptions import NoSuchElementException 



# latest smart phone deals
@csrf_exempt
def latest_offers(request):
    if request.method == 'GET':
        driver = webdriver.Chrome()
        driver.get("https://www.jumia.com.ng/mlp-stay-connected-deals/smartphones/")
        product_elements = driver.find_elements(By.CSS_SELECTOR, 'a.core')
        products = []
        for element in product_elements:
            text = element.text.split('\n')
                
            product = {
                    "store": text[0] if len(text) > 0 and "Store" in text[0] else None,
                    "name": text[1 if len(text) > 1 and "Store" in text[0] else 0] if len(text) > (1 if "Store" in text[0] else 0) else None,
                    "price": text[2 if len(text) > 2 and "Store" in text[0] else 1] if len(text) > (2 if "Store" in text[0] else 1) else None,
                    "original_price": text[3 if len(text) > 3 and "Store" in text[0] else 2] if len(text) > (3 if "Store" in text[0] else 2) else None,
                    "discount": text[4 if len(text) > 4 and "Store" in text[0] else 3] if len(text) > (4 if "Store" in text[0] else 3) else None,
                    "rating": text[5 if len(text) > 5 and "Store" in text[0] else 4] if len(text) > (5 if "Store" in text[0] else 4) else None,
                    "reviews": text[6 if len(text) > 6 else 5] if len(text) > (6 if "Store" in text[0] else 5) else None
                }
            products.append(product)
        driver.quit()
        return JsonResponse(products, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def techno_offers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            param = data.get('name', 'techno')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        driver = webdriver.Chrome()
        url = f"https://www.jumia.com.ng/mlp-stay-connected-deals/android-phones/{param}/#catalog-listing"
        
        try:
            driver.get(url)
            
            # Wait for the page to load completely, you may need to add a wait mechanism here
            
            Techno_elements = driver.find_elements(By.CSS_SELECTOR, 'a.core')
            
            products = []
            
            for element in Techno_elements:
                product_info = {}
                
                text = element.text
                parts = re.split(r'\(\d+\)', text)
                parts = [part.strip() for part in parts if part.strip()]
                
                combined_text = " ".join(parts)

                
                link = element.get_attribute('href')
    
                # Get the image (src attribute) from the element's child img tag
                image_element = element.find_element(By.TAG_NAME, 'img')
                image_src = image_element.get_attribute('src') if image_element else ''
                
                # Append the processed text, link, and image to the products list
                products.append({
                    'description': combined_text,
                    'link': link,
                    'image': image_src
                })
            # Close the driver after scraping
            driver.quit()
            
            # Return JSON response with the parsed products data
            return JsonResponse(products, safe=False)
        
        except Exception as e:
            # Handle exceptions gracefully
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)