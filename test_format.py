from processor import extract_summary, format_post

title = "Rare gold coin of Gupta era found in UP"
link = "https://example.com/gupta-coin"
source = "Archaeology News"
content_summary = "A rare gold coin from the Gupta empire was discovered in Uttar Pradesh during an excavation."

print("Testing format_post...")
post = format_post(title, content_summary, link, source)
print(post)
