import plotly.express as px  
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    def __init__(self, df):
        self.df = df

    def histogram(self, column):
        fig = px.histogram(
            self.df,
            x=column,
            nbins=min(50, max(10, len(self.df) // 100)),
            title=f"{column} Distriburtion",
            template="ggplot2",
            marginal='rug',
            )

        fig.update_layout(
            height = 400,
            margin = dict(l=20, r=20, t=40, b=20)
        )

        fig.update_traces(marker_line_width=1, marker_line_color="#0f1117")

        return fig

    def boxplot(self, column):
        fig = px.box(
            self.df,
            x=column,
            title=f"{column} Boxplot",
            template="plotly_dark"
        )    
        fig.update_layout(height=500)
        fig.update_traces(marker_line_width=1, marker_line_color="#6f102d")
        
        return fig
    
    def kde_plot(self, column):

        import plotly.figure_factory as ff

        data = [
            self.df[column].dropna()
        ]

        fig = ff.create_distplot(
            data,
            [column],
            show_hist=False,
            show_rug=False,
        )

        fig.update_layout(
            template="plotly_dark",
            height=500,
            title=f"KDE Plot - {column}",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
        )

        return fig


    def  scatter_with_trend(self, x_col, y_col, hue_col=None):

        if self.df.shape[0] > 5000:
            df = self.df.sample(n=5000, random_state=42)
        df = self.df.copy()

        df = df[[x_col, y_col] + ([hue_col] if hue_col else [])].dropna()

        if x_col == y_col:
            return None

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=hue_col,
            opacity=0.7,
            trendline="ols",
            color_discrete_sequence=[
                "#4c5af0", "#f72525", "#9be6ff", "#ffd166", "#4bff6c"
            ],
        )

        fig.update_traces(
            marker=dict(
                size=5,
                opacity=0.6,
                line=dict(width=0),
            )
        )

        fig.update_layout(
            title=f"{y_col} vs {x_col}",
            template="plotly_dark",
            height=650,

            paper_bgcolor="#0f1117",
            plot_bgcolor="#0f1117",

            font=dict(color="#e8eaf0"),

            margin=dict(l=20, r=20, t=40, b=20),

            legend=dict(
                bgcolor="#0f1117",
                bordercolor="#222",
                borderwidth=1
            )
        )

        for trace in fig.data:
            if "trendline" in trace.name.lower():
                trace.line.color = "#ffd166"
                trace.line.width = 5

        return fig
    
    def line_chart(self, x_col, y_col):
        fig = px.line(
            self.df,
            x=x_col,
            y=y_col,
            template="plotly_dark",
        )

        fig.update_layout(
            title=f"{y_col} vs {x_col}",
            height=500,
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
        )

        return fig
    
    
    def correlation_heatmap(self):
        corr = self.df.corr(numeric_only=True)

        if corr.shape[0] < 2:
            return None
        
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu",
            color_continuous_midpoint=0,
            title="Correlation Heatmap"
        )

        fig.update_layout(height=700)

        return fig
    
    def violin_plot(self, column):
        fig = px.violin(
            self.df,
            x=column,
            box=True,
            title=f"{column} Distribution (Violin)",
            template="plotly_dark"
        )

        fig.update_layout(height = 400)
        return fig


    def pair_plot(self):
        numeric_df = self.df.select_dtypes(include='number')

        if numeric_df.shape[1] < 2:
            return None
        
        sample_df = numeric_df.sample(n=min(1000, len(numeric_df)), random_state=42)

        fig = sns.pairplot(sample_df.iloc[:, :4])
        return fig

    def categorical_bar(self, column):
        data = self.df[column].value_counts().head(15).reset_index()
        data.columns = [column, "count"]

        fig = px.bar(
            data,
            x=column,
            y="count",
            title = f"{column} Distribution",
            template="plotly_dark"
        )

        fig.update_layout(height=400)
        return fig
    
    def pie_chart(self, column):
        data = self.df[column].value_counts().head(10).reset_index()
        data.columns = [column, "count"]

        fig = px.pie(
            data,
            names=column,
            values="count",
            title=f"{column} Pie Distribution",
            template="plotly_dark"
        )

        fig.update_layout(height=400)
        return fig
    
    def donut_chart(self, column):
        data = self.df[column].value_counts().head(10).reset_index()
        data.columns = [column, "count"]

        fig = px.pie(
            data,
            names=column,
            values="count",
            hole=0.4,
            title=f"{column} Donut Distribution",
            template="plotly_dark"
        )

        fig.update_layout(height=400)
        return fig
    
    def count_plot(self, column):

        if column is None:
            return None
        if column not in self.df.columns:
            return None

        data = self.df[column].astype(str).value_counts().head(20).reset_index()
        
        data.columns = [column, "count"]

        fig = px.bar(
            data,
            x=column,
            color=column,
            template="plotly_dark",
        )

        return fig


    def categorical_vs_numeric_box(self, cat_col, num_col):
        if self.df[cat_col].nunique() > 50:
            return None
        
        fig = px.box(
            self.df,
            x = cat_col,
            y= num_col,
            title=f"{num_col} vs {cat_col}",
            template="plotly"
        )
        fig.update_layout(height = 400)
        return fig
    
    def categorical_vs_numeric_violin(self, cat_col, num_col):
        if self.df[cat_col].nunique() > 50:
            return None
        
        fig = px.violin(
            self.df,
            x = cat_col,
            y= num_col,
            box = True,
            title=f"{num_col} distribution by {cat_col}",
            template="ggplot2"
        )
        fig.update_layout(height = 400)
        return fig

    def categorical_mean(self, cat_col, num_col):
        top_categories = self.df[cat_col].value_counts().head(20).index
        filtered_df = self.df[self.df[cat_col].isin(top_categories)]
        data = filtered_df.groupby(cat_col)[num_col].mean().reset_index()
        fig = px.bar(
            data,
            x = cat_col,
            y= num_col,
            title=f"Average {num_col} by {cat_col}",
            template="ggplot2"
        )
        fig.update_layout(height = 400)
        return fig


    def categorical_vs_categorical_bar(self, col1, col2):
        df_count = self.df.groupby([col1,col2]).size().head(20).reset_index(name='count')

        fig = px.bar(
            df_count,
            x=col1,
            y="count",
            color=col2,
            barmode="group",
            template="plotly_dark",
            title=f"{col1} vs {col2}"
        )
        fig.update_layout(height = 400)
        return fig

    def categorical_vs_categorical_stacked(self,col1, col2):
        df_count = self.df.groupby([col1,col2]).size().head(20).reset_index(name='count')

        fig = px.bar(
            df_count,
            x=col1,
            y="count",
            color=col2,
            barmode="stack",
            template="plotly_dark",
            title=f"{col1} vs {col2} (stacked)"
        )
        fig.update_layout(height = 400)
        return fig
    
    
    def categorical_heatmap(self,col1, col2):
        pivot = pd.crosstab(self.df[col2], self.df[col1])

        fig = px.imshow(
            pivot,
            text_auto=True,
            color_continuous_scale="Blues",
            template="plotly_dark",
            title=f"{col1} vs {col2} Heatmap"
        )
        fig.update_layout(height = 500)
        return fig