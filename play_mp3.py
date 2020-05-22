from pydub import AudioSegment

from pyaudio_play import play_audio

def trans_mp3_to_wav(file_path):
    print("* translate mp3 to wav")
    song = AudioSegment.from_mp3(file_path)
    song.export("pingfanzhilu.wav", format("wav"))
    print("* done translate")

def main():
    trans_mp3_to_wav("pingfanzhilu.mp3")
    play_audio("pingfanzhilu.wav")

if __name__ == '__main__':
    main()