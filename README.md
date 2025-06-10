# Phase 13: Direct Animation Integration

This module demonstrates the concept of sending generated patient animation scripts to a service like [D-ID](https://www.d-id.com/) to produce narrated videos.

## How It Works
- You input a procedure and patient language
- The AI generates a plain-language script
- The script is sent to the D-ID API (or similar)
- You get back a video URL or downloadable file

## Integration
Replace the stub in `did_integration.py` with actual D-ID API requests using your API key.

## Example Usage
```python
from did_integration import generate_did_video
video_url = generate_did_video("Your tooth needs a crown because...")
print(video_url)
```
