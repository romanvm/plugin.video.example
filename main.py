# Author: Roman V. M.
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Example video plugin that is compatible with Kodi 20.x "Nexus" and above
"""
import sys
from urllib.parse import urlencode, parse_qsl

import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

# Public domain movies are from https://publicdomainmovie.net
# Here we use a hardcoded list of movies simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some website or online service.
VIDEOS = [
    {
        'genre': 'Drama',
        'icon': '',
        'movies': [
            {
                'title': 'The Stranger',
                'url': 'https://ia800908.us.archive.org/30/items/TheStranger_0/The_Stranger_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Movie-Mystery-Magazine-July-1946.jpg',
                'plot': 'In 1946, Mr. Wilson (Edward G. Robinson) of the United Nations War Crimes Commission is hunting for '
                        'a Nazism fugitive Franz Kindler (Orson Welles), a war criminal who has erased all evidence which '
                        'might identify him. Kindler has assumed a new identity, Charles Rankin, '
                        'and has become a University-preparatory school#United States and Canada teacher '
                        'in a small town in the United States. ',
                'year': 1946,
            },
            {
                'title': 'The Iron Mask',
                'url': 'https://ia600702.us.archive.org/3/items/iron_mask/iron_mask_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Ironmaskposter.jpg',
                'plot': 'The Iron Mask is a 1929 American part-talkie adventure film directed by Allan Dwan. '
                          'It is an adaptation of the last section of the novel The Vicomte de Bragelonne by '
                          'Alexandre Dumas, père, which is itself based on the French legend of The Man in the Iron Mask.',
                'year': 1929,
            },
            {
                'title': 'Meet John Doe',
                'url': 'https://ia804707.us.archive.org/30/items/meet_john_doe_ipod/video_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Poster_-_Meet_John_Doe_01.jpg',
                'plot': 'Meet John Doe is a 1941 in film United States comedy film drama film film directed and produced '
                        'by Frank Capra, and starring Gary Cooper and Barbara Stanwyck. The film is about a "grassroots" '
                        'political campaign created unwittingly by a newspaper columnist and pursued by a wealthy businessman.',
                'year': 1941,
            },
        ],
    },
    {
        'genre': 'Horror',
        'icon': '',
        'movies': [
            {
                'title': 'House on Haunted Hill',
                'url': 'https://ia800203.us.archive.org/18/items/house_on_haunted_hill_ipod/house_on_haunted_hill_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=House_on_Haunted_Hill.jpg',
                'plot': 'Eccentric millionaire Frederick Loren (Vincent Price) invites five people to a "party" '
                        'he is throwing for his fourth wife, Annabelle (Carol Ohmart), '
                        'in an allegedly haunted house he has rented, promising to give them each $10,000 '
                        'with the stipulation that they must stay the entire night in the house after '
                        'the doors are locked at midnight.',
                'year': 1959,
            },
        ],
    },
]


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(_URL, urlencode(kwargs))


def get_genres():
    """
    Get the list of video genres

    Here you can insert some code that retrieves
    the list of video sections (in this case movie genres) from some site or API.

    :return: The list of video genres
    :rtype: list
    """
    return VIDEOS


def get_videos(genre_index):
    """
    Get the list of videofiles/streams.

    Here you can insert some code that retrieves
    the list of video streams in the given section from some site or API.

    :param genre_index: genre index
    :type genre_index: int
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[genre_index]


def list_genres():
    """
    Create the list of movie genres in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'Public Domain Movies')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'movies')
    # Get movie genres
    genres = get_genres()
    # Iterate through genres
    for index, genre in enumerate(genres):
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=genre['genre'])
        # Set additional info for the list item using its InfoTag.
        # Here we use a category name for both properties for simplicity's sake.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(genre)
        info_tag.setGenres([genre])
        # Set icon for the list item.
        # addAvailableArtwork() method can be used to add different types of images: poster, fanart, etc.
        info_tag.addAvailableArtwork(genre['icon'], 'icon')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0
        url = get_url(action='listing', genre_index=index)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)


def list_videos(genre_index):
    """
    Create the list of playable videos in the Kodi interface.

    :param genre_index: the index of genre in the list of videos
    :type genre_index: int
    """
    genre_info = VIDEOS[genre_index]
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, genre_info['genre'])
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'movies')
    # Get the list of videos in the category.
    videos = genre_info['movies']
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label
        list_item = xbmcgui.ListItem(label=video['title'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('movie')
        info_tag.setTitle(video['title'])
        info_tag.setGenres(genre_info['genre'])
        info_tag.setPlot(video['plot'])
        info_tag.setYear(video['year'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use only for simplicity's sake.
        # In a real-life plugin you may need to set multiple image types.
        info_tag.addAvailableArtwork(video['poster'], 'poster')
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['url'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(int(params['genre_index']))
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_genres()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
