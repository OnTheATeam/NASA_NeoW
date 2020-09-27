import argparse
from datetime import date

from asteroids import Asteroids
from plot import AsteroidPlot

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('api_key', help='NASA API key')
    args = parser.parse_args()

    asteroids = Asteroids(args.api_key)
    asteroids_list = asteroids.get_asteroids_today()
    
    plot = AsteroidPlot(str(date.today()))
    plot.plot_asteroids(asteroids_list)

if __name__ == "__main__":
    main()