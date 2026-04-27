import requests
import time
import re
import csv

def get_game_name(app_id):
    """透過 Steam 商店 API 獲取遊戲名稱"""
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        response = requests.get(url)
        data = response.json()
        if data and str(app_id) in data and data[str(app_id)]['success']:
            return data[str(app_id)]['data']['name']
    except Exception as e:
        print(f"無法獲取遊戲名稱: {e}")
    return f"Unknown_Game_{app_id}"

def scrape_all_steam_reviews_smart():
    store_url = input("🔗 請貼上你要抓取的 Steam 遊戲網址: ").strip()
    
    match = re.search(r'/app/(\d+)', store_url)
    if not match:
        print("❌ 找不到 App ID，請確認網址。")
        return
        
    app_id = match.group(1)
    game_name = get_game_name(app_id)
    safe_game_name = re.sub(r'[\\/*?:"<>|]', "", game_name)
    csv_filename = f"{safe_game_name}_全部評論.csv"
    
    print(f"\n✅ 成功找到遊戲: 【 {game_name} 】")
    print(f"📂 資料將儲存至: {csv_filename}\n")

    api_url = f"https://store.steampowered.com/appreviews/{app_id}"
    cursor = "*"
    total_reviews_fetched = 0
    expected_total_reviews = 0
    page = 1

    with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['推薦與否', '遊玩時數(小時)', '評論內容']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            params = {
                "json": 1,
                "filter": "all",
                "language": "all",
                "cursor": cursor,
                "review_type": "all",
                "purchase_type": "all",
                "num_per_page": 100
            }

            try:
                response = requests.get(api_url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("success") == 1:
                    # 1. 只有第一頁時，讀取官方提供的「總評論數」
                    if page == 1 and "query_summary" in data:
                        expected_total_reviews = data["query_summary"].get("total_reviews", 0)
                        print(f"📊 官方數據顯示：總共有 {expected_total_reviews} 則評論。\n")

                    reviews = data.get("reviews", [])
                    review_count = len(reviews)
                    total_reviews_fetched += review_count
                    
                    for rev in reviews:
                        playtime_mins = rev.get('author', {}).get('playtime_forever', 0)
                        playtime_hours = round(playtime_mins / 60, 1)
                        review_text = rev.get('review', '').replace('\n', ' ')

                        writer.writerow({
                            '推薦與否': '推薦' if rev.get('voted_up') else '不推薦',
                            '遊玩時數(小時)': playtime_hours,
                            '評論內容': review_text
                        })

                    print(f"[進度] 正在抓取第 {page} 頁，目前已存入 {total_reviews_fetched} / {expected_total_reviews} 筆...", end="\r")

                    # 2. 【依照你的要求修改的斷點】：抓到數量達到或超過總數，就停！
                    if expected_total_reviews > 0 and total_reviews_fetched >= expected_total_reviews:
                        print(f"\n\n🏁 已經抓足官方標示的總數量 ({expected_total_reviews} 筆)，停止抓取！")
                        break

                    # 3. 【防呆煞車】：如果官方總數有誤差，導致我們一直空轉 (回傳 0 筆)，強制停下避免當機
                    if review_count == 0:
                        print(f"\n\n⚠️ Steam 已經沒有資料可以回傳了 (官方總數可能包含被隱藏的評論)，強制停止抓取！")
                        break

                    cursor = data.get("cursor")
                    page += 1
                else:
                    print(f"\n❌ API 回傳失敗。")
                    break

            except Exception as e:
                print(f"\n❌ 發生錯誤: {e}")
                break
            
            time.sleep(1)

    print("-" * 40)
    print(f"🎉 任務結束！實際成功寫入 CSV 的評論數：{total_reviews_fetched} 筆。")

if __name__ == "__main__":
    scrape_all_steam_reviews_smart()