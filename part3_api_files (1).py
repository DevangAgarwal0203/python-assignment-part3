import requests
from datetime import datetime


def log_error(context, error_msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {context}: {error_msg}\n"
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  Logged: {entry.strip()}")


# Task 1

print("Task 1 - File Read & Write")

notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes.",
]

with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in notes:
        f.write(line + "\n")

print("File written successfully.")

extra = [
    "Topic 6: Functions make code reusable and easier to read.",
    "Topic 7: Modules let you split code into separate files.",
]

with open("python_notes.txt", "a", encoding="utf-8") as f:
    for line in extra:
        f.write(line + "\n")

print("Lines appended.")

print("\nFile contents:")
with open("python_notes.txt", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

for idx, line in enumerate(all_lines, start=1):
    print(f"{idx}. {line.rstrip()}")

print(f"\nTotal lines : {len(all_lines)}")

keyword = input("\nEnter a keyword to search: ").strip().lower()
matches = [l.rstrip() for l in all_lines if keyword in l.lower()]
if matches:
    print(f"Lines containing '{keyword}':")
    for m in matches:
        print(f"  {m}")
else:
    print(f"No lines found containing '{keyword}'.")


# Task 2

print("\nTask 2 - API Integration")

BASE_URL = "https://dummyjson.com/products"
products = []

print("\nFetching 20 products...")
try:
    resp = requests.get(f"{BASE_URL}?limit=20", timeout=5)
    data = resp.json()
    products = data.get("products", [])

    print(f"\n{'ID':<5}| {'Title':<32}| {'Category':<15}| {'Price':<10}| {'Rating'}")
    print("-" * 70)
    for p in products:
        print(f"{p['id']:<5}| {p['title']:<32}| {p['category']:<15}| ${p['price']:<9.2f}| {p['rating']}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("fetch_products", "ConnectionError — Could not reach dummyjson.com")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
    log_error("fetch_products", "Timeout — Server took too long to respond")
except Exception as e:
    print(f"Unexpected error: {e}")
    log_error("fetch_products", f"Exception — {e}")

if products:
    filtered = [p for p in products if p["rating"] >= 4.5]
    filtered.sort(key=lambda p: p["price"], reverse=True)
    print("\nFiltered (rating >= 4.5), sorted by price:")
    print(f"{'ID':<5}| {'Title':<32}| {'Price':<10}| {'Rating'}")
    print("-" * 55)
    for p in filtered:
        print(f"{p['id']:<5}| {p['title']:<32}| ${p['price']:<9.2f}| {p['rating']}")

print("\nLaptops category:")
try:
    resp = requests.get(f"{BASE_URL}/category/laptops", timeout=5)
    laptops = resp.json().get("products", [])
    for lp in laptops:
        print(f"  {lp['title']} — ${lp['price']:.2f}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("fetch_laptops", "ConnectionError — Could not reach dummyjson.com")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
    log_error("fetch_laptops", "Timeout — Server took too long")
except Exception as e:
    print(f"Unexpected error: {e}")
    log_error("fetch_laptops", f"Exception — {e}")

print("\nPOST new product:")
new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API",
}
try:
    resp = requests.post(f"{BASE_URL}/add", json=new_product, timeout=5)
    print(resp.json())

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("post_product", "ConnectionError — Could not reach dummyjson.com")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
    log_error("post_product", "Timeout — Server took too long")
except Exception as e:
    print(f"Unexpected error: {e}")
    log_error("post_product", f"Exception — {e}")


# Task 3

print("\nTask 3 - Exception Handling")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nsafe_divide tests:")
print(f"safe_divide(10, 2)    = {safe_divide(10, 2)}")
print(f"safe_divide(10, 0)    = {safe_divide(10, 0)}")
print(f"safe_divide('ten', 2) = {safe_divide('ten', 2)}")


def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print("File operation attempt complete.")

print("\nReading 'python_notes.txt':")
content = read_file_safe("python_notes.txt")
if content:
    print(content[:80] + "...")

print("\nReading 'ghost_file.txt':")
read_file_safe("ghost_file.txt")

print("\nAll API calls in Task 2 include try-except for ConnectionError, Timeout, and Exception.")

print("\nProduct ID lookup (type 'quit' to exit):")
while True:
    user_input = input("Enter a product ID (1-100) or 'quit': ").strip()

    if user_input.lower() == "quit":
        print("Exiting lookup.")
        break

    try:
        pid = int(user_input)
        if pid < 1 or pid > 100:
            print("Please enter a number between 1 and 100.\n")
            continue
    except ValueError:
        print("That's not a valid integer. Try again.\n")
        continue

    try:
        resp = requests.get(f"{BASE_URL}/{pid}", timeout=5)
        if resp.status_code == 404:
            print(f"Product not found (ID {pid}).")
        elif resp.status_code == 200:
            p = resp.json()
            print(f"  Title : {p['title']}")
            print(f"  Price : ${p['price']:.2f}\n")
        else:
            print(f"Unexpected status: {resp.status_code}")

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("lookup_product", f"ConnectionError — ID {pid}")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("lookup_product", f"Timeout — Product ID {pid}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("lookup_product", f"Exception — {e}")


# Task 4

print("\nTask 4 - Error Logger")

print("\nTriggering ConnectionError with unreachable URL...")
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError as e:
    print("Connection failed. Please check your internet.")
    log_error("fetch_products", f"ConnectionError — {e}")
except requests.exceptions.Timeout:
    print("Request timed out.")
    log_error("fetch_products", "Timeout")
except Exception as e:
    log_error("fetch_products", f"Exception — {e}")

print("\nLooking up product ID 999 (expect 404)...")
try:
    resp = requests.get(f"{BASE_URL}/999", timeout=5)
    if resp.status_code != 200:
        log_error("lookup_product", f"HTTPError — {resp.status_code} Not Found for product ID 999")
        print(f"  Logged 404 for product ID 999.")
    else:
        p = resp.json()
        print(f"  Found: {p['title']}")
except requests.exceptions.ConnectionError:
    print("Connection failed.")
    log_error("lookup_product", "ConnectionError — Could not reach dummyjson.com")
except requests.exceptions.Timeout:
    print("Request timed out.")
    log_error("lookup_product", "Timeout — product ID 999")
except Exception as e:
    log_error("lookup_product", f"Exception — {e}")

print("\nContents of error_log.txt:")
try:
    with open("error_log.txt", "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("error_log.txt not found.")
