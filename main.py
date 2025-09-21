import os
import sys
from PIL import Image
import argparse

def resize_images(input_folder, output_folder=None, width=800, height=600, format='JPEG', quality=85, maintain_aspect=True):
    """
    Resize all images in a folder
    
    Args:
        input_folder (str): Path to folder containing images
        output_folder (str): Path to output folder (optional)
        width (int): Target width
        height (int): Target height
        format (str): Output format (JPEG, PNG, WEBP, etc.)
        quality (int): Quality for JPEG (1-100)
        maintain_aspect (bool): Whether to maintain aspect ratio
    """
    
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    # Create output folder if not specified
    if output_folder is None:
        output_folder = os.path.join(input_folder, 'resized')
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all image files from input folder
    image_files = []
    for file in os.listdir(input_folder):
        if os.path.splitext(file.lower())[1] in supported_formats:
            image_files.append(file)
    
    if not image_files:
        print(f"No supported image files found in {input_folder}")
        return
    
    print(f"Found {len(image_files)} images to process")
    print(f"Target size: {width}x{height}")
    print(f"Output format: {format}")
    print(f"Maintain aspect ratio: {maintain_aspect}")
    print("-" * 50)
    
    processed = 0
    errors = 0
    
    for filename in image_files:
        try:
            input_path = os.path.join(input_folder, filename)
            
            # Open image
            with Image.open(input_path) as img:
                print(f"Processing: {filename} ({img.size[0]}x{img.size[1]})")
                
                # Convert RGBA to RGB for JPEG
                if format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize image
                if maintain_aspect:
                    # Calculate aspect ratio preserving resize
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                    resized_img = img
                else:
                    # Force exact dimensions
                    resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Generate output filename
                name, _ = os.path.splitext(filename)
                if format.upper() == 'JPEG':
                    output_filename = f"{name}.jpg"
                else:
                    output_filename = f"{name}.{format.lower()}"
                
                output_path = os.path.join(output_folder, output_filename)
                
                # Save image
                save_kwargs = {}
                if format.upper() == 'JPEG':
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                elif format.upper() == 'PNG':
                    save_kwargs['optimize'] = True
                elif format.upper() == 'WEBP':
                    save_kwargs['quality'] = quality
                    save_kwargs['method'] = 6
                
                resized_img.save(output_path, format=format.upper(), **save_kwargs)
                
                # Show new size
                print(f"  → Saved: {output_filename} ({resized_img.size[0]}x{resized_img.size[1]})")
                processed += 1
                
        except Exception as e:
            print(f"  ✗ Error processing {filename}: {str(e)}")
            errors += 1
    
    print("-" * 50)
    print(f"Processing complete!")
    print(f"Successfully processed: {processed} images")
    if errors > 0:
        print(f"Errors: {errors} images")
    print(f"Output folder: {output_folder}")

def main():
    parser = argparse.ArgumentParser(description='Batch Image Resizer Tool')
    parser.add_argument('input_folder', help='Path to folder containing images')
    parser.add_argument('-o', '--output', help='Output folder (default: input_folder/resized)')
    parser.add_argument('-w', '--width', type=int, default=800, help='Target width (default: 800)')
    parser.add_argument('-h', '--height', type=int, default=600, help='Target height (default: 600)')
    parser.add_argument('-f', '--format', choices=['JPEG', 'PNG', 'WEBP'], default='JPEG', help='Output format (default: JPEG)')
    parser.add_argument('-q', '--quality', type=int, default=85, help='JPEG/WEBP quality 1-100 (default: 85)')
    parser.add_argument('--no-aspect', action='store_true', help='Don\'t maintain aspect ratio')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist")
        sys.exit(1)
    
    if not os.path.isdir(args.input_folder):
        print(f"Error: '{args.input_folder}' is not a directory")
        sys.exit(1)
    
    resize_images(
        input_folder=args.input_folder,
        output_folder=args.output,
        width=args.width,
        height=args.height,
        format=args.format,
        quality=args.quality,
        maintain_aspect=not args.no_aspect
    )

# Example usage functions
def resize_to_thumbnails(folder_path):
    """Quick function to create thumbnails (200x200)"""
    resize_images(folder_path, width=200, height=200, format='JPEG', quality=80)

def resize_for_web(folder_path):
    """Quick function to resize for web (1200x800)"""
    resize_images(folder_path, width=1200, height=800, format='JPEG', quality=85)

def convert_to_webp(folder_path):
    """Quick function to convert all images to WebP format"""
    resize_images(folder_path, width=1920, height=1080, format='WEBP', quality=80)

if __name__ == "__main__":
    # If no command line arguments, show usage example
    if len(sys.argv) == 1:
        print("Image Resizer Tool")
        print("==================")
        print()
        print("Command line usage:")
        print("python image_resizer.py /path/to/images")
        print("python image_resizer.py /path/to/images -w 1200 -h 800 -f PNG")
        print("python image_resizer.py /path/to/images -o /path/to/output --no-aspect")
        print()
        print("Interactive usage:")
        folder = input("Enter path to image folder: ").strip()
        if folder and os.path.exists(folder):
            print("\nChoose an option:")
            print("1. Custom resize")
            print("2. Create thumbnails (200x200)")
            print("3. Resize for web (1200x800)")
            print("4. Convert to WebP")
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":
                try:
                    w = int(input("Enter width (default 800): ") or "800")
                    h = int(input("Enter height (default 600): ") or "600")
                    fmt = input("Enter format JPEG/PNG/WEBP (default JPEG): ") or "JPEG"
                    resize_images(folder, width=w, height=h, format=fmt.upper())
                except ValueError:
                    print("Invalid input")
            elif choice == "2":
                resize_to_thumbnails(folder)
            elif choice == "3":
                resize_for_web(folder)
            elif choice == "4":
                convert_to_webp(folder)
            else:
                print("Invalid choice")
        else:
            print("Invalid folder path")
    else:
        main()
