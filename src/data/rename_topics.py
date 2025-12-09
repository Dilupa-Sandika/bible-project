import json
import os

FILE_PATH = 'topics_db.json'

# --- RENAME MAPPING (Old Name -> New Unique Name) ---
rename_map = {
    "Acknowledging God": "Knowing God",
    "Addiction": "Breaking Bondages",
    "Almighty": "God Almighty",
    "Angels": "Heavenly Angels",
    "Anger": "Controlling Anger",
    "Ascension": "Christ's Ascension",
    "Awe": "Reverence for God",
    "Baptism": "Water Baptism",
    "Beauty": "Inner Beauty",
    "Blameless": "Living Blamelessly",
    "Blessing": "God's Blessings",
    "Blood": "Blood of Jesus",
    "Body": "The Human Body",
    "Bread": "Bread of Life",
    "Calling": "God's Calling",
    "Children": "Raising Children",
    "Christmas": "Birth of Jesus",
    "Church": "Body of Christ",
    "Clothing": "Modesty & Clothing",
    "Comforter": "The Comforter",
    "Community": "Christian Fellowship",
    "Compassion": "Divine Compassion",
    "Confession": "Confessing Sins",
    "Contentment": "Finding Contentment",
    "Conversion": "Born Again",
    "Courage": "Holy Courage",
    "Covenant": "God's Covenant",
    "Creation": "God's Creation",
    "Crucifixion": "The Cross",
    "Death": "Life After Death",
    "Debt": "Financial Debt",
    "Dependence": "Depending on God",
    "Desires": "Heart's Desires",
    "Devil": "Resisting the Devil",
    "Easter": "Resurrection Sunday",
    "Encouragement": "Daily Encouragement",
    "End times": "The Last Days",
    "Equipment": "Spiritual Armor",
    "Eternal life": "Everlasting Life",
    "Evangelism": "Sharing the Gospel",
    "Evil": "Overcoming Evil",
    "Faith": "Unwavering Faith",
    "Faithfulness": "Being Faithful",
    "Family": "Christian Family",
    "Fasting": "Spiritual Fasting",
    "Father": "God the Father",
    "Fear": "Overcoming Fear",
    "Following": "Following Jesus",
    "Food": "Daily Bread",
    "Forgiveness": "Forgiving Others",
    "Freedom": "Liberty in Christ",
    "Friendship": "Godly Friendship",
    "Fruitfulness": "Bearing Fruit",
    "Generosity": "Being Generous",
    "Gentleness": "Spirit of Gentleness",
    "Giving": "Joy of Giving",
    "God": "The Lord God",
    "Goodness": "Goodness of God",
    "Gossip": "Stopping Gossip",
    "Grace": "Amazing Grace",
    "Gratitude": "Thankfulness",
    "Greed": "Overcoming Greed",
    "Harvest": "Spiritual Harvest",
    "Healing": "Divine Healing",
    "Health": "Health & Wellness",
    "Heart": "A Pure Heart",
    "Heaven": "Kingdom of Heaven",
    "Hell": "Eternal Judgment",
    "Holiness": "Living Holy",
    "Holy Spirit": "Spirit of God",
    "Honesty": "Being Honest",
    "Hope": "Eternal Hope",
    "Humility": "Being Humble",
    "Idols": "Idolatry",
    "Jesus": "Jesus Christ",
    "Joy": "Joy of the Lord",
    "Judgment": "God's Judgment",
    "Kingdom": "Kingdom of God",
    "Law": "God's Law",
    "Learning": "Gaining Knowledge",
    "Life": "Christian Life",
    "Light": "Light of the World",
    "Listening": "Listening to God",
    "Love": "Biblical Love",
    "Lying": "Truth vs Lying",
    "Marriage": "Holy Matrimony",
    "Materialism": "Worldly Possessions",
    "Mediator": "Christ the Mediator",
    "Mercy": "God's Mercy",
    "Messiah": "The Messiah",
    "Mind": "Renewing the Mind",
    "Miracles": "Signs and Wonders",
    "Money": "Biblical Finance",
    "Nearness": "Drawing Near to God",
    "Neighbor": "Loving Neighbors",
    "Obedience": "Obeying God",
    "Orphans": "Caring for Orphans",
    "Overcoming": "Victory Over Sin",
    "Patience": "Waiting on God",
    "Peace": "Inner Peace",
    "Pentecost": "Day of Pentecost",
    "Persecution": "Facing Persecution",
    "Planning": "Future Plans",
    "Poverty": "Helping the Poor",
    "Praise": "Praise and Worship",
    "Prayer": "Power of Prayer",
    "Pride": "Overcoming Pride",
    "Promises": "God's Promises",
    "Prophecy": "Biblical Prophecy",
    "Protection": "Divine Protection",
    "Punishment": "Discipline",
    "Purification": "Being Purified",
    "Rebirth": "New Creation",
    "Receiving": "Receiving from God",
    "Reconciliation": "Being Reconciled",
    "Redeemer": "Our Redeemer",
    "Relationships": "Godly Relationships",
    "Reliability": "God's Faithfulness",
    "Repentance": "Turning to God",
    "Rest": "Sabbath Rest",
    "Resurrection": "Christ's Resurrection",
    "Reward": "Heavenly Rewards",
    "Righteousness": "Righteous Living",
    "Sabbath": "Keeping the Sabbath",
    "Sacrifice": "Living Sacrifice",
    "Sadness": "Overcoming Sorrow",
    "Safety": "Safety in God",
    "Salvation": "Way of Salvation",
    "Savior": "Our Savior",
    "Second coming": "Return of Jesus",
    "Seeking": "Seeking God",
    "Self-control": "Discipline & Control",
    "Selfishness": "Selflessness",
    "Serving": "Serving Others",
    "Sexuality": "Biblical Sexuality",
    "Sickness": "Prayers for Sickness",
    "Sin": "Freedom from Sin",
    "Singing": "Singing Praises",
    "Slavery": "Servants of God",
    "Soul": "Care for the Soul",
    "Speaking": "Words We Speak",
    "Spirit": "Walking in the Spirit",
    "Strength": "God's Strength",
    "Suffering": "Hope in Suffering",
    "Temptation": "Resisting Temptation",
    "Thoughts": "Godly Thoughts",
    "Transformation": "Changed Life",
    "Trust": "Trusting God",
    "Truth": "Word of Truth",
    "Understanding": "Understanding God",
    "Valuable": "Worth to God",
    "Weakness": "Strength in Weakness",
    "Widows": "Caring for Widows",
    "Wine": "Wine and Scripture",
    "Wisdom": "Godly Wisdom",
    "Word of God": "The Holy Bible",
    "Work": "Work Ethic",
    "World": "The World vs God",
    "Worry": "Overcoming Worry",
    "Worship": "True Worship"
}

