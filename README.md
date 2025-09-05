<p align="center">
  <img width="300" height="300" src="http://asset.anvesh.rf.gd/github/Adult-Content-Image-Detector/logo.png">
</p>

# Adult Content Image Detector

A Python-based tool for detecting adult content in images using machine learning APIs and computer vision techniques. This tool is designed for content moderation, parental controls, and maintaining safe digital environments.

## ⚠️ Important Notice

This tool is intended for legitimate purposes such as:
- Content moderation for websites and platforms
- Parental control systems
- Automated content filtering for educational environments
- Personal digital hygiene and safety

Please use responsibly and in accordance with local laws and regulations.

## 🚀 Features

- **Multi-API Detection**: Integrates with multiple content moderation APIs for high accuracy
- **Fallback Detection**: Basic computer vision-based detection when APIs are unavailable
- **Safe Deletion**: Moves flagged content to trash instead of permanent deletion
- **Image Validation**: Supports multiple image formats with validation
- **User Confirmation**: Requires user approval before any file operations
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.7+
- OpenCV
- PIL/Pillow
- NumPy
- Requests

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/developeranveshraman/Adult-Image-Detector.git
   cd Adult-Image-Detector
   ```

2. **Install required packages:**

   For regular use: 
   ```bash
   pip install -r requirements.txt
   ```
   For development:
   ```bash
   pip install -r requirements-dev.txt
   ```

   Or install manually:
   ```bash
   pip install opencv-python pillow requests numpy
   ```

4. **Optional (for Windows trash functionality):**
   ```bash
   pip install winshell
   ```

## 🔧 Configuration

### API Keys Setup

For optimal accuracy, configure API keys from supported services:

1. **ModerateContent API**
   - Sign up at [moderatecontent.com](https://moderatecontent.com/)
   - Get your API key
   - Replace `YOUR_MODERATECONTENT_API_KEY` in the code

2. **Sightengine API**
   - Sign up at [sightengine.com](https://sightengine.com/)
   - Get your API user and secret
   - Replace `YOUR_SIGHTENGINE_USER` and `YOUR_SIGHTENGINE_SECRET` in the code

### Environment Variables (Optional)

You can set API keys as environment variables:

```bash
export MODERATECONTENT_API_KEY="your_api_key_here"
export SIGHTENGINE_API_USER="your_user_here"
export SIGHTENGINE_API_SECRET="your_secret_here"
```

## 🚀 Usage

### Command Line Interface

```bash
python index.py
```

The program will prompt you to enter image paths for analysis.

### Programmatic Usage

```python
from adult_content_detector import AdultContentDetector

detector = AdultContentDetector()
is_adult_content = detector.process_image("path/to/image.jpg")

if is_adult_content:
    print("Adult content detected!")
else:
    print("Image is safe.")
```

### Batch Processing

```python
import os
from adult_content_detector import AdultContentDetector

detector = AdultContentDetector()
image_folder = "path/to/images"

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        image_path = os.path.join(image_folder, filename)
        detector.process_image(image_path)
```

## 📁 Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)
- WebP (.webp)

## 🧠 Detection Methods

### 1. API-Based Detection (Recommended)
- **ModerateContent API**: Advanced ML models for content classification
- **Sightengine API**: Specialized in nudity and adult content detection
- High accuracy and reliability

### 2. Basic Computer Vision
- Skin tone detection using HSV color space
- Fallback method when APIs are unavailable
- Lower accuracy, use with caution

## 🔒 Privacy and Security

- **Local Processing**: Basic detection runs entirely on your machine
- **API Communication**: Only when configured and consented
- **Safe Deletion**: Files moved to trash, not permanently deleted
- **No Data Storage**: No images or results stored by this tool

## ⚙️ Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `use_api` | Enable API-based detection | `True` |
| `skin_threshold` | Skin detection sensitivity (0.0-1.0) | `0.3` |
| `adult_threshold` | API confidence threshold (0.0-1.0) | `0.5` |

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid image file" error**
   - Ensure the file is a supported image format
   - Check if the file is corrupted

2. **API errors**
   - Verify your API keys are correct
   - Check your internet connection
   - Ensure you haven't exceeded API limits

3. **Permission errors during deletion**
   - Run with appropriate permissions
   - Check if the file is in use by another program

### Debug Mode

Enable debug output:

```python
detector = AdultContentDetector()
detector.debug = True
```

## 📊 Accuracy Notes

- **API-based detection**: 95-99% accuracy (depending on service)
- **Basic skin detection**: 60-70% accuracy (many false positives)
- **Recommendation**: Always use API-based detection for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 adult_content_detector.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Disclaimer

This software is provided for educational and legitimate content moderation purposes only. Users are responsible for:

- Complying with local laws and regulations
- Respecting privacy and consent requirements
- Using the tool ethically and responsibly
- Not using it for harassment or illegal activities

The developers are not responsible for misuse of this software.

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/developeranveshraman/Adult-Content-Image-Detector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/developeranveshraman/Adult-Content-Image-Detector/discussions)
- **Email**: support@anveshraman.rf.gd

## 📚 References

- [OpenCV Documentation](https://docs.opencv.org/)
- [ModerateContent API Docs](https://docs.moderatecontent.com/)
- [Sightengine API Docs](https://docs.sightengine.com/)

---

**⭐ If this project helped you, please consider giving it a star!**
