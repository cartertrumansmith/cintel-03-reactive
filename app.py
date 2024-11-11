import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
import seaborn as sns
from shiny import reactive
import palmerpenguins

ui.page_opts(title="Filling layout", fillable=True)

penguins_df = palmerpenguins.load_penguins()
# Add a Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):
    # Use the ui.h2() function to add a 2nd level header to the sidebar
    ui.h2("Sidebar")
    
    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize("selected_attribute","Selected Attribute",["choice 1","choice 2","choise 3"])
    
    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count","Plotly Bin Count",1,min=1)
    
    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count","Seaborn Bin Count",value=1,min=1,max=100)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list","Selected Species List",["Adelie", "Gentoo", "Chinstrap"],selected=["Adelie"],inline=True)

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    ui.a("Github",href="https://github.com/cartertrumansmith/cintel-02-data",target="_blank")

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Data Table")

        @render.data_frame
        def species_data():
            return penguins_df[penguins_df['species'].isin(input.selected_species_list())]

        with ui.card(full_screen=True):
            ui.card_header("Data Grid")
            @render.data_frame
            def grid():
               return render.DataGrid(data=penguins_df)



with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram: Species")

        @render_plotly
        def histogram_plotly():
            return px.histogram(filtered_data(), x="bill_length_mm",nbins=input.plotly_bin_count())
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram: Species")

        @render.plot
        def histogram_seaborn():
            return sns.histplot(data=filtered_data(),x="bill_length_mm",bins=input.seaborn_bin_count())
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(data_frame=filtered_data(),x="bill_length_mm", y="body_mass_g",color="species",hover_name="island",symbol="sex")

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    
    return penguins_df

