import socket
import asyncio
import pyaudio
import numpy as np
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def listen_to_F5TTS(text, server_ip="localhost", server_port=9998):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    await asyncio.get_event_loop().run_in_executor(None, client_socket.connect, (server_ip, int(server_port)))

    start_time = time.time()
    first_chunk_time = None
    BUFFER_SIZE = 8192  
    audio_buffer = b''  # Buffer to accumulate incomplete chunks

    async def play_audio_stream():
        nonlocal first_chunk_time, audio_buffer
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=24000, output=True, frames_per_buffer=2048)

        try:
            while True:
                data = await asyncio.get_event_loop().run_in_executor(None, client_socket.recv, BUFFER_SIZE)
                if not data:
                    break
                if data == b"END":
                    logger.info("End of audio received.")
                    break

                # Accumulate data to ensure a multiple of 4 bytes
                audio_buffer += data
                if len(audio_buffer) < 4:
                    continue  # Not enough data to process yet
                
                # Process only multiples of 4 bytes
                valid_length = len(audio_buffer) - (len(audio_buffer) % 4)
                if valid_length == 0:
                    continue
                
                try:
                    audio_array = np.frombuffer(audio_buffer[:valid_length], dtype=np.float32)
                    stream.write(audio_array.tobytes())
                    audio_buffer = audio_buffer[valid_length:]  # Keep leftover bytes
                except ValueError as e:
                    logger.error(f"Invalid buffer size: {len(audio_buffer)} bytes. Error: {e}")
                    break  # Stop playback on error

                if first_chunk_time is None:
                    first_chunk_time = time.time()

        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

        logger.info(f"Total time taken: {time.time() - start_time:.4f} seconds")

    try:
        data_to_send = text.encode("utf-8")
        await asyncio.get_event_loop().run_in_executor(None, client_socket.sendall, data_to_send)
        await play_audio_stream()

    except Exception as e:
        logger.error(f"Error in listen_to_F5TTS: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    text_to_send = "TTS to speak"

    asyncio.run(listen_to_F5TTS(text_to_send))
