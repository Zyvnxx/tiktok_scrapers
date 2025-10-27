import requests
import os
import time
import json
from urllib.parse import urlparse

def get_tiktok_video_info(video_url):
    """
    Dapatkan informasi video TikTok
    """
    try:
        api_url = 'https://www.tikwm.com/api/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.post(api_url, data={'url': video_url}, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data
        return None
        
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None

def download_tiktok_video_api(video_url, save_folder="downloads"):
    """
    Download video TikTok menggunakan API pihak ketiga
    """
    try:
        # Buat folder jika belum ada
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        api_url = 'https://www.tikwm.com/api/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        print(f"Mencoba download: {video_url}")
        
        # Dapatkan data video
        response = requests.post(api_url, data={'url': video_url}, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('data') and data['data'].get('play'):
                video_download_url = data['data']['play']
                print(f"✓ Video URL ditemukan")
                
                # Download video
                video_response = requests.get(video_download_url, stream=True, timeout=30)
                
                if video_response.status_code == 200:
                    # Generate filename
                    video_id = urlparse(video_url).path.split('/')[-1]
                    filename = f"tiktok_{video_id}.mp4"
                    filepath = os.path.join(save_folder, filename)
                    
                    # Dapatkan full absolute path
                    absolute_path = os.path.abspath(filepath)
                    
                    # Download dengan progress
                    total_size = int(video_response.headers.get('content-length', 0))
                    downloaded_size = 0
                    
                    with open(filepath, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)
                                if total_size > 0:
                                    progress = (downloaded_size / total_size) * 100
                                    print(f"Progress: {progress:.1f}%", end='\r')
                    
                    print(f"\n✓ Download selesai: {filepath}")
                    
                    # Return data video untuk disimpan di JSON
                    video_info = {
                        'url': video_url,
                        'id': video_id,
                        'filename': filename,
                        'download_path': filepath,
                        'absolute_path': absolute_path,
                        'folder_location': os.path.abspath(save_folder),
                        'title': data['data'].get('title', ''),
                        'author': data['data'].get('author', {}).get('nickname', ''),
                        'duration': data['data'].get('duration', ''),
                        'download_url': video_download_url,
                        'file_size': os.path.getsize(filepath) if os.path.exists(filepath) else 0,
                        'download_time': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    return video_info
        
        print("✗ Gagal download")
        return None
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def main():
    """
    Main function untuk download multiple videos
    """
    # LIST URL VIDEO TIKTOK YANG MAU DIDOWNLOAD
    tiktok_urls = [
        "https://www.tiktok.com/@kemoooonnnnn/video/7563488421830823176",
        "https://www.tiktok.com/@kemoooonnnnn/video/7552568040936738056", 
        "https://www.tiktok.com/@kemoooonnnnn/video/7545085888359927047",
        # Tambahkan URL lainnya di sini
    ]
    
    print(f"Memulai download {len(tiktok_urls)} video...")
    
    successful_downloads = 0
    all_videos_data = []  # Untuk menyimpan semua data video
    
    for i, url in enumerate(tiktok_urls, 1):
        print(f"\n[{i}/{len(tiktok_urls)}] Processing: {url}")
        
        # Download video dan dapatkan info
        video_info = download_tiktok_video_api(url)
        
        if video_info:
            successful_downloads += 1
            all_videos_data.append(video_info)
            print(f"✓ Berhasil download video {i}")
            
            # Tampilkan info lokasi
            print(f"📍 Lokasi video: {video_info['absolute_path']}")
        else:
            print(f"✗ Gagal download video {i}")
        
        # Jeda antara download
        if i < len(tiktok_urls):
            print("Menunggu 2 detik sebelum video berikutnya...")
            time.sleep(2)
    
    # ⭐⭐ SIMPAN DATA KE JSON ⭐⭐
    if all_videos_data:
        with open('tiktok_videos.json', 'w', encoding='utf-8') as f:
            json.dump(all_videos_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Data disimpan ke: {os.path.abspath('tiktok_videos.json')}")
    
    # Tampilkan summary dengan lokasi
    print(f"\n=== SUMMARY ===")
    print(f"Total video: {len(tiktok_urls)}")
    print(f"Berhasil: {successful_downloads}")
    print(f"Gagal: {len(tiktok_urls) - successful_downloads}")
    
    if successful_downloads > 0:
        print(f"\n📍 LOKASI FILE:")
        print(f"• Folder video: {os.path.abspath('downloads')}")
        print(f"• File JSON: {os.path.abspath('tiktok_videos.json')}")
        
        print(f"\n📁 FILE YANG DIDOWNLOAD:")
        for video in all_videos_data:
            print(f"• {video['filename']}")
            print(f"  📍 {video['absolute_path']}")

if __name__ == "__main__":
    main()