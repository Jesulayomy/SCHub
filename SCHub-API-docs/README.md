# MkDocs Project Setup

This project uses MkDocs for documentation. Follow the instructions below to set it up locally, install dependencies, and serve it from GitHub Pages.

### 1. Install Dependencies

To install the required dependencies, make sure you have a `requirements.txt` file in your project directory. Use the following command:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages specified in `requirements.txt`, including MkDocs and MkDocs Material.

### 2. Serve the Documentation Locally

Once the dependencies are installed, you can serve the MkDocs documentation locally by running:

```bash
mkdocs serve
```

This will start a local development server at `http://127.0.0.1:8000`. You can open this URL in your web browser to view the documentation.

### 3. Deploying to GitHub Pages

To serve your documentation using GitHub Pages, follow this cmd:

```bash
mkdocs gh-deploy
```
