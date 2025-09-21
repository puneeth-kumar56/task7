Batch Image Resizer
Batch Image Resizer is a Python command-line and interactive tool that efficiently resizes, converts, and optimizes images in bulk. It leverages the Pillow library for high-quality processing and supports multiple formats and aspect ratio settings.

Features
Resize all images in a folder automatically.

Supports JPEG, PNG, WEBP, GIF, BMP, TIFF formats.

Choose target width, height, output format, and quality.

Option to maintain or ignore aspect ratio.

Custom output folder support.

Ready-to-use CLI and interactive usage menu.

Preset functions for thumbnails, web-optimized images, and WebP conversion.

Installation
Install Python 3.8+ from [Python.org].

Install Pillow (Python Imaging Library fork):

text
pip install pillow
(Optional) Clone repository:

text
git clone https://github.com/yourusername/image-resizer.git
cd image-resizer
Usage
Command-line Interface (CLI)
bash
python image_resizer.py /path/to/images
python image_resizer.py /path/to/images -w 1200 -h 800 -f PNG
python image_resizer.py /path/to/images -o /path/to/output --no-aspect
Arguments:

input_folder : Path to folder containing images.

-o, --output : Output folder (default: input_folder/resized).

-w, --width : Target width (default: 800).

-h, --height : Target height (default: 600).

-f, --format : Output format [JPEG | PNG | WEBP] (default: JPEG).

-q, --quality : Quality for JPEG/WEBP (default: 85).

--no-aspect : Do not maintain aspect ratio.

Interactive Mode
Run the script without parameters to enter interactive mode:

text
python image_resizer.py
Follow prompts to select image folder, resize type, and settings.

Example Preset Functions
Thumbnails (200x200):

text
resize_to_thumbnails('/path/to/images')
Web (1200x800):

text
resize_for_web('/path/to/images')
WebP (1920x1080):

text
convert_to_webp('/path/to/images')
Sample Output
photos/resized/image1.jpg (800x600)

photos/resized/image2.webp (1920x1080)

Contributing
PRs, issues, and suggestions are welcome! Please check [CONTRIBUTING.md] for guidelines.

License
Licensed under MIT.

Note: Add screenshots or demo images with the following Markdown:

text
![App Screenshot](screenshots/demo.png)
Or specify size (Markdown + HTML):

text
<img src="screenshots/demo.png" width="400"/>
