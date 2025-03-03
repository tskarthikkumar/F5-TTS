---------------------------------------------------------------------------------------
option 1:
StartTTSAPI.bat to start the api server in windows

triggers:
tsk_api.py - used to run locally

tsk_api_ngrok.py - used to run from colab

---------------------------------------------------------------------------------------
option2: api server using official method:

conda activate f5-tts

run the server:
python src/f5_tts/socket_server.py --ref_audio src/f5_tts/assets/ref_audio.mp3

run the client to generate TTS:
python src/f5_tts/socket_client.py

creates output in src/f5_tts/output/


---------------------------------------------------------------------------------------
option3: official method to trigger gradio UI
conda activate f5-tts
f5-tts_infer-gradio
