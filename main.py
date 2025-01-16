@"
import argparse
import yaml
import sys
from src.url_manager import URLManager
from src.user_manager import UserManager

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    url_manager = URLManager(config)
    user_manager = UserManager()
    
    parser = argparse.ArgumentParser(description='URL Shortener Service')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create short URL')
    create_parser.add_argument('url', help='Original URL')
    create_parser.add_argument('--lifetime', type=int, help='Lifetime in hours')
    create_parser.add_argument('--visits', type=int, help='Visits limit')
    create_parser.add_argument('--user-id', help='User ID')
    
    # Open command
    open_parser = subparsers.add_parser('open', help='Open short URL')
    open_parser.add_argument('short_url', help='Short URL')
    
    # Edit command
    edit_parser = subparsers.add_parser('edit', help='Edit URL parameters')
    edit_parser.add_argument('short_url', help='Short URL')
    edit_parser.add_argument('--visits', type=int, required=True, help='New visits limit')
    edit_parser.add_argument('--user-id', required=True, help='User ID')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete URL')
    delete_parser.add_argument('short_url', help='Short URL')
    delete_parser.add_argument('--user-id', required=True, help='User ID')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List user URLs')
    list_parser.add_argument('--user-id', required=True, help='User ID')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        user_id = args.user_id
        if not user_id:
            user_id = user_manager.create_user()
            print(f"Created new user with ID: {user_id}")
        
        short_url = url_manager.create_url(
            args.url,
            user_id,
            args.lifetime,
            args.visits
        )
        print(f"Created short URL: {short_url}")
        
    elif args.command == 'open':
        original_url = url_manager.get_url(args.short_url)
        if original_url:
            print(f"Redirecting to: {original_url}")
        else:
            print("URL not found or expired")
            
    elif args.command == 'edit':
        if url_manager.edit_url(args.short_url, args.user_id, args.visits):
            print("URL updated successfully")
        else:
            print("Failed to update URL")
            
    elif args.command == 'delete':
        if url_manager.delete_url(args.short_url, args.user_id):
            print("URL deleted successfully")
        else:
            print("Failed to delete URL")
            
    elif args.command == 'list':
        urls = url_manager.get_user_urls(args.user_id)
        if urls:
            for url in urls:
                print(f"Short URL: {url['short_url']}")
                print(f"Original URL: {url['original_url']}")
                print(f"Visits: {url['visits_count']}/{url['visits_limit']}")
                print(f"Expires at: {url['expires_at']}")
                print("---")
        else:
            print("No URLs found")

if __name__ == "__main__":
    main()
"@ | Out-File -FilePath "main.py" -Encoding UTF8
