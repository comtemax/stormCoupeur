import av
import sys
import Pathlib
import os

def walk_error_handler(exception_instance):
    print("os.walk seems to have failed with args : %s" % exception_instance)
    if exception_instance and exception_instance.filename:
        print(exception_instance.filename)
    if exception_instance and exception_instance.errno:
        print(exception_instance.errno)
    if exception_instance and exception_instance.keys:
        print(exception_instance.keys)
    if exception_instance and exception_instance.strerror:
        print(exception_instance.strerror)

def getThumbnail(video):
    #get the brightest(s) pictures of the thunder and save it aside the trimed vid
    return 0

def open_video(filepath):
    try:
        container = av.open(filepath)
    except (RuntimeError, TypeError, NameError, ValueError) as err:
        print(f"av.open failed on {filepath} with error [{err}]")
        return 0
    return container

def open_folder(path='~/Videos/'):
    processed_files = 0


    for (root, dirs, files) in os.walk(path, topdown=True, onerror=walk_error_handler):
        for file in files:
            processed_files += 1
            filename, file_extension = os.path.splitext(file)
#            print(f"{root} processing {filename} {file_extension.upper()}")
            #TODO not in (excluded_ext)
            # if file_extension.upper() in (allowed_ext):
            #     the_path = root
            #     # logic used to clean up path to first "=" when using smb
            #     # could be improved to skip to the last equal sign if needed
            #     if ('=' in root):
            #         the_path = root[root.rindex('=') + 1:]
            #
            #     path = os.path.join(root, file)
            #     the_size = os.stat(path).st_size  # get size in bytes
            #
            #     size_string = getMostAccurateSize(the_size)
            #     mv = File(name=file, path=the_path, edit_date=timezone.now(), size=the_size)
            #     my_movie_list.append(FileObject(file, the_path, the_size, timezone.now(), extension=file_extension))
            #     mv.save()

    for video in folder:
        open_video(video):

        return
    return

def write_video_chunk():
    return 0

def write_video_chunk():
    return 0

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
