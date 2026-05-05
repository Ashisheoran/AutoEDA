import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def histogram(self, column):
        fig = px.histogram(
            self.df,
            x=column,
            nbins=20,
            # title=f"{column} Distriburtion",
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
            # title=f"{column} Boxplot",
            template="plotly_dark"
        )    
        fig.update_layout(height=500)
        fig.update_traces(marker_line_width=1, marker_line_color="#6f102d")
        
        return fig


    def  scatter_with_trend(self, x_col, y_col, hue_col=None):
        import plotly.express as px

        df = self.df.copy()

        # Clean data
        df = df[[x_col, y_col] + ([hue_col] if hue_col else [])].dropna()

        # Validate
        if x_col == y_col:
            return None

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=hue_col,  # None = single color
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
            # title=f"{y_col} vs {x_col}",
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
    
    
    def correlation_heatmap(self):
        corr = self.df.corr(numeric_only=True)

        if corr.shape[0] < 2:
            return None
        
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu",
            # title="Correlation Heatmap"
        )

        fig.update_layout(height=700)

        return fig

    def violin_plot(self, column):
        fig = px.violin(
            self.df,
            x=column,
            box=True,
            # title=f"{column} Distribution (Violin)",
            template="plotly_dark"
        )

        fig.update_layout(height = 400)
        return fig
    
    def pair_plot(self):
        numeric_df = self.df.select_dtypes(include='number')

        if numeric_df.shape[1] < 2:
            return None
        
        fig = sns.pairplot(numeric_df.iloc[:, :4])
        return fig

    def categorical_bar(self, column):
        data = self.df[column].value_counts().reset_index()
        data.columns = [column, "count"]

        fig = px.bar(
            data,
            x=column,
            y="count",
            # title = f"{column} Distribution",
            template="plotly_dark"
        )

        fig.update_layout(height=400)
        return fig
    
    def pie_chart(self, column):
        data = self.df[column].value_counts().reset_index()
        data.columns = [column, "count"]

        fig = px.pie(
            data,
            names=column,
            values="count",
            # title=f"{column} Pie Distribution",
            template="plotly_dark"
        )

        fig.update_layout(height=400)
        return fig
    
    def donut_chart(self, column):
        data = self.df[column].value_counts().reset_index()
        data.columns = [column, "count"]

        fig = px.pie(
            data,
            names=column,
            values="count",
            hole=0.4,
            # title=f"{column} Donut Distribution",
            template="plotly_dark"
        )

        fig.update_layout(height=400)
        return fig

    def bubble_chart(self,x_col,y_col,size_col):
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            size=size_col,
            # title=f"{x_col} vs {y_col} (Bubble Size: {size_col})",
            template="plotly_dark"
        )

        fig.update_layout(height=400)
        return fig


    def categorical_vs_numeric_box(self, cat_col, num_col):
        fig = px.box(
            self.df,
            x = cat_col,
            y= num_col,
            # title=f"{num_col} vs {cat_col}",
            template="plotly"
        )
        fig.update_layout(height = 400)
        return fig


    def categorical_vs_numeric_violin(self, cat_col, num_col):
        fig = px.violin(
            self.df,
            x = cat_col,
            y= num_col,
            box = True,
            # title=f"{num_col} distribution by {cat_col}",
            template="ggplot2"
        )
        fig.update_layout(height = 400)
        return fig

    def categorical_mean(self, cat_col, num_col):
        data = self.df.groupby(cat_col)[num_col].mean().reset_index()
        fig = px.bar(
            data,
            x = cat_col,
            y= num_col,
            # box = True,
            # title=f"Average {num_col} by {cat_col}",
            template="ggplot2"
        )
        fig.update_layout(height = 400)
        return fig


    def categorical_vs_categorical_bar(self, col1, col2):
        df_count = self.df.groupby([col1,col2]).size().reset_index(name='count')

        fig = px.bar(
            df_count,
            x=col1,
            y="count",
            color=col2,
            barmode="group",
            template="plotly_dark",
            # title=f"{col1} vs {col2}"
        )
        fig.update_layout(height = 400)
        return fig

    def categorical_vs_categorical_stacked(self,col1, col2):
        df_count = self.df.groupby([col1,col2]).size().reset_index(name='count')

        fig = px.bar(
            df_count,
            x=col1,
            y="count",
            color=col2,
            barmode="stack",
            template="plotly_dark",
            # title=f"{col1} vs {col2} (stacked)"
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
            # title=f"{col1} vs {col2} Heatmap"
        )
        fig.update_layout(height = 500)
        return fig









# import matplotlib.pyplot as plt
# import seaborn as sns

# class DataVisualizer:
#     def __init__(self,df):
#         self.df = df

#     def histogram(self, column):
#         fig, ax = plt.subplots(figsize=(6, 4))
#         sns.histplot(self.df[column].dropna(), kde=True, ax=ax)
#         ax.set_title(f"Histogram of {column}")
#         return fig
    
#     def boxplot(self,column):
#         fig, ax = plt.subplots(figsize=(6, 4))
#         sns.boxplot(x=self.df[column],ax=ax)
#         ax.set_title(f"Boxplot of {column}")
#         return fig

#     def scatter(self, x_col, y_col):
#         fig, ax = plt.subplots(figsize=(6, 4))
#         sns.scatterplot(x=self.df[x_col], y=self.df[y_col], ax=ax)
#         ax.set_title(f"{x_col} vs {y_col}")
#         return fig


#     def correlation_heatmap(self):
#         numeric_df = self.df.select_dtypes(include=['number'])
        
#         if numeric_df.shape[1] < 2:
#             return None
        
#         corr = numeric_df.corr()
        
#         if corr.empty or corr.isnull().all().all():
#             return None

#         fig, ax = plt.subplots(figsize=(6, 4))
#         corr = self.df.corr(numeric_only = True)
        
#         sns.heatmap(
#             corr,
#             annot=True,
#             cmap="coolwarm",
#             fmt=".2f",
#             ax=ax
#         )

#         ax.set_title("Correlation Heatmap")
        
#         return fig