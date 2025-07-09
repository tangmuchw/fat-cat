# 用 FFmpeg 提取音频（用于辅助对齐）

ffmpeg -i video.mp4 -vn audio.wav

# 使用 aeneas 自动对齐（需 Python 环境）

pip install aeneas
aeneas_execute_task audio.wav text.txt "task_language=zh|os_task_file_format=srt" output.srt
