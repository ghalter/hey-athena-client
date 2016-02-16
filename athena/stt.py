"""
    Basic Speech-To-Text tools are stored here
"""

import os, pyaudio, speech_recognition
import athena.tts as tts
import athena.settings as settings

from sphinxbase.sphinxbase import Config, Config_swigregister  # @UnusedImport
from pocketsphinx.pocketsphinx import Decoder

def init():
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-logfn', os.path.join(settings.LOGS_DIR, 'passive-listen.log'))
    config.set_string('-hmm', os.path.join(settings.MODEL_DIR, 'en-us\en-us'))
    config.set_string('-lm', os.path.join(settings.MODEL_DIR, 'en-us\en-us.lm.bin'))
    config.set_string('-dict', os.path.join(settings.MODEL_DIR, 'en-us\cmudict-en-us.dict'))
    
    # Decode streaming data
    global decoder, p
    decoder = Decoder(config)
    decoder.set_keyphrase('wakeup', settings.WAKE_UP_WORD)
    decoder.set_search('wakeup')
    p = pyaudio.PyAudio()

def listen_keyword():
    """
        Passively listens for the WAKE_UP_WORD string
    """
    global decoder, p
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    p.get_default_input_device_info()
    
    print('~ Waiting to be woken up... ')
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        decoder.process_raw(buf, False, False)
        if decoder.hyp() and decoder.hyp().hypstr == settings.WAKE_UP_WORD:
            decoder.end_utt()
            return
    decoder.end_utt()
    
def active_listen():
    """
        Actively listens for speech to translate into text
    
        :return: speech input as a text string
    """
    r = speech_recognition.Recognizer()

    # use the default microphone as the audio source
    with speech_recognition.Microphone() as src:   
        # listen for 1 second to adjust energy threshold for ambient noise
        r.adjust_for_ambient_noise(src)             
        print('\n~ Active listening... ')
        tts.play_mp3('double-beep.mp3')
        
        # listen for the first phrase and extract it into audio data
        audio = r.listen(src)
    
    msg = ''
    try:
        msg = r.recognize_google(audio)             # recognize speech using Google Speech Recognition
        print('\n~ \''+msg+'\'')
    except LookupError:                             # speech is unintelligible
        tts.speak(settings.ERROR)
    finally:
        return msg
