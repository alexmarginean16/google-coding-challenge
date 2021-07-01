"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random
from typing import Sequence


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currently_playing_state = False
        self.currently_playing = None

        self.isPaused = False

        self.playlists = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")

        videos = self._video_library.get_all_videos()
        videos_sorted = []
        for video in videos:
            line = str(video.title) + " (" + str(video.video_id) + ") ["
            
            for i in range(len(video.tags)):
                line += video.tags[i]
                if i != len(video.tags) - 1:
                    line += " "
            line += "]"

            videos_sorted.append(line)

        videos_sorted = sorted(videos_sorted)
        for video in videos_sorted:
            print(video)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot play video: Video does not exist")
        elif self.currently_playing_state is True:
            print("Stopping video: " + self.currently_playing)
            print("Playing video: " + video.title)
            self.currently_playing_state = True
            self.currently_playing = video.title
            self.isPaused = False
        else:
            print("Playing video: " + video.title)
            self.currently_playing_state = True
            self.currently_playing = video.title
            self.isPaused = False
        

    def stop_video(self):
        """Stops the current video."""
        if self.currently_playing_state is True:
            print("Stopping video: " + self.currently_playing)
            self.currently_playing_state = False
            self.currently_playing = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        num_videos = len(self._video_library.get_all_videos())
        random_num = random.randint(0, num_videos-1)
        random_video = self._video_library.get_all_videos()[random_num]
        
        self.play_video(random_video.video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.currently_playing_state is False:
            print("Cannot pause video: No video is currently playing")
        elif self.isPaused is False:
            print("Pausing video: " + self.currently_playing)
            self.isPaused = True
        else:
            print("Video already paused: " + self.currently_playing)

    def continue_video(self):
        """Resumes playing the current video."""
        if self.currently_playing_state is False:
            print("Cannot continue video: No video is currently playing")
        elif self.isPaused is True:
            print("Continuing video: " + self.currently_playing)
            self.isPaused = False
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.currently_playing_state is False:
            print("No video is currently playing")
        else:
            videos = self._video_library.get_all_videos()
            for video in videos:
                if self.currently_playing == video.title:
                    line = str(video.title) + " (" + str(video.video_id) + ") ["
                
                    for i in range(len(video.tags)):
                        line += video.tags[i]
                        if i != len(video.tags) - 1:
                            line += " "
                    line += "]"

                    if self.isPaused is False:
                        print("Currently playing: " + line)
                    else:
                        print("Currently playing: " + line + " - PAUSED")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        for playlist in self.playlists:
            if playlist.name.lower() == playlist_name.lower():
                print("Cannot create playlist: A playlist with the same name already exists")
                return

        new_playlist = Playlist(playlist_name)
        self.playlists.append(new_playlist)
        self.playlists = sorted(self.playlists, key=lambda x: x.name)
        print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        for playlist in self.playlists:
            if playlist.name.lower() == playlist_name.lower():
                video = self._video_library.get_video(video_id)
                if video is None:
                    print("Cannot add video to " + playlist_name + ": Video does not exist")
                    return
                else:
                    for vid_id in playlist.videos:
                        if vid_id == video_id:
                            print("Cannot add video to " + playlist_name + ": Video already added")
                            return

                    playlist.videos.append(video_id)
                    print("Added video to " + playlist_name + ": " + video.title)
                    return
        
        print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists) == 0:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        for playlist in self.playlists:
            print(playlist.name)


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        for playlist in self.playlists:
            if playlist.name.lower() == playlist_name.lower():
                print("Showing playlist: " + playlist_name)
                if len(playlist.videos) == 0:
                    print("No videos here yet")
                else:
                    for video_id in playlist.videos:
                        video = self._video_library.get_video(video_id)

                        line = str(video.title) + " (" + str(video.video_id) + ") ["
            
                        for i in range(len(video.tags)):
                            line += video.tags[i]
                            if i != len(video.tags) - 1:
                                line += " "
                        line += "]"
                        print(line)
                return

        print("Cannot show playlist " + playlist_name + ": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        for playlist in self.playlists:
            if playlist.name.lower() == playlist_name.lower():
                video_exists = self._video_library.get_video(video_id)
                if video_exists:
                    for i in range(len(playlist.videos)):
                        if playlist.videos[i] == video_id:
                            playlist.videos.pop(i)
                            print("Removed video from " + playlist_name + ": " + video_exists.title)
                            return
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
                    return
                    #for vid_id in playlist.videos:
                    #    if vid_id == video_id:
                else:
                    print("Cannot remove video from " + playlist_name + ": Video does not exist")
                    return

        print("Cannot remove video from " + playlist_name + ": Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        for playlist in self.playlists:
            if playlist.name.lower() == playlist_name.lower():
                for video in playlist.videos:
                    playlist.videos.pop()
                print("Successfully removed all videos from " + playlist_name)
                return

        print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        for i in range(len(self.playlists)):
            if self.playlists[i].name.lower() == playlist_name.lower():
                self.playlists.pop(i)
                print("Deleted playlist: " + playlist_name)
                return

        print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        videos_sorted = []
        for video in videos:
            line = []
            line.append(str(video.title))
            line.append(str(video.video_id))
            
            tags = []
            for i in range(len(video.tags)):
                tags.append(video.tags[i])
            line.append(tags)
            
            videos_sorted.append(line)

        videos_sorted = sorted(videos_sorted)
        video_results = []

        for video in videos_sorted:
            if video[0].lower().find(search_term.lower()) != -1:
                video_results.append(video)

        if len(video_results) != 0:
            print("Here are the results for " + search_term + ":")

            for video in video_results:
                print(str(video_results.index(video) + 1) + ")" , end = " ")
                print(video[0] + " ("+ video[1] + ") [", end = "")
                for i in range(len(video[2])):
                    print(video[2][i], end = "")
                    if i != len(video[2]) - 1:
                        print(" ", end = "")
                print("]")

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            command = input()

            try:
                index = int(command[0]) - 1
                video_title = video_results[index][0]
                print("Playing video: " + video_title)
            except:
                return
        else:
            print("No search results for " + search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
