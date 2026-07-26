import os
import sys
import json
import httpx
from lxml import html
from datetime import datetime

def main():
    username = "NnAsankaMadushan"
    url = f"https://github.com/users/{username}/contributions"
    print(f"Fetching contributions from {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = httpx.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching contributions: {e}")
        # Try local fallback if file exists, or crash nicely
        sys.exit(1)
        
    tree = html.fromstring(response.text)
    
    # We look for `<td data-date="..."` or standard SVG rects
    # GitHub changed their contribution calendar markup to use <td class="ContributionCalendar-day">
    days_elements = tree.xpath("//td[@class='ContributionCalendar-day'] | //rect[@class='ContributionCalendar-day']")
    
    if not days_elements:
        print("Warning: No contribution calendar days found in HTML. Trying generic xpath.")
        days_elements = tree.xpath("//*[@data-date]")
        
    contributions = []
    
    for day in days_elements:
        date_str = day.get("data-date")
        if not date_str:
            continue
            
        # Get count. Depending on the element, it might be in text content, or data-count, or parsed from tooltips.
        # Often data-level is directly present: "0", "1", "2", "3", "4"
        level_str = day.get("data-level", "0")
        try:
            level = int(level_str)
        except ValueError:
            level = 0
            
        # Get data-count if available
        count_str = day.get("data-count")
        if not count_str:
            # Let's inspect the ID/tooltip, or map level to approximate values
            # Alternatively, if there's no data-count, we count using text matching or similar.
            count = level * 2  # simple fallback estimation
        else:
            try:
                count = int(count_str)
            except ValueError:
                count = level * 2
                
        contributions.append({
            "date": date_str,
            "level": level,
            "count": count
        })
        
    if not contributions:
        print("Error: Could not parse any contributions data. GitHub page layout might have changed.")
        sys.exit(1)
        
    # Sort contributions by date
    contributions.sort(key=lambda x: x["date"])
    
    # Calculate stats
    total_contributions = sum(d["count"] for d in contributions)
    
    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Calculate streaks from sorted contributions
    for d in contributions:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak backwards from today
    # Find active streak at the end of the list
    active_streak = 0
    for d in reversed(contributions):
        # Allow today or yesterday as the start of the current streak
        if d["count"] > 0:
            active_streak += 1
        elif d["date"] < today_str:
            # If we hit a zero before today, the streak is broken
            break
    current_streak = active_streak

    # Busiest day of week breakdown
    weekday_counts = [0] * 7 # 0 = Monday, 6 = Sunday
    for d in contributions:
        if d["count"] > 0:
            dt = datetime.strptime(d["date"], "%Y-%m-%d")
            weekday_counts[dt.weekday()] += d["count"]
            
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    busiest_day_idx = weekday_counts.index(max(weekday_counts)) if sum(weekday_counts) > 0 else 0
    busiest_day = weekdays[busiest_day_idx]
    
    data = {
        "total": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "busiest_day": busiest_day,
        "contributions": contributions
    }
    
    os.makedirs("assets", exist_ok=True)
    with open("assets/contributions.json", "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully saved {len(contributions)} contributions to assets/contributions.json")
    print(f"Total: {total_contributions}, Current Streak: {current_streak}, Longest: {longest_streak}, Busiest Day: {busiest_day}")

if __name__ == "__main__":
    main()
