def format_daily_post(ai_data: dict, url: str) -> str:
    """Formats the extracted data into the requested daily post template."""
    hashtags_str = " ".join([tag if tag.startswith('#') else f"#{tag}" for tag in ai_data.get('hashtags', [])])
    
    # Base template
    template = f"""---
🪙 இன்றைய நாணய வரலாறு | Today's Coin History

🏛️ {ai_data.get('topic_name', 'Not specified')}

📜 காலம் | Period: {ai_data.get('period', 'Not mentioned')}
📍 கண்டுபிடிக்கப்பட்ட இடம் | Found at: {ai_data.get('location', 'Not mentioned')}"""

    # Add Ruler/Dynasty if applicable
    ruler = ai_data.get('ruler_dynasty', 'Not mentioned')
    if ruler and ruler.lower() != 'not mentioned':
        template += f"\n👑 ஆட்சியாளர் | Ruler/Dynasty: {ruler}"
        
    template += f"""

📖 தமிழில் | In Tamil:
{ai_data.get('tamil_summary', '')}

📖 In English:
{ai_data.get('english_summary', '')}

🔗 மேலும் படிக்க | Read More: {url}

#Numismatics #Heritage #AncientCoins #நாணயவரலாறு {hashtags_str}
---"""
    
    return template

def format_weekly_digest(articles: list, total_count: int, sources: list) -> str:
    """Formats the weekly digest template."""
    template = """---
🏆 இந்த வார சிறந்த நாணய செய்திகள்
   This Week's Top Numismatic News

"""
    
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, article in enumerate(articles[:10]):
        emoji = number_emojis[i] if i < len(number_emojis) else f"{i+1}."
        title = article.get('title', '')
        source = article.get('source', 'Unknown Source')
        # Note: If you want these to be clickable, you can format them as markdown links in Telegram
        template += f"{emoji} {title} - {source}\n"
        
    sources_str = ", ".join(sources)
        
    template += f"""
📊 இந்த வாரம் | This Week: {total_count} articles collected
🌍 Sources: {sources_str}

#WeeklyCoins #Numismatics
---"""
    
    return template
