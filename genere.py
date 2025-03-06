import sys

# Function to generate the html file
def generate_html_file(assets):
    # Assuming a simple template for the HTML table
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="styles.css" />
    <title>Resources galery</title>
</head>
<body>
    <div class="container">
    <h1>Visualisateur</h1>
    <h3>d'images/video</h3>
    <section class="table-section">
        <table class="styled-table">
        <thead>
            <tr>
            <th>ressource</th>
            <th>alt</th>
            </tr>
        </thead>
        <tbody>
    """

    for asset in assets:
        path, alt, asset_type = asset
        if asset_type == "IMAGE:":
            tableRow = f"""
                <tr>
                  <td data-type="image">{path}</td>
                  <td>{alt}</td>
                </tr>
            """
        elif asset_type == "VIDEO:":
            tableRow = f"""
                <tr>
                  <td data-type="video">{path}</td>
                  <td>{alt}</td>
                </tr>
            """
        html += tableRow
    
    html+= """
</tbody>
</table>
<div class="nav-btns">
    <button class="carousel-btn nav-btn">Carrousel</button>
    <button class="gallery-btn nav-btn">Gallerie</button>
</div>
</section>
<section class="display-section"></section>
</div>
<script src="script.js"></script>
</body>
</html>"""

    return html


# Function to save the HTML content to a file
def save_html(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

# Function to parse input from stdin
def parse_input():
    assets = []
    # Read and split the input from stdin
    input_lines = sys.stdin.read().strip().splitlines()

    # Ignore the first line since it has the path
    input_lines = input_lines[1:]  
    
    for line in input_lines:
        parts = line.split(' ', 2)  # Split by first space (to separate type from URL)
        if len(parts) == 3:
            asset_type, url, alt = parts
            if asset_type in ["IMAGE:", "VIDEO:"]:
                assets.append((url, alt.strip('"'), asset_type))
    
    return assets

def main():
    # Get optional filename from command-line arguments
    filename = "index.html"
    if(len(sys.argv)>1):
        filename = sys.argv[1]
        
    # Read the input paths from stdin (piped input)
    assets = parse_input()
    
    # Generate the HTML content
    html_content = generate_html_file(assets)
    
    # Save the HTML to index.html
    save_html(html_content, filename)

if __name__=="__main__":
    main()