from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from datetime import datetime

class ReportGenerator:
    """Generates HTML reports from simulation results using Jinja2 templates."""
    
    def __init__(self, template_dir='templates'):
        """
        Initialize the report generator.
        
        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = template_dir
        
        # Create templates directory if it doesn't exist
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Add custom filters
        self.env.filters['percentage'] = self._percentage_filter
        self.env.filters['currency'] = self._currency_filter
        
    def _percentage_filter(self, value, total):
        """Custom Jinja2 filter to calculate percentages."""
        if total == 0:
            return "0.00%"
        return f"{(value / total * 100):.2f}%"
    
    def _currency_filter(self, value):
        """Custom Jinja2 filter to format currency."""
        return f"${value:,.2f}"
    
    def generate_report(self, results, config, output_file):
        """
        Generate an HTML report from simulation results.
        
        Args:
            results: Dictionary containing simulation results
            config: Dictionary containing simulation configuration
            output_file: Path to output HTML file
        """
        template = self.env.get_template('report_template.html')
        
        # Prepare data for template
        report_data = {
            'title': 'Blackjack Simulation Report',
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'config': config,
            'results': results,
            'summary': self._calculate_summary(results)
        }
        
        # Render template
        html_content = template.render(**report_data)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _calculate_summary(self, results):
        """Calculate summary statistics across all players."""
        total_games = results.get('totalGames', 0)
        players = results.get('players', [])
        
        if not players:
            return {}
        
        total_wins = sum(p['wins'] for p in players)
        total_losses = sum(p['losses'] for p in players)
        total_draws = sum(p['draws'] for p in players)
        total_busts = sum(p['bustCount'] for p in players)
        
        # Calculate total winnings
        total_winnings = sum(
            float(p['totalWinnings'].replace('$', '').replace(',', '')) 
            for p in players
        )
        
        return {
            'totalGames': total_games,
            'totalWins': total_wins,
            'totalLosses': total_losses,
            'totalDraws': total_draws,
            'totalBusts': total_busts,
            'totalWinnings': total_winnings,
            'averageWinRate': f"{(total_wins / (total_games * len(players)) * 100):.2f}%" if total_games > 0 else "0.00%"
        }