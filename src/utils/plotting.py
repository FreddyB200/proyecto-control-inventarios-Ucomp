"""Plotting utilities for creating different types of graphs."""
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta

class GraphCreator:
    """Graph creation manager."""
    
    def __init__(self):
        """Initialize graph creator."""
        # Set style
        plt.style.use('seaborn')
        sns.set_palette("husl")
        
    def create_bar_chart(
        self,
        data: Dict[str, float],
        title: str,
        xlabel: str,
        ylabel: str,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """Create a bar chart.
        
        Args:
            data: Dictionary with labels and values
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        x = np.arange(len(data))
        ax.bar(x, list(data.values()))
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(list(data.keys()), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
        
    def create_line_chart(
        self,
        data: Dict[str, List[float]],
        title: str,
        xlabel: str,
        ylabel: str,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """Create a line chart.
        
        Args:
            data: Dictionary with series names and lists of values
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for series_name, values in data.items():
            ax.plot(values, label=series_name)
            
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        
        plt.tight_layout()
        return fig
        
    def create_pie_chart(
        self,
        data: Dict[str, float],
        title: str,
        figsize: Tuple[int, int] = (8, 8)
    ) -> plt.Figure:
        """Create a pie chart.
        
        Args:
            data: Dictionary with labels and values
            title: Chart title
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.pie(
            list(data.values()),
            labels=list(data.keys()),
            autopct='%1.1f%%',
            startangle=90
        )
        
        ax.set_title(title)
        plt.tight_layout()
        return fig
        
    def create_scatter_plot(
        self,
        x: List[float],
        y: List[float],
        title: str,
        xlabel: str,
        ylabel: str,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """Create a scatter plot.
        
        Args:
            x: X-axis values
            y: Y-axis values
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.scatter(x, y)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        plt.tight_layout()
        return fig
        
    def create_heatmap(
        self,
        data: List[List[float]],
        row_labels: List[str],
        col_labels: List[str],
        title: str,
        figsize: Tuple[int, int] = (10, 8)
    ) -> plt.Figure:
        """Create a heatmap.
        
        Args:
            data: 2D list of values
            row_labels: Labels for rows
            col_labels: Labels for columns
            title: Chart title
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            data,
            xticklabels=col_labels,
            yticklabels=row_labels,
            annot=True,
            fmt='.2f',
            cmap='YlOrRd',
            ax=ax
        )
        
        ax.set_title(title)
        plt.tight_layout()
        return fig
        
    def save_figure(self, fig: plt.Figure, filename: str) -> None:
        """Save figure to file.
        
        Args:
            fig: Matplotlib figure object
            filename: Output filename
        """
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
    def create_time_series(
        self,
        data: Dict[str, List[float]],
        dates: List[datetime],
        title: str,
        xlabel: str,
        ylabel: str,
        figsize: Tuple[int, int] = (12, 6)
    ) -> plt.Figure:
        """Create a time series plot.
        
        Args:
            data: Dictionary with series names and lists of values
            dates: List of datetime objects
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for series_name, values in data.items():
            ax.plot(dates, values, label=series_name)
            
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig 