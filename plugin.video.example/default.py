# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
import urlparse
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = {'Animals': [('Crab', 'http://www.vidsplay.com/vids/crab.jpg',
                       'http://www.vidsplay.com/vids/crab.mp4'),
                        ('Alligator', 'http://www.vidsplay.com/vids/alligator.jpg',
                         'http://www.vidsplay.com/vids/alligator.mp4'),
                        ('Turtle', 'http://www.vidsplay.com/vids/turtle.jpg',
                         'http://www.vidsplay.com/vids/turtle.mp4')],
          'Cars': [('Postal Truck', 'http://www.vidsplay.com/vids/us_postal.jpg',
                    'http://www.vidsplay.com/vids/us_postal.mp4'),
                    ('Traffic', 'http://www.vidsplay.com/vids/traffic1.jpg',
                     'http://www.vidsplay.com/vids/traffic1.avi'),
                    ('Traffic Arrows', 'http://www.vidsplay.com/vids/traffic_arrows.jpg',
                     'http://www.vidsplay.com/vids/traffic_arrows.mp4')],
          'Food': [('Chicken', 'http://www.vidsplay.com/vids/chicken.jpg',
                    'http://www.vidsplay.com/vids/bbqchicken.mp4'),
                   ('Hamburger', 'http://www.vidsplay.com/vids/hamburger.jpg',
                    'http://www.vidsplay.com/vids/hamburger.mp4'),
                   ('Pizza', 'http://www.vidsplay.com/vids/pizza.jpg',
                    'http://www.vidsplay.com/vids/pizza.mp4')]}


def get_params():
    """
    Parse parameters string received as sys.argv[2] list item.
    :return: list
    """
    # Remove the starting '?' character from the paramstring.
    paramstring = sys.argv[2].replace('?', '')
    if paramstring:
        # if a paramstring present, parse it to the list of tuples (parameter, value)
        params = urlparse.parse_qsl(paramstring)
    else:
        # Return an empty stub list if there's no paramstring passed to the plugin.
        params = [('',)]
    return params


def get_categories():
    """
    Get the list of video categories.
    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.
    :return: list
    """
    return VIDEOS.keys()


def get_videos(category):
    """
    Get the list of videofiles/streams.
    Here you can insert some parsing code that retrieves
    the list of videostreams in a given category from some site or server.
    :param category: str
    :return: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    :return: None
    """
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category, thumbnailImage=VIDEOS[category][0][1])
        # Set a fanart image for the list item.
        # Here we use the same image as the thumbnail for simplicity's sake.
        list_item.setProperty('fanart_image', VIDEOS[category][0][1])
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?category=Animals
        url = '{0}?category={1}'.format(__url__, category)
        # Add the list item to a virtual Kodi folder.
        # isFolder=True means that this item opens a sub-list of lower level items.
        xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=True)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(__handle__)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.
    :param category: str
    :return: None
    """
    # Get the list of videos in the category.
    videos = VIDEOS[category]
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video[0], thumbnailImage=video[1])
        # Set a fanart image for the list item.
        # Here we use the same image as the thumbnail for simplicity's sake.
        list_item.setProperty('fanart_image', video[1])
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?play=http://www.vidsplay.com/vids/crab.mp4
        url = '{0}?play={1}'.format(__url__, video[2])
        # Add the list item to a virtual Kodi folder.
        # isFolder=False means that this item won't open any sub-list.
        xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=False)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(__handle__)


def play_video(path):
    """
    Play a video by the provided path.
    :param path: str
    :return: None
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)


if __name__ == '__main__':
    # Get parameters
    params = get_params()
    # Check the parameters passed to the plugin
    if params[0][0] == 'category':
        # Display the list of videos in a given category.
        list_videos(params[0][1])
    elif params[0][0] == 'play':
        # Play a video from a given URL.
        play_video(params[0][1])
    else:
        # Display the list of video categories
        # if the plugin is called from Kodi UI without parameters.
        list_categories()
