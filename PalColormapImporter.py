# Carter J. Humphreys (GitHub: @HumphreysCarter)
# 12/30/2020

import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize


def read_pal_file(path):
    """
    Parses .pal file for color information and returns as Pandas DataFrame
    .pal specification: http://www.grlevelx.com/manuals/color_tables/files_color_table.htm
    """
    # Initlize empty DataFrame
    df = pd.DataFrame()

    # Open .pal file
    with open(path, 'r') as f:
    
        # Read each line and find colors
        for line in f.readlines():
            if 'color' in line.lower():
                # Substring to data value and RGB colors
                color = line[:line.find(':')].lower()
                line  = line[line.find(':')+1:]
            
                # Strip excess whitespace
                row = line.strip()
            
                # Split values into list
                values = line.split()
            
                # Remove Alpha values if Color4 or SolidColor4
                if 'color4' in color:
                    if len(values) == 9:
                        values.pop(4)
                        values.pop(-1)
                    elif len(values) == 5:
                        values.pop(4)
            
                # Convert list to series of RGB, use data value as name
                s = pd.Series(data=values[1:], name=float(values[0]), dtype='int')
            
                # Add to DataFrame
                df = df.append(s)
            
    # Ensure values are in correct order
    df = df.sort_index()

    return df


def get_color_list(df):
    """
    Generates list of RGB tuples from list of RGB values in Pandas DataFrame
    """
    colors=[]
    for r, g, b in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]):
        colors.append((r/255, g/255, b/255))
    
    return colors


def build_colormap_norm(colors, values):
    """
    Generates a linear colormap and normalization from list of colors and data values
    """
    # Create colormap from RGB with number of bins based on range of values
    cmap = LinearSegmentedColormap.from_list('test.pal', colors, N=max(values)-min(values))
    
    # Create colormap normalization from values range
    norm = Normalize(vmin=min(values), vmax=max(values))
    
    return cmap, norm


def get_pal_colormap(pal_file, include_norm=True):
    """
    Generates matplotlib colormap and norm from .pal file
    """
    # Parse .pal file
    df = read_pal_file(pal_file)
    
    # Get list of colors
    colors = get_color_list(df)
    
    # Get colormap
    cmap, norm = build_colormap_norm(colors, df.index)
    
    if include_norm:
        return cmap, norm
    else:
        return cmap