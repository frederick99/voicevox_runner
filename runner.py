"""
Voicevox runner
"""

import abc
import logging
import multiprocessing
import urllib.parse

import requests
import simpleaudio


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Runner(abc.ABC):
    """Voicevox runner abstract base class"""

    def __init__(self, speaker_id=None):
        self.speaker_id = speaker_id if speaker_id else 25
        self.text_queue = multiprocessing.Queue()
        self.wave_queue = multiprocessing.Queue()

    def wave_worker(self):
        """Play wav"""
        try:
            logger.debug('wave thread running.')
            while True:
                # 再生
                wavefmt = self.wave_queue.get()
                logger.debug('playing')
                simpleaudio\
                    .play_buffer(audio_data=wavefmt, num_channels=2,
                                 bytes_per_sample=2, sample_rate=24000)\
                    .wait_done()
                logger.debug('done')
        except KeyboardInterrupt:
            logging.debug('wave worker done')

    # pylint: disable=line-too-long
    def text_worker(self):
        """Process TTS text"""
        try:
            logger.debug('text thread running.')
            with requests.Session() as session:
                while True:
                    logger.debug('waiting for text')
                    text = self.text_queue.get()
                    logger.debug('got text %s', text)

                    data = urllib.parse.quote(text)

                    logger.debug('getting accents %s', text)
                    accent_phrases = session.post(f"http://localhost:50021/accent_phrases?text={data}&speaker={self.speaker_id}").content
                    query = b'{"accent_phrases":' + accent_phrases + b',"speedScale":1,"pitchScale":0,"intonationScale":1,"volumeScale":1,"prePhonemeLength":0.1,"postPhonemeLength":0.1,"outputSamplingRate":24000,"outputStereo":true,"kana":""}'

                    logger.debug('getting wav %s', text)
                    wavefmt = session.post(f"http://localhost:50021/synthesis?speaker={self.speaker_id}&enable_interrogative_upspeak=true",
                                           data=query, headers={"Content-Type": "application/json"}).content

                    logger.debug('requesting playback: %s', text)
                    self.wave_queue.put_nowait(wavefmt)
        except KeyboardInterrupt:
            logging.debug('text worker done')

    def queue_tts(self, text):
        """Queue TTS test"""
        logger.debug('enqueuing %s', text)
        self.text_queue.put_nowait(text)

    def init(self):
        """Start worker threads"""
        wave_thread = multiprocessing.Process(target=self.wave_worker)
        text_thread = multiprocessing.Process(target=self.text_worker)

        wave_thread.start()
        text_thread.start()

    @abc.abstractmethod
    def tts_loop(self):
        """TTS loop"""
        return

    def main_loop(self):
        """Runner main loop"""
        try:
            self.init()
            self.tts_loop()
        except KeyboardInterrupt:
            logger.debug('closing queues')
            self.wave_queue.close()
            self.text_queue.close()
