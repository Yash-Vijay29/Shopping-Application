from transformers import pipeline

# Initialize the summarization pipeline with authentication
summarizer = pipeline("summarization")

def generate_summary(reviews):
    # Concatenate all reviews into a single string
    reviews_text = " ".join(reviews)
    
    # Use the summarizer to generate a summary
    summary = summarizer(reviews_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    
    return summary

def summarize_product_info(product_info):
    reviews = product_info['reviews']
    summary = generate_summary(reviews)
    product_info['summary'] = summary
    product_info['recommendation'] = f"This product is highly recommended because: {summary}"
    
    return product_info
