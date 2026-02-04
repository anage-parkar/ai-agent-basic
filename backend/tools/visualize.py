import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from typing import Dict, Any, List


class VisualizeTool:
    """Create quick visualizations"""
    
    def __init__(self):
        self.name = "visualize"
        self.description = """Create charts and visualizations.
Supported chart types: line, bar, scatter, pie
Input format: {
  "type": "line",  # line, bar, scatter, pie
  "data": {"x": [...], "y": [...]},  # or {"labels": [...], "values": [...]} for pie
  "title": "Chart Title",
  "xlabel": "X Label",
  "ylabel": "Y Label"
}
Returns: Base64 encoded PNG image"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create visualization"""
        chart_type = input_data.get("type", "line").lower()
        data = input_data.get("data", {})
        title = input_data.get("title", "")
        xlabel = input_data.get("xlabel", "")
        ylabel = input_data.get("ylabel", "")
        
        if not data:
            return {"error": "Data required for visualization"}
        
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "line":
                x = data.get("x", [])
                y = data.get("y", [])
                if not x or not y:
                    return {"error": "Line chart requires 'x' and 'y' data"}
                ax.plot(x, y, marker='o', linewidth=2)
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.grid(True, alpha=0.3)
            
            elif chart_type == "bar":
                x = data.get("x", [])
                y = data.get("y", [])
                if not x or not y:
                    return {"error": "Bar chart requires 'x' and 'y' data"}
                ax.bar(x, y, color='steelblue', alpha=0.8)
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                plt.xticks(rotation=45, ha='right')
            
            elif chart_type == "scatter":
                x = data.get("x", [])
                y = data.get("y", [])
                if not x or not y:
                    return {"error": "Scatter chart requires 'x' and 'y' data"}
                ax.scatter(x, y, alpha=0.6, s=100, color='coral')
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.grid(True, alpha=0.3)
            
            elif chart_type == "pie":
                labels = data.get("labels", [])
                values = data.get("values", [])
                if not labels or not values:
                    return {"error": "Pie chart requires 'labels' and 'values' data"}
                ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
            
            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
            
            if title:
                ax.set_title(title, fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            # Convert to base64
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
            
            return {
                "success": True,
                "image": img_base64,
                "type": chart_type
            }
            
        except Exception as e:
            plt.close('all')
            return {
                "success": False,
                "error": f"Visualization error: {str(e)}"
            }


# Global instance
visualize_tool = VisualizeTool()
