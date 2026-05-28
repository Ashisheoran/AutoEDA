import pandas as pd


class ReportGenerator:

    def __init__(
        self,
        df,
        insights,
        charts=None,
        ml_results=None,
        ai_summary=None
    ):

        self.df = df
        self.insights = insights
        self.charts = charts or []
        self.ml_results = ml_results
        self.ai_summary = ai_summary


    def generate_html_report(self):

        html = f"""
        <html>
        <head>
            <title>AutoEDA Report</title>

            <style>

                body {{
                    background: #0f1117;
                    color: #e8eaf0;
                    font-family: Arial, sans-serif;
                    padding: 40px;
                    line-height: 1.7;
                }}

                h1, h2 {{
                    color: #4fd9c4;
                }}

                .card {{
                    background: #161a22;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    border: 1px solid #222;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}

                th, td {{
                    border: 1px solid #333;
                    padding: 10px;
                    text-align: left;
                }}

                th {{
                    background: #1e2430;
                }}

                .insight {{
                    background: #1b2330;
                    padding: 10px;
                    margin-bottom: 8px;
                    border-left: 4px solid #4fd9c4;
                    border-radius: 6px;
                }}

            </style>

        </head>

        <body>

        <h1>AutoEDA Report</h1>

        <div class="card">
            <h2>Dataset Overview</h2>

            <p><b>Rows:</b> {self.df.shape[0]}</p>
            <p><b>Columns:</b> {self.df.shape[1]}</p>

            <p><b>Numeric Columns:</b>
            {len(self.df.select_dtypes(include='number').columns)}
            </p>

            <p><b>Categorical Columns:</b>
            {len(self.df.select_dtypes(exclude='number').columns)}
            </p>
        </div>
        """


        html += """
        <div class="card">
            <h2>Data Preview</h2>
        """

        html += self.df.head().to_html()

        html += "</div>"

        missing = self.df.isnull().sum()

        missing_df = pd.DataFrame({
            "Column": missing.index,
            "Missing Values": missing.values
        })

        html += """
        <div class="card">
            <h2>Missing Value Analysis</h2>
        """

        html += missing_df.to_html(index=False)

        html += "</div>"

        html += """
        <div class="card">
            <h2>Statistical Summary</h2>
        """

        html += self.df.describe(include='all').to_html()

        html += "</div>"


        html += """
        <div class="card">
            <h2>Insights</h2>
        """

        for category, items in self.insights.items():

            html += f"<h3>{category.title()}</h3>"

            if items:
                for item in items:
                    html += f"""
                    <div class="insight">
                        {item}
                    </div>
                    """
            else:
                html += "<p>No major issues detected.</p>"

        html += "</div>"


        if self.ml_results:

            html += """
            <div class="card">
                <h2>Machine Learning Results</h2>
            """

            html += f"""
            <p><b>Best Model:</b>
            {self.ml_results.get('best_model')}
            </p>

            <p><b>Best Score:</b>
            {self.ml_results.get('best_score')}
            </p>
            """

            results_df = pd.DataFrame(
                self.ml_results.get("results", [])
            )

            html += results_df.to_html(index=False)

            html += "</div>"


        if self.ai_summary:

            html += """
            <div class="card">
                <h2>AI Summary</h2>
            """

            html += f"""
            <p>{self.ai_summary}</p>
            """

            html += "</div>"


        if self.charts:

            html += """
            <div class="card">
                <h2>Visualizations</h2>
            """

            for chart in self.charts:
                html += chart.to_html(
                    full_html=False,
                    include_plotlyjs="cdn"
                )

            html += "</div>"

        html += """
        </body>
        </html>
        """

        return html