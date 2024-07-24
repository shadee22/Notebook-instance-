import gradio as gr
import pandas as pd

def analyze_csv(file):
    # Read the CSV file
    df = pd.read_csv(file.name)
    
    # Get the first few rows (head)
    head = "<h2>First Few Rows</h2>" + df.head().to_html(classes='table table-striped table-hover', index=False)
    
    # Calculate missing values
    missing_values = "<h2>Missing Values</h2>" + df.isnull().sum().to_frame('Missing Values').to_html(classes='table table-striped table-hover')
    
    # Compute basic statistics
    basic_stats = "<h2>Basic Statistics</h2>" + df.describe().to_html(classes='table table-striped table-hover')
    
    return head, missing_values, basic_stats

# Create Gradio interface with basic layout
with gr.Blocks() as iface:
    gr.Markdown("# CSV File Analyzer")
    gr.Markdown("Upload a CSV file to view its head, missing values, and basic statistics.")
    
    with gr.Row():
        file_input = gr.File(label="Upload CSV file")
    
    with gr.Row():
        analyze_button = gr.Button("Analyze")
    
    with gr.Row():
        head_output = gr.HTML(label="First Few Rows")
    
    with gr.Row():
        with gr.Column():
            missing_values_output = gr.HTML(label="Missing Values")
        with gr.Column():
            basic_stats_output = gr.HTML(label="Basic Statistics")
    
    analyze_button.click(
        analyze_csv,
        inputs=file_input,
        outputs=[head_output, missing_values_output, basic_stats_output]
    )

# Launch the app
iface.launch()
