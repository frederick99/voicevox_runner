import collections
import asyncio
import simpleaudio
import requests
import urllib.parse

# from concurrent import futures
# from requests_futures import sessions

class Runner:
    def __init__(self, speaker_id = 25):
        self.speaker_id = speaker_id
        self.text_queue = collections.deque()
        self.wave_queue = collections.deque()

    async def wave_thread(self):
        # print('wave thread running.')
        while True:
            while not self.wave_queue:
                await asyncio.sleep(.1)
            # 再生
            # print('playing')
            wavefmt = self.wave_queue.popleft()
            simpleaudio\
                .play_buffer(audio_data=wavefmt, num_channels=2, bytes_per_sample=2, sample_rate=24000)\
                .wait_done()
            # print('done')

    async def text_thread(self):
        # print('text thread running.')
        with requests.Session() as session:

            while True:
                while len(self.text_queue) == 0:
                    await asyncio.sleep(.1)

                text = self.text_queue.popleft()
                data = urllib.parse.quote(text)

                # print('getting accents', text)
                accent_phrases = session.post(f"http://localhost:50021/accent_phrases?text={data}&speaker={self.speaker_id}").content
                query = b'{"accent_phrases":' + accent_phrases + b',"speedScale":1,"pitchScale":0,"intonationScale":1,"volumeScale":1,"prePhonemeLength":0.1,"postPhonemeLength":0.1,"outputSamplingRate":24000,"outputStereo":true,"kana":""}'

                # print(query)

                # print('getting wav', text)
                wavefmt = session.post(f"http://localhost:50021/synthesis?speaker={self.speaker_id}&enable_interrogative_upspeak=true", data=query, headers={"Content-Type": "application/json"}).content
                self.wave_queue.append(wavefmt)

                # print('requesting playback:', text)

    def enqueue(self, text):
        # print('enqueuing:', text)
        self.text_queue.append(text)

    def run(self):
        return NotImplemented()
