def filter_books(api_data, keyword):
    """
    Filters books from Google Books API data based on keyword.
    Searches title, authors, and categories.
    """

    if not api_data or "items" not in api_data:
        return []

    keyword = keyword.lower()
    filtered_books = []

    for item in api_data.get("items", []):
        volume_info = item.get("volumeInfo", {})

        title = volume_info.get("title", "").lower()
        authors = " ".join(volume_info.get("authors", [])).lower()
        categories = " ".join(volume_info.get("categories", [])).lower()

        if keyword in title or keyword in authors or keyword in categories:
            filtered_books.append({
                "title": volume_info.get("title", "N/A"),
                "authors": volume_info.get("authors", ["Unknown"]),
                "categories": volume_info.get("categories", ["Unknown"])
            })

    return filtered_books


# =========================
# TESTING (standalone)
# =========================
if __name__ == "__main__":
    # Fake data to simulate API response
    sample_data = {
        "items": [
            {
                "volumeInfo": {
                    "title": "Python Programming",
                    "authors": ["John Doe"],
                    "categories": ["Programming"]
                }
            },
            {
                "volumeInfo": {
                    "title": "Cooking Basics",
                    "authors": ["Jane Smith"],
                    "categories": ["Cooking"]
                }
            }
        ]
    }

    keyword = input("Enter keyword to filter: ")
    results = filter_books(sample_data, keyword)

    print("\nFiltered Results:")
    if not results:
        print("No matches found.")
    else:
        for book in results:
            print(book)