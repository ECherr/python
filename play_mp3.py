from pydub import AudioSegment

from pyaudio_play import play_audio

def trans_mp3_to_wav(file_path):
    print("* translate mp3 to wav")
    song = AudioSegment.from_mp3(file_path)
    music = file_path.split('.mp3')[0] + '.wav'
    song.export(music, format("wav"))
    print("* done translate")
    return music

def play_mp3(file_path):
    song = AudioSegment.from_mp3(file_path)

def main():
    file_path = './audio/平凡之路.mp3'
    music = trans_mp3_to_wav(file_path)
    play_audio(music)

if __name__ == '__main__':
    main()
