import pandas as pd
import numpy as np
import plotly.express as px

class FileExporter:
    @staticmethod
    def export_to_excel(metrics: dict, filename: str = "polarization_results.xlsx"):
        """Export all metrics to Excel file"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for key, data in metrics.items():
                pd.DataFrame(data).to_excel(writer, sheet_name=key[:31])
        return filename
    
    @staticmethod
    def create_summary_statistics(metrics: dict) -> pd.DataFrame:
        """Create summary statistics for all metrics"""
        stats = []
        for key, data in metrics.items():
            stats.append({
                'Metric': key,
                'Mean': np.mean(data),
                'Std': np.std(data),
                'Min': np.min(data),
                'Max': np.max(data),
                'Median': np.median(data)
            })
        return pd.DataFrame(stats)