def rename_topics():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    try:
        with open(FILE_PATH, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        updated_count = 0
        
        for topic in data:
            current_title = topic['title_en']
            
            # Check if we have a new name for this topic
            if current_title in rename_map:
                new_title = rename_map[current_title]
                new_id = new_title.lower().replace(" ", "-").replace("'", "").replace("&", "and")
                
                # Update Fields
                topic['title_en'] = new_title
                # Reset Spanish Title to force translation later (Optional)
                topic['title_es'] = new_title 
                topic['id'] = new_id
                
                # Update Image Path (Optional - to match new ID)
                # topic['image'] = f"/images/themes/{new_id}.jpg" 
                
                # Update SEO
                if 'seo' in topic:
                    topic['seo']['en']['title'] = f"Bible Verses about {new_title}"
                    topic['seo']['en']['description'] = f"Discover what the Bible says about {new_title}. Read and share scripture."
                    topic['seo']['en']['alt_text'] = f"{new_title} bible verses background"
                
                updated_count += 1
                print(f"Renamed: {current_title} -> {new_title}")

        # Sort A-Z by New Title
        data.sort(key=lambda x: x['title_en'])

        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print("-" * 30)
        print(f"✅ Success! Renamed {updated_count} topics.")
        print("⚠️ IMPORTANT: Now run 'python force_translate.py' to update Spanish titles.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    rename_topics()