import datetime
from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Reds
class AsteroidPlot:
    def __init__(self, date_str:str):
        self.date_str = date_str
        self.plot_title = "Near Earth Objects Passing Earth On " + self.date_str
        
    def plot_asteroids(self, neos_list:list):
        names = [name for (name, miss_time, miss_dist, dia) in neos_list]
        x = [datetime.datetime.strptime(miss_time, '%Y-%b-%d %H:%M') for (name, miss_time, miss_dist, dia) in neos_list]
        y = [float(miss_dist) for (name, miss_time, miss_dist, dia) in neos_list]
        sizes = [float(dia) for (name, miss_time, miss_dist, dia) in neos_list]
        radii = [size * 1e7 for size in sizes]

        colors = []
        min_dist = min(y)
        max_dist = max(y)
        range_dist = max_dist - min_dist
        for dist in y:
            if dist == min_dist:
                colors.append("#%02x%02x%02x" % (255, 0, 0))

            elif dist == max_dist:
                colors.append("#%02x%02x%02x" % (0, 255, 0))

            else:
                perc = (dist - min_dist)/range_dist
                num = int(perc * 500)
                if num > 255:
                    colors.append("#%02x%02x%02x" % (0, num-255, 0))
                else:
                    colors.append("#%02x%02x%02x" % (255-num, 0, 0))

        source = ColumnDataSource(data=dict(hours=x,
                            distance=y,
                            names=names,
                            radii=radii,
                            sixes=sizes,
                            colors=colors))


        citation = Label(x=850, y=70, x_units='screen', y_units='screen',
                        text='Data From NASA NeoW API', render_mode='css',
                        border_line_color='black', border_line_alpha=0.6,
                        background_fill_color='white', background_fill_alpha=0.6)

        output_file("color_scatter.html", title="color_scatter.py example", mode="cdn")
        TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
        p = figure(tools=TOOLS, x_axis_type="datetime", plot_width=1250, height=650, x_axis_label="Hours After Midnight", 
            y_axis_label="Miles From Earth", title=self.plot_title)
        p.circle(x="hours", y="distance", source=source, radius="radii", fill_color="colors", fill_alpha=0.6, line_color=None)

        labels = LabelSet(x='hours', y='distance', text='names', source=source, text_font_size='8pt')

        p.add_layout(labels)
        p.add_layout(citation)
        show(p)



    
