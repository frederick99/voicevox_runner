$speaker_id = 25

while ($text = Read-Host) {

# echo -n "こんにちは、音声合成の世界へようこそ" > text.txt
echo -n $text > text.txt

# curl.exe -s `
#     -X POST `
#     "localhost:50021/audio_query?speaker=1"`
#     --get --data-urlencode 'text@text.txt' `
#     > query.json

# curl.exe -s `
#     -X POST `
#     "localhost:50021/audio_query_from_preset?preset_id=3"`
#     --get --data-urlencode 'text@text.txt' `
#     -o query.json

$accent_phrases = (curl.exe -s `
    -X POST `
    "localhost:50021/accent_phrases?speaker=$speaker_id"`
    --get --data-urlencode "text@text.txt")

$payload = '{"accent_phrases":' + $accent_phrases + ',"speedScale":1,"pitchScale":0,"intonationScale":1,"volumeScale":1,"prePhonemeLength":0.1,"postPhonemeLength":0.1,"outputSamplingRate":24000,"outputStereo":true,"kana":""}'
echo $payload > query.json

curl.exe -s `
    -H "Content-Type: application/json" `
    -X POST `
    -d '@query.json' `
    "localhost:50021/synthesis?speaker=$speaker_id&enable_interrogative_upspeak=true" `
    -o audio.wav

if ($?) { cmdmp3win.exe .\audio.wav }
}
