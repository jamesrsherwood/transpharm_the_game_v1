# Sustainable Pharmaceuticals Game

An educational game about pharmaceutical sustainability and environmental impact, built with Pygame.

## Play Online

The game is hosted on GitHub Pages: [Play Now](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/)

## Local Development

### Prerequisites
- Python 3.11 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Deploying to GitHub Pages

This project is configured to automatically build and deploy to GitHub Pages using Pygbag.

### Setup Instructions

1. **Create a GitHub repository** (if you haven't already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to Settings → Pages
   - Under "Build and deployment", set Source to "GitHub Actions"

3. **The deployment will happen automatically**:
   - Every push to the `main` or `master` branch triggers the workflow
   - You can also manually trigger it from the Actions tab
   - After the workflow completes, your game will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

### Manual Build (Optional)

If you want to test the Pygbag build locally:

```bash
# Install pygbag
pip install pygbag

# Build the project
pygbag --build .

# The built files will be in ./build/web
```

## Project Structure

```
.
├── main.py              # Main game entry point (async for Pygbag)
├── requirements.txt     # Python dependencies
├── index.html          # Custom HTML template for web version
├── .github/
│   └── workflows/
│       └── pygbag.yml  # GitHub Actions workflow
├── data/               # Game data and maps
├── graphics/           # Game assets
└── *.py               # Other game modules
```

## How it Works

The game uses Pygbag to convert Pygame to WebAssembly for browser compatibility:

1. **Async Game Loop**: The main game loop is converted to `async def run()` with `await asyncio.sleep(0)` to yield control to the browser
2. **Asset Loading**: All assets are loaded using relative paths compatible with Pygbag
3. **GitHub Actions**: Automatically builds and deploys on every push
4. **GitHub Pages**: Hosts the built WebAssembly files

## Controls

- **Arrow Keys**: Move player
- **Space**: Interact with NPCs
- **Enter**: Open/close monster index
- **ESC**: Close menus

## Requirements

The game requires:
- pygame-ce (Community Edition)
- pytmx (for TMX map support)

## License

[Add your license here]

## Credits

[Add credits here]
