# ui/components/results_view.py
"""Backward compatibility facade re-exporting render_results from results_dashboard."""
from ui.components.results_dashboard import render_results

__all__ = ["render_results"]
