"""
Visualization module for AI Flashcards application
Generates charts and graphs for study statistics
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Flask
import matplotlib.pyplot as plt
import io
import base64
from analytics import *

def generate_deck_progress_chart(deck_stats):
    """Generate bar chart showing deck progress"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if not deck_stats:
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
        return _fig_to_base64(fig)
    
    deck_names = [d['name'][:15] + '...' if len(d['name']) > 15 else d['name'] 
                  for d in deck_stats]
    progress = [d['progress'] for d in deck_stats]
    
    bars = ax.bar(deck_names, progress, color='#3498db', alpha=0.7)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    ax.set_ylabel('Progress (%)', fontsize=12)
    ax.set_xlabel('Deck', fontsize=12)
    ax.set_title('Study Progress by Deck', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 110)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return _fig_to_base64(fig)

def generate_interval_distribution_chart(data):
    """Generate pie chart showing card interval distribution"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    if not data['values'] or sum(data['values']) == 0:
        ax.text(0.5, 0.5, 'No cards to display', ha='center', va='center')
        return _fig_to_base64(fig)
    
    colors = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    
    wedges, texts, autotexts = ax.pie(data['values'], 
                                        labels=data['labels'],
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90)
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Card Distribution by Review Interval', 
                 fontsize=14, fontweight='bold', pad=20)
    
    return _fig_to_base64(fig)

def generate_difficulty_distribution_chart(data):
    """Generate horizontal bar chart showing difficulty distribution"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if not data['values'] or sum(data['values']) == 0:
        ax.text(0.5, 0.5, 'No studied cards', ha='center', va='center')
        return _fig_to_base64(fig)
    
    colors = {'Very Hard': '#e74c3c', 'Hard': '#e67e22', 
              'Medium': '#f39c12', 'Easy': '#2ecc71'}
    
    bar_colors = [colors.get(label, '#95a5a6') for label in data['labels']]
    
    bars = ax.barh(data['labels'], data['values'], color=bar_colors, alpha=0.7)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, data['values'])):
        ax.text(val, i, f' {val}', va='center')
    
    ax.set_xlabel('Number of Cards', fontsize=12)
    ax.set_title('Card Difficulty Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return _fig_to_base64(fig)

def generate_upcoming_reviews_chart(data):
    """Generate line chart showing upcoming reviews"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if not data['values']:
        ax.text(0.5, 0.5, 'No upcoming reviews', ha='center', va='center')
        return _fig_to_base64(fig)
    
    ax.plot(data['labels'], data['values'], marker='o', 
            linewidth=2, markersize=8, color='#3498db')
    ax.fill_between(range(len(data['values'])), data['values'], 
                     alpha=0.3, color='#3498db')
    
    # Add value labels
    for i, val in enumerate(data['values']):
        ax.text(i, val, str(val), ha='center', va='bottom')
    
    ax.set_ylabel('Number of Cards Due', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_title('Upcoming Review Forecast (Next 7 Days)', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return _fig_to_base64(fig)

def generate_retention_metrics_chart(metrics):
    """Generate bar chart showing retention metrics"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = ['1st Review\nRetention', '2nd Review\nRetention', 'Mature Card\nRate']
    values = [
        metrics['first_review_retention'],
        metrics['second_review_retention'],
        metrics['mature_card_rate']
    ]
    
    colors = ['#3498db', '#2ecc71', '#9b59b6']
    bars = ax.bar(labels, values, color=colors, alpha=0.7)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Retention Rate (%)', fontsize=12)
    ax.set_title('Learning Retention Metrics', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 110)
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    
    return _fig_to_base64(fig)

def generate_overall_summary_chart(stats):
    """Generate summary donut chart"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    if stats['total_cards'] == 0:
        ax.text(0.5, 0.5, 'No cards yet', ha='center', va='center')
        return _fig_to_base64(fig)
    
    # Data
    labels = ['Studied', 'Unstudied', 'Due Today']
    sizes = [
        stats['studied_cards'],
        stats['unstudied_cards'],
        stats['due_cards']
    ]
    colors = ['#2ecc71', '#95a5a6', '#e74c3c']
    
    # Create donut chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors, startangle=90,
                                        wedgeprops=dict(width=0.5))
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # Add center text
    ax.text(0, 0, f'{stats["total_cards"]}\nTotal Cards', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    ax.set_title('Overall Study Status', fontsize=14, fontweight='bold', pad=20)
    
    return _fig_to_base64(fig)

def _fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for HTML embedding"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64