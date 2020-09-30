import datetime
from bokeh.models import ColumnDataSource, Label, LabelSet, OpenURL, TapTool
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Reds


class AsteroidPlot:
    def __init__(self, date_str:str):
        self.date_str = date_str
        self.plot_title = "Near Earth Objects Passing Earth On " + self.date_str
        
    def plot_asteroids(self, neos_list:list):
        # We will label each circle on our plot with the NEO name and it's diameter
        names = [(name + " {:.2f}".format(dia) + " M wide") for (name, miss_time, miss_dist, dia, url) in neos_list]
        names.append('Moon') # We will add the moon to our plot to help give a sense of scale

        # Drop the nanoseconds we don't need off the end of the timestamps
        x = [datetime.datetime.strptime(miss_time[0:-7], '%Y-%m-%d %H:%M:%S') for (name, miss_time, miss_dist, dia, url) in neos_list]
        x.append(datetime.datetime.strptime(self.date_str + ' 04:00', '%Y-%m-%d %H:%M')) # We'll put the moon at 4 hours

        # Distance from Earth will go along the Y axis
        y = [float(miss_dist) for (name, miss_time, miss_dist, dia, url) in neos_list]
        y.append(238900)  # The moon is 238,900 from Earth

        # Let's represent each NEO's relative size with the diameter of each circle
        # Since most NEOs are less than a mile wide, we will need to scale them by a factor of 1e7
        # to see them on our plot
        sizes = [float(dia) for (name, miss_time, miss_dist, dia, url) in neos_list]
        radii = [size * 1e7 for size in sizes]
        radii.append(1e6) # This is an arbitrary size, since the moon is actually much larger than any of our NEOs

        # Users will be able to click on each circle to view the NASA's page for each NEO
        urls = [url for (name, miss_time, miss_dist, dia, url) in neos_list]
        urls.append('https://moon.nasa.gov/')  # Moon website!

        # Let's make the NEOs coming close to Earth red and the
        # ones farthest from Earth green
        colors = []
        min_dist = min(y)
        max_dist = max(y)
        range_dist = max_dist - min_dist
        for (name, dist) in zip(names, y):
            if name == 'Moon':
                colors.append('#0EBFE9')  # Let's make the moon blue so that 
                                          # it's clear it's different from the NEOs
            elif dist == min_dist:
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

        # Create the ColumnDataSource that we will use for plotting and creating labels
        source = ColumnDataSource(data=dict(hours=x,
                            distance=y,
                            names=names,
                            radii=radii,
                            colors=colors,
                            url=urls))


        # Let's label each NEO to make our plot more meaningful
        citation = Label(x=850, y=70, x_units='screen', y_units='screen',
                        text='Data From NASA NeoW API', render_mode='css',
                        border_line_color='black', border_line_alpha=0.6,
                        background_fill_color='white', background_fill_alpha=0.6)

        # Let's make a note comparing the moon's real diameter to the largest NEO on this plot
        max_size = max(sizes)
        scale = " {:.2f}".format(2158.8/max_size) # Moon is 2,158.8 miles in diameter

        moon_note = Label(x=150, y=30, x_units='screen', y_units='screen',
                text='Moon diameter not to scale; it is ' + scale + 'x larger than largest NEO on this plot.', render_mode='css',
                border_line_color='black', border_line_alpha=0.6,
                background_fill_color='white', background_fill_alpha=0.6, text_font_size="8pt")

        # Output our plot to a static HTML file
        output_file("neos_today.html", title="NEOs Demo", mode="cdn")

        # Set up our plots
        TOOLS = "pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,tap"
        p = figure(tools=TOOLS, x_axis_type="datetime", plot_width=1250, height=650, x_axis_label="Hours After Midnight", 
            y_axis_label="Miles From Earth", title=self.plot_title)
        p.circle(x="hours", y="distance", source=source, radius="radii", fill_color="colors", fill_alpha=0.6, line_color=None)

        labels = LabelSet(x='hours', y='distance', text='names', source=source, text_font_size='8pt')

        p.add_layout(labels)
        p.add_layout(citation)
        p.add_layout(moon_note)

        # Add TapTool call back that will open a new tab with our NEO URL on a click
        taptool = p.select(type=TapTool)
        taptool.callback = OpenURL(url="@url")

        # Display the plot in a browser
        show(p)



    
